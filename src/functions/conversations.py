from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, or_
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
import os


# 創建獨立的數據庫會話（用於工具調用）
async def get_db_session():
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/app.db")
    engine = create_async_engine(DATABASE_URL)
    from sqlalchemy.orm import sessionmaker

    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    return AsyncSessionLocal()


from src.database import SessionLocal
from src.models import Conversation

# 導入事件管理器
from src.functions.server import event_manager

router = APIRouter()


# Pydantic模型用於請求和響應
class ConversationCreate(BaseModel):
    role: str
    content: str
    extra_metadata: Optional[Dict[str, Any]] = None


class ConversationResponse(BaseModel):
    id: int
    timestamp: datetime
    role: str
    content: str
    extra_metadata: Optional[Dict[str, Any]] = None

    # 使用ConfigDict代替Config類
    model_config = ConfigDict(from_attributes=True)


# 依賴注入：獲取資料庫會話
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


# 紀錄對話的API端點
@router.post("/conversations/", response_model=ConversationResponse)
async def create_conversation_endpoint(
    conversation: ConversationCreate, db: AsyncSession = Depends(get_db)
):
    return await create_conversation(conversation, db)


# 創建對話的工具函數
async def create_conversation(
    conversation: Union[ConversationCreate, Dict[str, Any]],
    db: Optional[AsyncSession] = None,
):
    close_db = False
    if db is None:
        db = await get_db_session()
        close_db = True

    try:
        if isinstance(conversation, dict):
            conversation = ConversationCreate(**conversation)

        # 創建新的對話記錄
        db_conversation = Conversation(
            role=conversation.role,
            content=conversation.content,
            extra_metadata=conversation.extra_metadata,
        )

        # 添加到資料庫
        db.add(db_conversation)
        await db.commit()
        await db.refresh(db_conversation)

        # 將新對話記錄轉換為字典並廣播給所有連接的客戶端
        conversation_dict = {
            "id": db_conversation.id,
            "timestamp": db_conversation.timestamp.isoformat(),
            "role": db_conversation.role,
            "content": db_conversation.content,
            "extra_metadata": db_conversation.extra_metadata,
        }

        # 異步廣播新對話記錄
        await event_manager.broadcast_conversation(conversation_dict)

        return db_conversation
    except Exception as e:
        # Error handling - removed print statement, use proper logging in production
        if "db" in locals() and db is not None:
            await db.rollback()
        raise HTTPException(status_code=500, detail=f"無法創建對話記錄: {str(e)}")
    finally:
        if close_db and "db" in locals() and db is not None:
            await db.close()


# 搜尋對話的API端點
@router.get("/search/", response_model=List[ConversationResponse])
async def search_conversations_endpoint(
    query: str = Query(..., description="搜尋關鍵字"),
    skip: int = Query(0, description="跳過的記錄數"),
    limit: int = Query(10, description="返回的最大記錄數"),
    db: AsyncSession = Depends(get_db),
):
    return await search_conversations(query, skip, limit, db)


# 搜尋對話的工具函數
async def search_conversations(
    query: str, skip: int = 0, limit: int = 10, db: Optional[AsyncSession] = None
):
    close_db = False
    if db is None:
        db = await get_db_session()
        close_db = True

    try:
        # 構建基本搜尋查詢（使用LIKE操作進行簡單文本匹配）
        search_query = (
            select(Conversation)
            .filter(
                or_(
                    Conversation.content.like(f"%{query}%"),
                    Conversation.role.like(f"%{query}%"),
                )
            )
            .offset(skip)
            .limit(limit)
        )

        # 執行查詢
        result = await db.execute(search_query)
        conversations = result.scalars().all()

        # 如果沒有找到結果，返回空列表
        if not conversations:
            return []

        return conversations
    except Exception as e:
        # Error handling - removed print statement
        raise HTTPException(status_code=500, detail=f"搜尋過程中發生錯誤: {str(e)}")
    finally:
        if close_db and "db" in locals() and db is not None:
            await db.close()


# 獲取所有對話的API端點（用於測試）
@router.get("/conversations/", response_model=List[ConversationResponse])
async def get_all_conversations_endpoint(
    skip: int = Query(0, description="跳過的記錄數"),
    limit: int = Query(10, description="返回的最大記錄數"),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_conversations(skip, limit, db)


# 獲取所有對話的工具函數
async def get_all_conversations(
    skip: int = 0, limit: int = 10, db: Optional[AsyncSession] = None
):
    close_db = False
    if db is None:
        db = await get_db_session()
        close_db = True

    try:
        query = select(Conversation).offset(skip).limit(limit)
        result = await db.execute(query)
        conversations = result.scalars().all()
        return conversations
    except Exception as e:
        # Error handling - removed print statement
        raise HTTPException(status_code=500, detail=f"獲取對話列表時發生錯誤: {str(e)}")
    finally:
        if close_db and "db" in locals() and db is not None:
            await db.close()


# 根據ID獲取單個對話的API端點
@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation_endpoint(
    conversation_id: int, db: AsyncSession = Depends(get_db)
):
    return await get_conversation(conversation_id, db)


# 根據ID獲取單個對話的工具函數
async def get_conversation(conversation_id: int, db: Optional[AsyncSession] = None):
    close_db = False
    if db is None:
        db = await get_db_session()
        close_db = True

    try:
        query = select(Conversation).filter(Conversation.id == conversation_id)
        result = await db.execute(query)
        conversation = result.scalars().first()

        if conversation is None:
            raise HTTPException(status_code=404, detail="對話記錄不存在")

        return conversation
    except HTTPException:
        raise
    except Exception as e:
        # Error handling - removed print statement
        raise HTTPException(status_code=500, detail=f"獲取對話記錄時發生錯誤: {str(e)}")
    finally:
        if close_db and "db" in locals() and db is not None:
            await db.close()

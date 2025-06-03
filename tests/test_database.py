from dotenv import load_dotenv
load_dotenv()

import pytest
from sqlalchemy import select
from datetime import datetime

from src.models import Conversation
from src.database import engine

@pytest.mark.asyncio
async def test_database_connection():
    """測試資料庫連接是否正常"""
    async with engine.connect() as conn:
        result = await conn.execute(select(1))
        assert result.scalar() == 1

@pytest.mark.asyncio
async def test_create_conversation(db_session):
    """測試建立對話記錄"""
    # 建立測試資料
    conversation = Conversation(
        timestamp=datetime.now(),
        role="user",
        content="這是一條測試訊息",
        extra_metadata={"source": "test"}
    )
    
    # 新增到資料庫
    db_session.add(conversation)
    
    # 手動將資料重新載入
    await db_session.flush()
    
    # 從資料庫獲取並驗證
    result = await db_session.execute(
        select(Conversation).filter_by(content="這是一條測試訊息")
    )
    saved_conversation = result.scalars().first()
    
    assert saved_conversation is not None
    assert saved_conversation.role == "user"
    assert saved_conversation.content == "這是一條測試訊息"
    assert saved_conversation.extra_metadata == {"source": "test"}

@pytest.mark.asyncio
async def test_retrieve_conversation(db_session):
    """測試讀取對話記錄"""
    # 建立測試資料
    conversation = Conversation(
        timestamp=datetime.now(),
        role="assistant",
        content="測試回應",
        extra_metadata={"response_time": 0.5}
    )
    
    # 新增到資料庫
    db_session.add(conversation)
    await db_session.flush()
    
    # 從資料庫讀取並驗證
    retrieved_id = conversation.id
    result = await db_session.execute(
        select(Conversation).filter_by(id=retrieved_id)
    )
    retrieved_conversation = result.scalars().first()
    
    assert retrieved_conversation is not None
    assert retrieved_conversation.id == retrieved_id
    assert retrieved_conversation.role == "assistant"
    assert retrieved_conversation.content == "測試回應"
    assert retrieved_conversation.extra_metadata == {"response_time": 0.5} 
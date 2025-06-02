from dotenv import load_dotenv
load_dotenv()

import pytest_asyncio # 導入 pytest_asyncio
import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
import json

from src.database import SessionLocal
from src.models import Conversation # 導入 Conversation 模型
from src.database import engine, Base # 導入 engine 和 Base
from datetime import datetime # 導入 datetime
from typing import AsyncGenerator # 引入 AsyncGenerator

@pytest.fixture(scope="session") # 新增 session 作用範圍的 anyio_backend fixture
def anyio_backend():
    return "asyncio"

# @pytest_asyncio.fixture(scope="module") # 移除 create_tables fixture
# async def create_tables():
#     """在測試模組開始前創建資料表"""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     # 可選：在測試模組結束後刪除資料表，以確保測試環境的乾淨

# 為每個測試提供一個獨立的異步 Session，並在測試結束時回滾
@pytest_asyncio.fixture(scope="function") # 使用 pytest_asyncio 的 fixture，作用範圍為每個測試函數
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.connect() as connection:
        # 開始一個事務塊
        async with connection.begin() as transaction:
            # 使用這個連線綁定創建一個異步 Session
            session = SessionLocal(
                bind=connection,
                join_transaction_mode="create_savepoint"
            )

            # 在測試執行期間提供 session
            yield session

            # 測試結束後，回滾事務以清理數據
            await transaction.rollback()

            # 關閉 session
            await session.close()

pytestmark = pytest.mark.asyncio

async def test_database_connection(db_session):
    """測試資料庫連線是否成功"""
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

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
    # 提交由外部管理，因為我們在fixture中使用了session.begin()
    
    # 手動將資料重新載入（SQLite不會自動重整資料）
    await db_session.flush()
    
    # 驗證
    assert conversation.id is not None
    assert conversation.role == "user"
    assert conversation.content == "這是一條測試訊息"
    assert conversation.extra_metadata == {"source": "test"}

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
    
    # 從資料庫讀取
    stmt = text("SELECT * FROM conversations WHERE id = :id")
    result = await db_session.execute(stmt, {"id": conversation.id})
    row = result.fetchone()
    
    # 驗證
    assert row is not None
    assert row.id == conversation.id
    assert row.role == "assistant"
    assert row.content == "測試回應"
    # SQLite將JSON存為字串，需要解析
    assert json.loads(row.extra_metadata) == {"response_time": 0.5} 
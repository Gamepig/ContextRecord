import pytest
import pytest_asyncio
import asyncio
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src.models import Base
from src.main import app
import src.functions.conversations

# 使用檔案型SQLite進行測試
TEST_DB_FILE = "test_database.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}?check_same_thread=False"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session")
async def engine():
    """建立SQLite測試資料庫引擎"""
    # 確保每次測試前都是新的資料庫
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    test_engine = create_async_engine(
        TEST_DATABASE_URL, poolclass=NullPool, echo=True  # 啟用SQL日誌，幫助除錯
    )

    # 顯式創建所有表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    # 結束後清理表結構並關閉引擎
    await test_engine.dispose()

    # 清理測試文件
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


@pytest_asyncio.fixture
async def db_session(engine):
    """為每個測試提供獨立的資料庫會話"""
    # 使用測試引擎創建會話工廠
    session_factory = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=True
    )

    # 備份原始的會話工廠
    original_session_local = src.functions.conversations.SessionLocal

    # 覆蓋應用程式的會話工廠
    src.functions.conversations.SessionLocal = session_factory

    # 創建會話
    async with session_factory() as session:
        async with session.begin():
            # 提供會話給測試
            yield session
            # 測試結束後自動回滾

    # 恢復原始會話工廠
    src.functions.conversations.SessionLocal = original_session_local


@pytest.fixture
def client():
    """提供測試用FastAPI客戶端"""
    with TestClient(app) as test_client:
        yield test_client

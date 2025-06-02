import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text

from src.models import Base
from src.main import app

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture(scope="session")
async def engine():
    """建立內存SQLite測試資料庫引擎並創建所有表"""
    # 使用內存中的SQLite進行測試，避免PostgreSQL設定問題
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    # 創建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # 結束後清理表結構
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(engine):
    """為每個測試提供獨立的資料庫會話"""
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        # 創建一個事務以便在測試結束時能夠回滾
        async with session.begin():
            yield session
            # 測試結束時自動回滾

@pytest.fixture
def client():
    """提供測試用FastAPI客戶端"""
    return TestClient(app) 
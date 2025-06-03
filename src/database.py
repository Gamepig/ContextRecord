from sqlalchemy import text

# 從 sqlalchemy.ext.declarative 導入 declarative_base 已棄用，改用新的 2.0 API
from sqlalchemy.orm import declarative_base

# from sqlalchemy.orm import sessionmaker # 移除同步的 sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)  # 導入異步的引擎和 sessionmaker
import os

# 從環境變數讀取資料庫URL，預設使用SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

# 創建異步引擎
engine = create_async_engine(DATABASE_URL)

# 創建異步 SessionLocal
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

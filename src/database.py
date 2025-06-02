from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker # 移除同步的 sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker # 導入異步的引擎和 sessionmaker
import os

# 從環境變數讀取資料庫URL，預設使用SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

print(f"Database URL loaded: {DATABASE_URL.replace('password', '***')}") # 測試用，確認是否讀取到環境變數，隱藏密碼

# 創建異步引擎
engine = create_async_engine(DATABASE_URL)

# 創建異步 SessionLocal
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker # 移除同步的 sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker # 導入異步的引擎和 sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:54321/mydatabase") # 從環境變數讀取，提供預設值方便本地開發

print(f"Database URL loaded: {DATABASE_URL}") # 測試用，確認是否讀取到環境變數

# engine = create_engine(DATABASE_URL) # 移除同步引擎創建
engine = create_async_engine(DATABASE_URL) # 創建異步引擎

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 移除同步 SessionLocal
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine) # 創建異步 SessionLocal

Base = declarative_base() 
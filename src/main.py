import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .database import engine, Base, SessionLocal
from .functions.conversations import router as conversations_router
from .functions.server import router as server_router, register_conversation_tools

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # 在應用程式啟動時創建資料表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 註冊對話相關工具
    register_conversation_tools()
    
    yield
    # 在應用程式關閉時清理資源 (如果需要)

app = FastAPI(lifespan=lifespan)

# 註冊路由器
app.include_router(conversations_router, prefix="/api", tags=["conversations"])
app.include_router(server_router, prefix="/api", tags=["server"])

@app.get("/")
def read_root():
    return {"message": "Hello, World! - Development Mode with Hot Reload"}
 
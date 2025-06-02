from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
# 移除PostgreSQL專用類型，確保與SQLite兼容
# from sqlalchemy.dialects.postgresql import ARRAY

from src.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    extra_metadata = Column(JSON, nullable=True)
    
    # 注意：若未來切換到PostgreSQL並需要向量搜尋功能，可以添加以下註釋代碼
    # from pgvector.sqlalchemy import Vector
    # embedding = Column(Vector(1536), nullable=True) # 向量維度可能根據使用的嵌入模型而不同 
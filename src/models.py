from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import ARRAY # 如果需要儲存數組或其他PostgreSQL特定類型
# 如果需要 pgvector，需要安裝相關庫並導入 Vector 類型
# from pgvector.sqlalchemy import Vector

from src.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    role = Column(String)
    content = Column(String)
    extra_metadata = Column(JSON, nullable=True) # 將 metadata 改為 extra_metadata
    # embedding = Column(Vector(dim), nullable=True) # 如果整合 pgvector，dim 為向量維度 
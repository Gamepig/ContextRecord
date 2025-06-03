# 04_資料庫設定與ORM模型定義

## 目標
設定應用程式與SQLite資料庫的連線（開發/測試環境），同時考慮未來可能切換到PostgreSQL（生產環境），並定義對話紀錄的資料模型，為資料的持久化儲存做準備。

## 細化步驟

1.  [x] 決定資料庫選擇與連接方式。
    *   **開發/測試環境：** 使用SQLite，通過aiosqlite提供異步支援
    *   **生產環境（未來）：** 考慮切換到PostgreSQL，特別是需要向量搜尋功能時
2.  [x] 考慮如何安全地管理資料庫連接資訊。
    *   **推薦方式：** 使用環境變數。在開發環境中可以使用 `.env` 檔案，在 Docker 和 CI/CD 環境中則通過 Docker Secrets 或 GitHub Secrets 傳遞環境變數。
3.  [x] 在專案中建立資料庫連接的配置和初始化模組。
    *   在 `src/` 目錄下創建檔案 (例如 `database.py`)。
    *   在此檔案中，使用 SQLAlchemy 建立資料庫引擎 (Engine)。
        ```python
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from sqlalchemy.ext.declarative import declarative_base
        import os

        # 從環境變數讀取，開發/測試環境默認使用SQLite
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

        # 創建異步引擎
        engine = create_async_engine(DATABASE_URL)

        # 創建異步會話工廠
        SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

        Base = declarative_base()
        ```
    *   **重要：** 設計時考慮到未來可能從SQLite切換到PostgreSQL，確保代碼結構能夠適應不同的資料庫後端。
4.  [x] 定義對話紀錄的 ORM 模型。
    *   在 `src/` 目錄下創建檔案 (例如 `models.py`)。
    *   定義 `Conversation` 類別，繼承自 `Base`，並映射到 `conversations` 資料表。
        ```python
        from sqlalchemy import Column, Integer, String, DateTime, JSON
        from datetime import datetime
        from src.database import Base

        class Conversation(Base):
            __tablename__ = "conversations"

            id = Column(Integer, primary_key=True, index=True)
            timestamp = Column(DateTime, default=datetime.now)
            role = Column(String, nullable=False)
            content = Column(String, nullable=False)
            extra_metadata = Column(JSON, nullable=True)
            # 未來若需要向量搜尋功能，可以添加embedding欄位
        ```
5.  [x] 測試資料庫連接與 ORM 模型功能。
    *   **目標：** 驗證應用程式能否成功連接到資料庫，以及定義的 ORM 模型能否正確地進行數據的讀取和寫入。
    *   使用內存SQLite進行單元測試，編寫測試案例來驗證 ORM 模型映射到資料表的功能 (例如，創建、讀取、更新、刪除測試數據)。
    *   確保測試覆蓋對話紀錄模型 (`Conversation`) 的關鍵欄位。
    *   使用pytest-asyncio進行異步測試。

6.  [x] 撰寫資料庫初始化腳本。
    *   已在 `src/main.py` 中實現，在應用程式啟動時自動創建資料表：
        ```python
        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
            # 在應用程式啟動時創建資料表
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            yield
            # 在應用程式關閉時清理資源 (如果需要)

        app = FastAPI(lifespan=lifespan)
        ```
    *   對於生產環境或更複雜的系統，未來可以考慮使用Alembic等資料庫遷移工具來管理資料庫結構的變化。
    *   為未來可能的PostgreSQL遷移做好準備，當需要向量搜尋功能時，可以添加pgvector擴展的安裝和初始化：`CREATE EXTENSION IF NOT EXISTS vector;`（僅在使用PostgreSQL時需要）。 
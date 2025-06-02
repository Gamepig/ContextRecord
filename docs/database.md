# 資料庫連接、設定與 ORM 模型

## 檔案目的

紀錄與資料庫相關的所有細節，包括連接設定、使用的 ORM (例如 SQLAlchemy) 模型定義、以及資料庫操作的相關函數。

## 資料庫策略

### 資料庫選擇

本專案採用雙資料庫策略：
- **開發與測試環境：** 使用 SQLite 作為主要資料庫
- **生產環境 (未來)：** 計劃使用 PostgreSQL，特別是當需要向量搜尋功能時

### 為何選擇 SQLite 進行開發與測試

1. **簡化設置：** 不需要額外安裝和配置獨立的資料庫伺服器
2. **可移植性：** 跨平台支援，能在任何環境中輕鬆運行測試
3. **速度：** 使用內存模式（`:memory:`）時測試執行速度更快
4. **簡化 CI 流程：** 避免在 CI 環境中配置 PostgreSQL 伺服器
5. **無狀態測試：** 每次測試運行都使用全新資料庫，避免測試間互相干擾

### 遷移策略

將來從 SQLite 轉換到 PostgreSQL 時，我們通過以下措施確保平滑遷移：
- 使用 SQLAlchemy ORM 抽象層隔離具體資料庫實現
- 通過環境變數配置資料庫連接
- 使用 Alembic 或類似工具管理資料庫遷移

## 連接設定

### SQLite (開發與測試環境)

連接字串格式：
```
sqlite+aiosqlite:///:memory:  # 用於測試 (內存資料庫)
sqlite+aiosqlite:///app.db    # 用於開發 (檔案資料庫)
```

### PostgreSQL (未來生產環境)

連接字串格式：
```
postgresql+asyncpg://{username}:{password}@{hostname}:{port}/{database}
```

示例：
```
postgresql+asyncpg://user:password@localhost:5432/mydatabase
```

## ORM 模型定義

紀錄所有定義的 ORM 模型 (例如 SQLAlchemy 的 Declarative Base 定義)，包括：

- 每個模型的類別名稱
- 每個模型對應的資料表名稱
- 每個模型的欄位 (名稱、資料類型、約束條件如主鍵/外鍵/唯一等)
- 模型之間的關聯性 (一對一、一對多、多對多)

例如：

```python
# 示例：假設有一個 Conversation 模型
class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    extra_metadata = Column(JSON)
```

## 資料庫操作函數

紀錄用於資料庫 CRUD (創建、讀取、更新、刪除) 操作的函數，例如：

- `create_conversation(session, content, role, extra_metadata)`
- `get_conversation(session, conversation_id)`
- `get_all_conversations(session)`
- `update_conversation(session, conversation_id, new_content)`
- `delete_conversation(session, conversation_id)`

## 注意事項

- **異步支援：** 使用 SQLAlchemy 2.0+ 的異步功能，配合 `aiosqlite` 和 `asyncpg` 實現異步資料庫操作
- **資料庫遷移：** 未來可能使用 Alembic 管理資料庫結構變更
- **連接池管理：** 在生產環境中需要正確配置連接池大小和超時設定
- **向量搜尋：** 將來實現向量搜尋功能時，需將資料庫切換到 PostgreSQL 並安裝 pgvector 擴充
- **SQLite 限制：** 注意 SQLite 在併發寫入和某些 SQL 功能方面的限制，在生產環境可能不適用 
# 05_Tools Functions

## 目標
實作用於紀錄和搜尋對話內容的核心功能，作為 MCP Server 的基礎工具。

## 細化步驟

### 5.1 紀錄對話

1.  [ ] 在 `src/functions/` 目錄下創建處理對話相關 API 的模組 (例如 `conversations.py`)。
2.  [ ] 在 `conversations.py` 中，導入必要的 FastAPI 組件 (如 `APIRouter`, `Depends`) 和資料庫相關模組 (如 `src.database`, `src.models`)。
3.  [ ] 定義用於處理 POST 請求的 API 端點。
    *   使用 `@router.post("/conversations/")` 裝飾器。
    *   定義請求 body 的 Pydantic 模型，包含 `role` (str) 和 `content` (str)。可以考慮增加 `extra_metadata` (dict, 可選)。
    *   在 API 函數中，獲取資料庫會話 (Session)。可以使用 FastAPI 的依賴注入來管理會話生命週期。
    *   創建一個新的 `Conversation` 實例，將請求數據和自動生成的 `timestamp` 賦值給模型屬性。
    *   將新的 `Conversation` 實例添加到資料庫會話中。
    *   使用異步方式提交會話，將數據寫入資料庫：`await db_session.commit()`。
    *   刷新會話以獲取資料庫自動生成的 ID：`await db_session.refresh(conversation)`。
    *   返回創建成功的響應，包含新紀錄的 ID 和時間戳。
4.  [ ] 實作錯誤處理。
    *   處理資料庫寫入過程中可能出現的異常。
    *   返回適當的 HTTP 錯誤狀態碼 (例如 500 Internal Server Error)。
5.  [ ] **考慮細節：**
    *   時間戳如何生成？在應用程式端生成還是讓資料庫自動生成？
    *   `extra_metadata` 欄位如何設計和使用？
    *   如何驗證輸入數據？
    *   是否需要對 `content` 進行預處理 (例如清理 HTML 標籤)？

### 5.2 搜尋對話

1.  [ ] 在 `src/functions/conversations.py` (或新的搜尋模組) 中，定義處理 GET 請求的 API 端點。
    *   使用 `@router.get("/search/")` 裝飾器。
    *   定義接收搜尋查詢參數的方式。例如，使用查詢參數 `query: str`。
2.  [ ] 在 API 函數中，獲取資料庫會話。
3.  [ ] 根據接收到的 `query` 參數構建資料庫查詢。
    *   **基本搜尋：** 使用 SQLAlchemy 的 `filter()` 方法和 `like()` 或 `ilike()` (大小寫不敏感) 運算符來匹配 `content` 欄位。
        ```python
        from sqlalchemy import or_, text
        # ...
        results = await db_session.execute(
            select(Conversation).filter(
                or_(
                    Conversation.content.like(f"%{query}%"),
                    Conversation.role.like(f"%{query}%")
                    # 可以根據需要加入對其他欄位的搜尋
                )
            )
        )
        return results.scalars().all()
        ```
    *   **SQLite全文搜尋（未來可能遷移到PostgreSQL時使用更強大的功能）：**
        - 對於SQLite，可以使用基本的LIKE操作進行簡單搜尋
        - 對於未來可能的PostgreSQL遷移，在代碼中保留註釋說明如何使用PostgreSQL的全文搜尋功能
4.  [ ] 處理搜尋結果。
    *   將 SQLAlchemy 模型實例轉換為可序列化的格式 (例如 Pydantic 模型或字典)。
    *   實現分頁功能，避免一次返回大量結果。
    *   返回搜尋結果列表。
5.  [ ] 實作錯誤處理。
    *   處理資料庫查詢過程中可能出現的異常。
    *   返回適當的 HTTP 錯誤狀態碼。
6.  [ ] **考慮細節：**
    *   如何實現分頁和排序？
    *   搜尋結果的格式應該是什麼？
    *   如何處理沒有找到匹配結果的情況？
    *   未來如何整合向量搜尋 (當遷移到PostgreSQL時使用 `pgvector`)？需要定義新的 API 端點還是修改現有端點？需要哪些新的輸入參數 (例如向量嵌入)？

### 5.3 (未來) 整合向量搜尋

1.  [ ] 研究和選擇文字嵌入模型 (例如 Sentence-Transformers)。
2.  [ ] 確保應用程式架構設計支持未來從SQLite遷移到PostgreSQL。
3.  [ ] 設計API端點時考慮未來擴展性，允許未來添加向量搜尋功能。
4.  [ ] 當遷移到PostgreSQL時，啟用`pgvector`擴展並修改搜尋API以利用向量相似度搜尋功能。
5.  [ ] 未來可根據相似度排序並返回搜尋結果。

## 測試

在完成紀錄和搜尋對話功能後，需要為這些核心功能撰寫單元測試，以確保其正確性和穩定性。

1.  [ ] **紀錄對話功能單元測試：**
    *   測試 POST `/conversations/` 端點是否能成功接收數據並寫入資料庫。
    *   測試輸入數據的驗證 (例如，`role` 和 `content` 是否存在)。
    *   模擬資料庫錯誤，測試錯誤處理邏輯是否正確。
    *   驗證儲存到資料庫的數據是否與預期一致 (包括自動生成的時間戳和 ID)。

2.  [ ] **搜尋對話功能單元測試：**
    *   測試 GET `/search/` 端點是否能接收查詢參數。
    *   測試基本搜尋功能是否能正確地從資料庫中檢索匹配的對話記錄。
    *   測試大小寫不敏感搜尋 (如果實現了 `ilike`)。
    *   測試分頁邏輯是否正確工作。
    *   測試當沒有找到匹配結果時，API 是否返回空列表和正確的狀態碼。
    *   模擬資料庫錯誤，測試錯誤處理邏輯是否正確。

在編寫單元測試時，可以使用內存中的SQLite數據庫進行測試，這可以加快測試速度並簡化測試環境設置。 
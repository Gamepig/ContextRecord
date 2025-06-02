# Server-Sent Events (SSE) 實作

## 檔案目的

紀錄如何實作 Server-Sent Events (SSE) 來實現伺服器向客戶端推送即時更新的功能，特別是用於傳送 AI 回應的 Token 或處理進度。

## 關鍵函數/類別

- `sse_endpoint()`: 處理客戶端 SSE 連接的端點函數。
- `generate_sse_response()`: 產生符合 SSE 格式回應的生成器函數。
- `push_update_to_client(client_id, data)`: 向特定客戶端推送資料的函數。
- 用於管理客戶端連接的機制 (例如一個列表或字典)。

## 依賴項

列出此檔案直接依賴的其他模組或程式庫，特別是與 Web 框架 (FastAPI/Flask) 和非同步處理相關的庫。

## 使用/工作原理

簡要描述 SSE 如何設定、客戶端如何連接、以及伺服器如何產生和推送事件到連接的客戶端。 
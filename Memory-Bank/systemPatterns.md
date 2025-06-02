# 系統模式與設計決策 (System Patterns)

本檔案記錄專案的整體系統架構、重要的技術決策和採用的設計模式。

## 系統架構概述
專案採用客戶端-伺服器架構。後端是一個基於 Python FastAPI 的應用程式，負責處理 API 請求、與 PostgreSQL 資料庫互動以及通過 SSE 向客戶端推送即時更新。應用程式將被容器化並可使用 Docker Compose 在本地運行或部署到遠端伺服器。

```mermaid
graph LR
    Client[客戶端]
    subgraph Backend[後端 MCP Server (FastAPI)]
        API_Layer(API 端點)
        SSE_Handler(SSE 連接處理)
        Tool_Calling(工具呼叫邏輯)
        DB_Interaction(資料庫互動)
    end
    Database[PostgreSQL 資料庫]

    Client -- HTTP Request/Response --> API_Layer
    Client -- SSE Connection --> SSE_Handler
    API_Layer -- DB Operations --> DB_Interaction
    DB_Interaction -- 資料儲存/讀取 --> Database
    Tool_Calling -- 觸發工具 --> External_Tools[外部工具]
    DB_Interaction -- 數據變動事件 --> SSE_Handler
    SSE_Handler -- Push Updates --> Client
```

## 技術決策
- **後端框架：** 選擇 FastAPI 是因為其高性能、易於使用、自動生成 API 文件以及對異步操作的良好支援。
- **資料庫：** 選擇 PostgreSQL 是因為其穩定性、擴展性以及對結構化數據和未來 pgvector 擴充功能的支援，適合用於儲存對話紀錄和進行向量搜尋。
- **即時通訊：** 選擇 Server-Sent Events (SSE) 作為伺服器到客戶端的單向即時通訊方式，相對 WebSocket 更簡單，且符合伺服器主動推送更新的需求。
- **容器化：** 採用 Docker 和 Docker Compose，提供標準化的開發、測試和部署環境，解決環境依賴問題。
- **依賴管理：** 使用 UV 進行 Python 依賴管理，以提升速度和可靠性。
- **CI/CD：** 使用 GitHub Actions 實現自動化的程式碼檢查、測試、映像檔建置與推送，提高開發效率和程式碼品質。

## 設計模式與考量
- **API 設計：** 遵循 RESTful 原則來設計主要的對話紀錄和搜尋 API。
- **依賴注入：** 利用 FastAPI 的依賴注入系統來管理資料庫會話等資源。
- **環境變數：** 使用環境變數來管理敏感資訊 (如資料庫憑證) 和配置設定，增強安全性。
- **非同步操作：** 利用 Python 的 `asyncio` 和 FastAPI 的異步特性來處理 I/O 密集型操作，提高應用程式的響應性。
- **資料庫 ORM：** 使用 SQLAlchemy 作為 ORM 工具，提供更高層次的資料庫互動抽象。
- **未來擴展：** 在設計時考慮到未來整合 pgvector 進行向量搜尋的可能性，相關模型和查詢預留了擴展點。 
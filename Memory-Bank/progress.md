# 專案進度 (Progress)

本檔案追蹤專案的整體進度，記錄已完成、正在進行和待完成的工作項目。

## 已完成事項
- 專案目標、技術棧和高層次架構的確定。
- 資料庫類型選擇：
  - 初期/測試環境：SQLite（使用aiosqlite提供異步支援）
  - 未來生產環境：PostgreSQL（特別是需要向量搜尋功能時）
- 專案計劃 (`mcp_server_plan.md`) 的制定，包括 Git/GitHub 和 CI/CD 規劃。
- 將主要開發步驟細化為獨立的任務檔案 (`Task/01_` 到 `Task/10_`)。
- 創建了專案記憶庫的目錄 (`Memory-Bank/`)。
- 建立了 Memory Bank 中的 `projectbrief.md`, `productContext.md`, `memory_bank_instructions.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md` 檔案。
- 在 `Task/04_資料庫設定與ORM模型定義.md` 中加入了資料庫連接和 ORM 模型功能的測試步驟說明。
- 成功實現基本的 ORM 模型和測試環境設置（使用內存中的 SQLite）。
- 設置並修復 GitHub Actions CI 流程，確保測試可在無外部依賴環境中運行。
- 更新 `.gitignore` 檔案，確保所有敏感資訊和不必要的檔案都被排除。
- 實現資料庫初始化腳本，於應用程式啟動時自動創建資料表。
- 實現對話紀錄和搜尋API功能，包括：
  - 建立對話記錄API端點 (`POST /api/conversations/`)
  - 實現搜尋功能API端點 (`GET /api/search/`)
  - 獲取對話列表API端點 (`GET /api/conversations/`)
  - 根據ID獲取單個對話API端點 (`GET /api/conversations/{conversation_id}`)
  - 完善的錯誤處理和輸入驗證
  - 使用Pydantic模型進行請求和響應的序列化
  - 實現分頁功能
- 實現MCP Server核心功能，包括：
  - 使用FastAPI的StreamingResponse實現SSE連接功能
  - 創建管理客戶端連接的事件管理器
  - 實現向所有連接客戶端廣播事件的機制
  - 設計並實現工具呼叫的概念架構，包括工具註冊和呼叫API
  - 完善API文檔，添加SSE和工具呼叫相關端點的描述
  - 撰寫單元測試確保功能正確性
- 完成所有測試單元，包括：
  - 對話功能測試（創建、獲取、搜尋）
  - 資料庫連接測試
  - 主應用程式端點測試
  - 伺服器功能測試（工具註冊和調用）
  - 解決測試中的各種環境問題
  - 修復SQLite資料庫測試問題，從內存數據庫改為檔案型數據庫確保表結構正確創建

## 正在進行事項
- 考慮未來向量搜尋功能的實現方案，為遷移至PostgreSQL做準備。

## 待完成事項
- 根據 `Task/` 目錄中的細化步驟，逐步進行程式碼實作：
    - 設定專案環境與基本架構 (`Task/01_`) - ✅
    - 初始化 Git 倉庫並推送到 GitHub (`Task/02_`) - ✅ 
    - 設定 GitHub Actions CI 工作流程 (`Task/03_`) - ✅
    - 實作資料庫連接與 ORM 模型定義 (`Task/04_`) - ✅
    - 實作 Tools Functions (紀錄與搜尋 API) (`Task/05_`) - ✅
    - 實作 MCP Server 核心功能 (SSE 連接與工具呼叫概念) (`Task/06_`) - ✅
    - 撰寫單元測試和整合測試 (`Task/07_`) - ✅
    - 設定 GitHub Actions CD 工作流程 (`Task/08_`) - ✅
    - Docker 化應用程式 (`Task/09_`) - ✅
    - 撰寫專案文件 (`Task/10_`) - 部分完成 ✅
- 實施和驗證 CI/CD 工作流程。
- 建立詳細的API文檔，將所有API端點以JSON格式記錄，包括：
  - 端點路徑
  - HTTP方法
  - 請求參數和格式
  - 響應格式和狀態碼
  - 錯誤處理方式
  - 示例請求和響應
- (未來) 整合 pgvector 進行向量搜尋。
- (未來) 實作更完整的工具呼叫機制。 
- (未來) 實作自動部署到雲端平台的功能，可能包括 AWS ECS、Google Cloud Run 或 Azure Container Instances。 
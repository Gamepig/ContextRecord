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
- 建立了 Memory Bank 中的 `projectbrief.md`, `productContext.md`, `memory_bank_instructions.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md` 檔案。
- 在 `Task/04_PostgreSQL資料庫設定與ORM模型定義.md` 中加入了資料庫連接和 ORM 模型功能的測試步驟說明。
- 成功實現基本的 ORM 模型和測試環境設置（使用內存中的 SQLite）。
- 設置並修復 GitHub Actions CI 流程，確保測試可在無外部依賴環境中運行。

## 正在進行事項
- 建立 Memory Bank 中剩餘的核心檔案 (`progress.md` - 本檔案)。
- 檢查所有 `Task/` 檔案，確保包含單元測試和實際操作測試步驟。

## 待完成事項
- 根據 `Task/` 目錄中的細化步驟，逐步進行程式碼實作：
    - 設定專案環境與基本架構 (`Task/01_`) - ✅
    - 初始化 Git 倉庫並推送到 GitHub (`Task/02_`) - ✅ 
    - 設定 GitHub Actions CI 工作流程 (`Task/03_`) - ✅
    - 實作資料庫連接與 ORM 模型定義 (`Task/04_`) - ✅
    - 實作 Tools Functions (紀錄與搜尋 API) (`Task/05_`)。
    - 實作 MCP Server 核心功能 (SSE 連接與工具呼叫概念) (`Task/06_`)。
    - 撰寫單元測試和整合測試 (`Task/07_`) - 部分完成 ✅
    - 設定 GitHub Actions CD 工作流程 (`Task/08_`)。
    - Docker 化應用程式 (`Task/09_`)。
    - 撰寫專案文件 (`Task/10_`) - 部分完成 ✅
- 根據需要更新和完善 Memory Bank 中的所有檔案。
- 實施和驗證 CI/CD 工作流程。
- (未來) 整合 pgvector 進行向量搜尋。
- (未來) 實作更完整的工具呼叫機制。 
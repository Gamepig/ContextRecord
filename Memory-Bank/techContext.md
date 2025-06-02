# 技術情境 (Tech Context)

本檔案詳細記錄專案所使用的具體技術、開發環境設定要求以及已知的技術約束。

## 使用的技術棧與版本
- **程式語言：** Python 3.9+ (建議使用與 CI 中設定的版本一致)
- **Web 框架：** FastAPI (最新穩定版)
- **非同步套件：** asyncio (Python 標準庫)
- **資料庫：** PostgreSQL 13+ (與 Docker Compose 中設定的版本一致)
- **資料庫驅動：** asyncpg (推薦用於異步操作) 或 psycopg2-binary
- **ORM 工具：** SQLAlchemy 1.4+ 或 2.0+ (建議使用最新版本)
- **依賴管理：** UV (最新版本)
- **容器化：** Docker Engine, Docker Compose
- **版本控制：** Git
- **CI/CD：** GitHub Actions
- **測試框架：** pytest, pytest-asyncio
- **程式碼檢查/格式化：** flake8, black
- **向量搜尋 (未來)：** pgvector (PostgreSQL 擴充功能), Sentence-Transformers 或其他嵌入模型相關套件

## 開發環境設定要求
- 安裝 Python 3.9 或更高版本。
- 安裝 UV (詳細安裝指南請參考 UV 官方文件)。
- 安裝 Docker Engine 和 Docker Compose。
- 安裝 Git 客戶端。
- (可選) 安裝支援 PostgreSQL 的資料庫管理工具 (如 DBeaver, pgAdmin)。

## 本地開發環境啟動步驟 (使用 Docker Compose)
1.  複製專案倉庫：`git clone <repository_url>`
2.  切換到專案目錄：`cd ContextRecord`
3.  (如果沒有 `.env` 檔案，請根據 `.env.example` 創建並填寫資料庫憑證等資訊，確保 `.gitignore` 忽略 `.env`)。
4.  啟動 Docker Compose 服務 (包括應用程式和資料庫)：`docker compose up --build -d`
5.  (如果需要手動初始化資料庫或運行遷移，請執行相應腳本或命令)。
6.  應用程式應可在 `http://localhost:8000` 訪問。

## 技術約束與注意事項
- SSE 連接是單向的 (伺服器到客戶端)。如果需要雙向通訊，未來可能需要考慮 WebSocket。
- 在本地開發環境中，資料庫憑證儲存在 `.env` 或 Docker Compose 檔案中，生產環境應使用更安全的 Secrets 管理機制 (例如 GitHub Secrets, Docker Secrets, Kubernetes Secrets)。
- 向量搜尋功能 (`pgvector`) 需要資料庫伺服器安裝並啟用相應的擴充功能。
- 初步版本的工具呼叫邏輯將是概念性的，實際整合外部工具需要進一步設計和實作。
- 應注意處理大量對話數據時的性能問題，可能需要資料庫索引優化、查詢優化或數據歸檔策略。

## 背景運行 FastAPI 應用

**需求：** 在關閉終端機後，API 程式應能繼續在背景運行，直到手動停止。

**解決方案：** 在 macOS/Linux 環境下，可以使用 `nohup` 指令將程式放入背景執行並忽略掛斷信號（SIGHUP）。

**啟動指令範例 (待完成 APP 後使用)：**
```bash
nohup uvicorn src.main:app --reload > app.log 2>&1 &
```

**停止方法：** 需要找到對應的行程 ID (PID)，然後使用 `kill <PID>` 指令終止。

**備註：** `--reload` 旗標在生產環境中通常不需要，屆時應移除。生產環境的部署方式可能與此不同（例如使用 Gunicorn 配合 Supervisor 或 Docker）。 
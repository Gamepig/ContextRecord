# 簡易 MCP Server 開發主要步驟 (細化)

根據專案規劃書與您的要求，以下是更詳細的開發步驟順序：

1.  **專案環境與基本架構設定**
    *   使用 UV 建立 Python 虛擬環境。
    *   安裝 FastAPI、uvicorn (ASGI 伺服器)。
    *   安裝 PostgreSQL 資料庫驅動 (psycopg2 或 asyncpg)。
    *   安裝 ORM (SQLAlchemy)。
    *   安裝處理 SSE 的套件 (如果 FastAPI 內建支援則不需要額外安裝，但需要了解如何使用)。
    *   建立專案所需的基礎目錄結構（如 `app/`, `app/db/`, `app/api/`, `app/core/`, `docker/`, `.github/workflows/` 等）。

2.  **初始化 Git 倉庫並推送到 GitHub**
    *   在專案根目錄初始化 Git 倉庫 (`git init`)。
    *   建立 `.gitignore` 檔案，忽略 `.venv/`, `__pycache__/`, `.env`, Docker volumes 等。
    *   將當前檔案（`mcp_server_plan.md`, `Task/development_steps.md`）及基礎結構檔案加入並進行首次提交。
    *   在 GitHub 上建立遠端倉庫。
    *   將本地倉庫與遠端倉庫關聯 (`git remote add origin ...`)。
    *   將本地程式碼推送到 GitHub (`git push -u origin main`)。

3.  **設定 GitHub Actions 的 CI 工作流程**
    *   在 `.github/workflows/` 目錄下建立 CI 工作流程檔案 (例如 `ci.yml`)。
    *   設定工作流程在 `push` 到 `main` 分支及針對 `main` 的 `pull_request` 時觸發。
    *   定義 CI Job：
        *   Checkout 程式碼。
        *   設定 Python 環境。
        *   使用 UV 安裝依賴 (`uv install -r requirements.txt`)。
        *   運行 Linting 和格式化檢查 (例如 `flake8`, `black --check`)。
        *   運行單元測試 (待撰寫)。
    *   確保每次提交都能通過自動化檢查。

4.  **PostgreSQL 資料庫設定與 ORM 模型定義**
    *   **使用現有 Docker 容器內的 PostgreSQL 資料庫。連接資訊：`host="localhost"`, `port="54321"`, `dbname="mydatabase"`, `user="user"`, `password="<您的密碼>"`。**
    *   在 `app/db/` 目錄下，設定資料庫連線（例如使用 SQLAlchemy 的 Engine）。考慮使用環境變數來管理連接資訊。
    *   定義對話紀錄的 ORM 模型 (`Conversation` class)，對應到 `conversations` 表，包含 `id`, `timestamp`, `role`, `content`, `metadata`, `embedding` 欄位。
    *   撰寫資料庫初始化腳本，用於創建 `conversations` 表 (如果不存在) 並啟用 `pgvector` 擴充 (如果需要向量搜尋)。

5.  **Tools Functions**

    5.1 **紀錄對話**
        *   在 `app/api/` 目錄下，建立處理對話相關 API 的模組。
        *   定義 `POST /conversations/` API 端點，接收包含 `role` 和 `content` 的對話資料。
        *   在 API 處理函數中，使用 ORM 將接收到的對話資料儲存到資料庫的 `conversations` 表中。
        *   **考慮細節：** 如何處理 `timestamp`, `metadata` 的生成或接收？如何返回成功或失敗狀態？

    5.2 **搜尋對話**
        *   在同一 API 模組中，定義 `GET /search/` API 端點。
        *   接收搜尋查詢參數 (例如 `query` 字符串)。
        *   在 API 處理函數中，使用 ORM 或直接 SQL 根據 `query` 在 `content` 欄位中進行搜尋。
        *   **考慮細節：** 使用基本的 `LIKE` 查詢還是全文搜尋？如何處理搜尋結果的分頁？如何格式化返回結果？未來如何擴展到向量搜尋？

6.  **MCP Server**

    6.1 **連接功能 (SSE)**
        *   在 `app/api/` 或獨立模組中，建立處理 SSE 連線的端點 (例如 `GET /events/`)。
        *   實現邏輯來管理所有連接的客戶端。
        *   需要一個機制讓 API (例如儲存對話的 API) 能夠通知 SSE 處理邏輯，以便向客戶端推送新事件（例如「有新的對話紀錄」）。這可能需要一個中間層，如一個非同步佇列或事件匯流排。
        *   **考慮細節：** 如何處理客戶端斷開連線？推送的 SSE 訊息格式？推送哪些類型的事件？

    6.2 **工具呼叫 (概念性)**
        *   這部分在簡易版中可以先規劃。MCP 的核心之一是工具呼叫。
        *   需要一個機制來接收外部的工具呼叫請求。
        *   需要一個分派器，根據請求識別要呼叫哪個內部或外部工具。
        *   需要處理工具的輸入和輸出。
        *   **考慮細節：** 工具呼叫的請求格式？如何將工具執行結果返回？這部分是否與 SSE 連接功能相關聯？

7.  **撰寫測試**
    *   為核心功能（如對話儲存、基本搜尋）撰寫單元測試和整合測試。
    *   測試資料庫互動是否正確。
    *   測試 API 端點是否按預期工作。

8.  **撰寫 Dockerfile 和 docker-compose.yml**
    *   撰寫 Python 應用程式的 Dockerfile，包含基礎映像、複製程式碼、安裝依賴 (從 `requirements.txt`)、暴露端口、啟動命令 (運行 uvicorn)。
    *   撰寫 `docker-compose.yml`：
        *   定義 `app` 服務，使用上面建立的 Dockerfile，映射端口，掛載代碼卷 (方便開發)。
        *   定義 `db` 服務，使用 PostgreSQL 官方映像，設定數據卷，設定數據庫、使用者、密碼等環境變數。
        *   設定網絡，確保 `app` 服務可以通過服務名稱連接到 `db` 服務。
        *   **重要：** 在 `docker-compose.yml` 中使用您的 PostgreSQL 連接資訊（端口、數據庫、使用者、密碼），並考慮使用 `.env` 文件來管理這些敏感資訊。

9.  **設定 GitHub Actions 的 CD 工作流程 (可先規劃，後續實作)**
    *   在 `.github/workflows/` 目錄下建立 CD 工作流程檔案 (例如 `cd.yml`)。
    *   設定工作流程在 CI 成功且 `push` 到 `main` 分支時觸發。
    *   定義 CD Job：
        *   Checkout 程式碼。
        *   登入 Docker Registry (使用 GitHub Secrets)。
        *   建置並標記 Docker 映像 (使用 commit hash 或版本號)。
        *   推送 Docker 映像到 Registry。
        *   (進階) 增加自動化部署到目標環境的步驟。 
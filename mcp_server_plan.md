# 簡易 MCP Server 專案規劃書

## 專案目標

建立一個基於 Python 的伺服器，能夠紀錄開發過程中的對話內容，並提供AI搜尋功能，以便快速查找相關資訊。伺服器使用 Server-Sent Events (SSE) 與客戶端通訊，並透過 Docker 進行容器化部署。資料庫選擇 PostgreSQL，考量其穩定性及對未來AI搜尋功能（如向量搜尋）的良好支援。

## 選定技術棧

*   **核心語言：** Python
*   **資料庫：** PostgreSQL (含 `pgvector` 擴充功能的考量)
*   **Web 框架：** 考慮使用 FastAPI (考量其高效能和非同步支援) 或 Flask (考量其輕量和靈活性)。建議使用 FastAPI。
*   **通訊協定：** Server-Sent Events (SSE)
*   **容器化：** Docker 與 Docker Compose

## 架構概覽

*   **Python 後端：** 處理 API 請求（儲存對話、搜尋對話）、與資料庫互動、管理 SSE 連線並推送更新。
*   **PostgreSQL 資料庫：** 持久化儲存對話資料。
*   **SSE 連線：** 提供客戶端實時接收對話更新或其他通知。
*   **Docker 容器：** 將 Python 後端和 PostgreSQL 資料庫各自封裝在獨立的容器中，方便部署和管理。

## 資料庫設計 (概念性)

設計一個簡單的資料表來儲存對話紀錄。例如：

*   `conversations` 表：
    *   `id` (Primary Key, Integer): 唯一的對話 ID。
    *   `timestamp` (Datetime): 對話發生的時間戳。
    *   `role` (Text): 對話的角色 (例如 'user', 'assistant', 'system')。
    *   `content` (Text): 對話的實際文字內容。
    *   `metadata` (JSONB, Optional): 可選的 JSON 欄位，用於儲存額外的結構化資訊（例如來源、相關檔案等）。
    *   `embedding` (Vector, Optional): 未來用於儲存對話內容的向量嵌入，以支援向量搜尋 (需要 `pgvector`)。

## 後端開發計畫

1.  **環境建置：**
    *   使用 UV 建立 Python 虛擬環境。
    *   安裝 FastAPI/Flask, 資料庫驅動 (如 `psycopg2`), ORM (如 SQLAlchemy), 以及其他必要套件。
2.  **專案結構：**
    *   建立清晰的專案目錄結構 (例如 `app/`, `database/`, `docker/` 等)。
3.  **資料庫整合：**
    *   設定資料庫連線。
    *   使用 ORM 定義資料模型 (`conversations` 表)。
    *   建立資料庫初始化腳本或遷移工具。
4.  **API 實作：**
    *   **POST `/conversations`：** 接收並儲存新的對話紀錄。
    *   **GET `/conversations`：** 獲取對話紀錄 (可選支援過濾、分頁)。
    *   **GET `/search`：** 根據關鍵字或查詢語句在 `content` 欄位中進行搜尋。初期可使用基本的 SQL `LIKE` 或全文搜尋，未來升級為基於 `embedding` 的向量搜尋。
5.  **SSE 實作：**
    *   **GET `/events`：** 建立 SSE 連線，用於向客戶端推送新對話紀錄的通知或搜尋結果的更新。
6.  **AI 搜尋策略 (未來擴展)：**
    *   研究並整合文字嵌入模型 (例如 Sentence-Transformers)。
    *   修改儲存對話的 API，在儲存時計算 `content` 的向量嵌入，並儲存在 `embedding` 欄位。
    *   修改搜尋 API，接收使用者查詢，計算查詢的向量嵌入，並使用 `pgvector` 的向量相似度搜尋功能查找相似的對話紀錄。

## SSE 連接方式

*   客戶端通過 HTTP GET 請求連線到後端的 `/events` 端點。
*   後端保持連線開啟，當有新對話紀錄儲存或搜尋完成時，格式化為 SSE 訊息 (`data: ...\n\n`) 通過該連線推送給客戶端。

## Docker 化計畫

1.  **`docker/Dockerfile` (for Python App):**
    *   選擇一個 Python 基礎映像。
    *   複製應用程式碼。
    *   安裝依賴 (使用 `uv install -r requirements.txt`)。
    *   暴露應用程式監聽的端口。
    *   定義啟動命令。
2.  **`docker/docker-compose.yml`：**
    *   定義 `app` 服務，使用上面建立的 Dockerfile。
    *   定義 `db` 服務，使用 PostgreSQL 官方映像，設定數據卷以持久化資料，設定環境變數（數據庫名稱、使用者、密碼）。
    *   設定網絡，讓 `app` 服務可以連線到 `db` 服務。

## 測試計畫

*   **單元測試：** 測試後端函數的邏輯，例如資料庫操作函數、SSE 訊息格式化等。
*   **整合測試：** 測試 API 端點的功能，例如儲存對話、基本搜尋是否按預期工作。
*   **Docker 測試：** 確保 Docker Compose 設定能夠正確啟動並連線應用程式和資料庫容器。

## 版本控制與 Git/GitHub 整合計畫

1.  **初始化 Git 倉庫：** 在專案根目錄下初始化一個新的 Git 倉庫。
    *   執行命令：`git init`
2.  **建立 `.gitignore` 檔案：**
    *   建立 `.gitignore` 檔案來忽略不應提交到版本控制中的文件和目錄，例如 Python 虛擬環境目錄 (`.venv` 或 `venv`)、快取文件 (`__pycache__`)、資料庫文件 (如果是 SQLite 且在專案目錄內)、`.env` 環境變數文件、Docker 生成的卷等。
    *   建議包含 Python 和 Docker 常用的忽略規則。
3.  **首次提交：**
    *   將所有初始專案文件加入暫存區：`git add .`
    *   執行首次提交：`git commit -m "Initial project setup"`
4.  **在 GitHub 建立新的遠端倉庫：**
    *   手動在 GitHub 網站上建立一個新的空倉庫 (不要初始化 README 或 `.gitignore`)。
    *   複製該倉庫的 HTTPS 或 SSH 遠端 URL。
5.  **添加遠端倉庫：**
    *   將本地倉庫與 GitHub 上的遠端倉庫關聯：`git remote add origin [遠端倉庫URL]`
6.  **推送到 GitHub：**
    *   將本地的主分支推送到遠端倉庫：`git push -u origin main` (或者您的主分支名稱，如 `master`)

## CI/CD (持續整合/持續部署) 計畫

為了自動化建置、測試和部署流程，我們將導入 CI/CD。考量到專案使用 GitHub 進行版本控制，我們選擇使用 **GitHub Actions** 作為 CI/CD 工具。

1.  **選擇 CI/CD 工具：** GitHub Actions。
2.  **工作流程定義：**
    *   建立一個或多個工作流程檔案 (`.github/workflows/*.yml`) 在專案根目錄下。
3.  **CI (持續整合) 工作流程：**
    *   **觸發條件：** 設定工作流程在每次 `push` 到 `main` 分支或創建 `pull_request` 目標為 `main` 分支時觸發。
    *   **步驟 (Job):**
        *   **Checkout 程式碼：** 從倉庫中獲取最新的程式碼。
        *   **設定 Python 環境：** 設定指定版本的 Python 環境。
        *   **安裝依賴：** 使用 `uv` 安裝 `requirements.txt` 中定義的所有套件。
        *   **執行 Linting 和格式化檢查：** 運行程式碼風格檢查工具 (如 Flake8, Black --check) 確保程式碼符合規範。
        *   **執行單元測試和整合測試：** 運行專案中的測試套件，確保程式碼功能正確。
        *   **建置 Docker 映像 (可選但推薦)：** 嘗試建置應用程式的 Docker 映像，以確保 Dockerfile 的有效性。
    *   **目標：** 確保提交的程式碼在合併到主分支前是穩定且符合品質標準的。
4.  **CD (持續部署/交付) 工作流程：**
    *   **觸發條件：** 設定此工作流程在 CI 工作流程成功完成後，並且當程式碼 `push` 到 `main` 分支時觸發。
    *   **步驟 (Job):**
        *   **Checkout 程式碼：** 獲取最新的程式碼。
        *   **登入 Docker Registry：** 使用安全憑證登入到 Docker Hub 或私有的 Docker Registry (需要在 GitHub Secrets 中設定)。
        *   **建置並標記 Docker 映像：** 建置應用程式的 Docker 映像，並使用有意義的標籤 (例如 `latest` 或 commit hash)。
        *   **推送 Docker 映像：** 將建置好的 Docker 映像推送到 Registry。
        *   **部署 (進階且可選)：** 根據部署環境的不同，執行部署腳本。例如：
            *   SSH 連線到伺服器並執行 `docker compose pull` 和 `docker compose up -d`。
            *   更新 Kubernetes Deployment。
            *   部署到雲端服務平台 (如 Heroku, AWS ECS/EKS, Google Cloud Run 等)。
    *   **目標：** 自動化將驗證過的程式碼部署到指定的環境。

## 後續步驟 (建議優先順序)

1.  專案環境與基本架構設定 (包含 UV 虛擬環境、基礎檔案結構、安裝套件)
2.  初始化 Git 倉庫並推送到 GitHub
3.  設定 GitHub Actions 的 CI 工作流程
4.  PostgreSQL 資料庫設定與 ORM 模型定義
5.  實作儲存對話的 API 端點
6.  實作基本的搜尋 API 端點
7.  實作 SSE 連線和推送功能
8.  撰寫 Dockerfile 和 docker-compose.yml
9.  設定 GitHub Actions 的 CD 工作流程 (可先規劃，後續實作) 
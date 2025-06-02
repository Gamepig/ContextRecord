# 09_Docker 化應用程式

## 目標
將應用程式容器化，以便在不同環境中一致地建置、運行和部署，同時設定 Docker Compose 來簡化本地開發環境的管理。根據需要，可以配置SQLite（開發/測試）或PostgreSQL（生產）作為資料庫。

## 細化步驟

1.  [ ] 在專案根目錄下創建 Dockerfile。
    *   檔案路徑：`./Dockerfile`
    *   選擇一個適合的 Python 基礎映像檔 (例如 `python:3.9-slim-buster` 或 `python:3.10-slim`)。
        ```dockerfile
        FROM python:3.9-slim
        ```
    *   設定工作目錄。
        ```dockerfile
        WORKDIR /app
        ```
    *   將 `requirements.txt` 複製到工作目錄。
        ```dockerfile
        COPY requirements.txt .
        ```
    *   使用 UV 安裝依賴。
        ```dockerfile
        RUN uv install -r requirements.txt
        ```
    *   將應用程式程式碼複製到工作目錄。
        ```dockerfile
        COPY ./src /app/src
        COPY ./main.py /app/ # 假設 main.py 在根目錄
        # 根據您的專案結構和進入點位置調整上述 COPY 指令
        ```
    *   創建資料目錄（如果使用SQLite檔案資料庫）
        ```dockerfile
        RUN mkdir -p /app/data
        ```
    *   暴露應用程式運行的埠 (例如 8000)。
        ```dockerfile
        EXPOSE 8000
        ```
    *   定義容器啟動時執行的命令 (使用 uvicorn 運行 FastAPI 應用)。
        ```dockerfile
        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        # 根據您的進入點檔案和 FastAPI 實例名稱調整
        ```
    *   **考慮細節：** 使用多階段建置來減小映像檔大小？處理環境變數？

2.  [ ] 在專案根目錄下創建 Docker Compose 檔案，支援多種資料庫配置。
    *   檔案路徑：`./docker-compose.yml`
    *   定義應用程式服務。
        *   指定建置上下文 (`build: .`) 或直接使用預建的映像檔 (`image: ...`)。
        *   映射埠 (`ports:`)。
        *   掛載 Volumes (用於本地開發時程式碼變動自動重載或持久化數據卷) (`volumes:`)。
        *   設定環境變數 (`environment:`)，包括資料庫選擇和連接資訊。
    *   根據環境需求定義資料庫服務，提供兩種配置選項：
        
        **配置1：SQLite (開發/測試)**
        ```yaml
        version: '3.8'

        services:
          app:
            build:
              context: .
            ports:
              - "8000:8000"
            volumes:
              - ./src:/app/src # 掛載 src 目錄下的程式碼，方便開發時熱重載
              - ./main.py:/app/main.py # 如果 main.py 在根目錄，則掛載它
              - ./data:/app/data # 掛載數據目錄，用於持久化SQLite資料庫
            environment:
              DATABASE_URL: sqlite+aiosqlite:///data/app.db # 使用檔案SQLite資料庫
        ```
        
        **配置2：PostgreSQL (生產或需要向量搜尋功能時)**
        ```yaml
        version: '3.8'

        services:
          app:
            build:
              context: .
            ports:
              - "8000:8000"
            volumes:
              - ./src:/app/src
              - ./main.py:/app/main.py
            environment:
              DATABASE_URL: postgresql+asyncpg://user:password@db:5432/mydatabase
            depends_on:
              - db

          db:
            image: postgres:13-alpine
            environment:
              POSTGRES_DB: mydatabase
              POSTGRES_USER: user
              POSTGRES_PASSWORD: password # 開發環境使用，生產環境應使用 Secrets
            ports:
              - "54321:5432" # 將容器的 5432 映射到主機的 54321
            volumes:
              - postgres_data:/var/lib/postgresql/data/
        
        volumes:
          postgres_data:
        ```
    
    *   為了簡化配置選擇，考慮使用多個compose檔案或環境變數來控制使用哪種資料庫。

3.  [ ] 建置 Docker 映像檔 (本地測試)。
    *   執行命令：`docker build -t mcp_server .`
4.  [ ] 使用 Docker Compose 啟動服務 (本地開發)。
    *   **使用SQLite：** `docker-compose -f docker-compose.sqlite.yml up --build`
    *   **使用PostgreSQL：** `docker-compose -f docker-compose.postgres.yml up --build`
    *   或使用環境變數來控制：`DB_TYPE=sqlite docker-compose up --build`
5.  [ ] 驗證 Docker 容器是否成功運行且應用程式可訪問。
    *   檢查容器日誌：`docker logs <容器名稱>`
    *   測試 API 端點。

6.  [ ] 更新 `.gitignore` 檔案，忽略 Docker 可能產生的文件或目錄。
    *   確保 `.env` 文件和本地SQLite數據庫文件 (`data/*.db`) 被忽略。 
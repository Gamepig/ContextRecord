# Dockerfile 與 Docker Compose

## 檔案目的

紀錄如何使用 Dockerfile 定義應用程式的建置流程，以及如何使用 docker-compose.yml 定義服務的運行環境和依賴關係。

## Dockerfile

紀錄 Dockerfile 的內容，包括：

- 使用的基礎映像檔 (`FROM`)
- 設定工作目錄 (`WORKDIR`)
- 複製應用程式檔案 (`COPY`)
- 安裝依賴項 (`RUN pip install ...`)
- 暴露的埠號 (`EXPOSE`)
- 定義啟動命令 (`CMD` 或 `ENTRYPOINT`)
- 其他必要的環境設定或使用者設定

```dockerfile
# 示例 Dockerfile 內容
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## docker-compose.yml

紀錄 docker-compose.yml 的內容，包括：

- 定義的服務 (例如 `app`, `database`)
- 每個服務使用的映像檔 (`image` 或 `build`)
- 服務之間的連接 (`depends_on`)
- 埠號映射 (`ports`)
- 卷宗映射 (`volumes`)
- 環境變數 (`environment`)
- 資料庫服務的設定 (如果資料庫也在 Docker Compose 中運行)

```yaml
# 示例 docker-compose.yml 內容
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:<password>@db:5432/mydatabase # 請使用實際連接字串和 Secrets
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: user
      POSTGRES_PASSWORD: <password> # 請使用 Secrets
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  pg_data:
```

## 使用/工作原理

簡要描述如何使用 `docker build` 和 `docker compose up` 命令來建置和運行應用程式及其依賴服務。 
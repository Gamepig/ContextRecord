# ContextRecord 部署指南

本文檔提供 ContextRecord 應用程式的部署說明，包括 Docker 部署和 GitHub Actions CI/CD 設定。

## 使用 Docker 部署

### 前提條件

- 安裝 Docker 和 Docker Compose
- 系統上已安裝 Git

### 本地部署步驟

1. 克隆倉庫：

```bash
git clone https://github.com/yourusername/ContextRecord.git
cd ContextRecord
```

2. 使用 Docker Compose 構建和啟動應用：

```bash
docker-compose up -d
```

3. 訪問應用：

```
http://localhost:8000
```

### 手動部署到伺服器

1. 在伺服器上克隆倉庫：

```bash
git clone https://github.com/yourusername/ContextRecord.git
cd ContextRecord
```

2. 使用 Docker Compose 部署：

```bash
docker-compose up -d
```

## 使用 GitHub Actions 自動構建 Docker 映像

本專案使用 GitHub Actions 實現 CI/CD 流程。當代碼推送到 main 分支並通過 CI 檢查後，會自動構建 Docker 映像並推送到 GitHub Container Registry (GHCR)。

### 配置 GitHub Secrets

在使用 GitHub Actions 進行自動構建前，需要在 GitHub 倉庫中配置以下 Secret：

1. `gamepig_ContextRecord` - GitHub 個人訪問令牌 (PAT)，用於訪問 GitHub Container Registry

設定步驟：

1. 在 GitHub 倉庫頁面，點擊 "Settings"
2. 在側邊欄中，選擇 "Secrets and variables" > "Actions"
3. 點擊 "New repository secret" 按鈕
4. 添加 `gamepig_ContextRecord` Secret

#### 創建個人訪問令牌 (PAT)

如果您還沒有 PAT，請按照以下步驟創建：

1. 訪問 GitHub 個人設定頁面 https://github.com/settings/tokens
2. 點擊 "Generate new token (classic)"
3. 提供一個描述性名稱
4. 選擇以下權限：
   - `repo` (所有)
   - `write:packages` (用於推送映像到 GHCR)
   - `read:packages`
   - `delete:packages`（可選，如需刪除舊映像）
5. 點擊 "Generate token"
6. 複製生成的令牌並將其添加為 `gamepig_ContextRecord` secret

### 手動部署到雲端平台

目前，應用程式需要手動部署到雲端平台。以下是使用自動構建的 Docker 映像進行部署的步驟：

1. 從 GitHub Container Registry 拉取最新映像：

```bash
docker pull ghcr.io/Gamepig/ContextRecord:latest
```

2. 在目標伺服器上運行容器：

```bash
# 創建資料目錄
mkdir -p ~/context-record-data

# 運行容器
docker run -d \
  --name context-record \
  -p 8000:8000 \
  -v ~/context-record-data:/app/data \
  --restart unless-stopped \
  ghcr.io/Gamepig/ContextRecord:latest
```

### 將來的自動部署計劃

後續將添加對雲端平台的自動部署功能，可能包括：

- 部署到 AWS ECS/Fargate
- 部署到 Google Cloud Run
- 部署到 Azure Container Instances
- 使用 Kubernetes 部署

## 部署後驗證

無論使用哪種部署方式，都可以通過以下命令檢查應用程式是否正常運行：

```bash
# 檢查容器狀態
docker ps | grep context-record

# 測試 API 響應
curl http://localhost:8000/

# 檢查日誌
docker logs context-record
```

## 常見問題排查

1. **容器無法啟動**：檢查 Docker 日誌 `docker logs context-record`
2. **數據庫連接問題**：確保環境變數 `DATABASE_URL` 設置正確
3. **權限問題**：確保數據目錄 `/app/data` 有正確的讀寫權限
4. **GitHub Actions 工作流程失敗**：
   - 檢查 `gamepig_ContextRecord` token 是否有效且具有正確權限
   - 檢查 Dockerfile 是否存在語法錯誤

## 資料備份

SQLite 數據庫檔案位於容器內的 `/app/data/app.db`，並通過 volume 掛載到主機的資料目錄。

定期備份數據：

```bash
# 備份數據
cp ~/context-record-data/app.db ~/backups/app_$(date +%Y%m%d).db
``` 
# 08_設定 GitHub Actions 的 CD 工作流程

## 任務說明
在這個任務中，您需要設定 GitHub Actions 的 CD (持續部署) 工作流程，以便在程式碼通過 CI 測試後，自動部署到目標環境。

## 任務目標
- 設定 GitHub Actions 工作流程，實現自動部署
- 配置 Docker 容器化部署
- 確保部署過程可靠且可重複

## 任務列表
- [x] 創建 Dockerfile 定義應用程序容器化環境
- [x] 創建 .dockerignore 檔案排除不必要的檔案
- [x] 設定 docker-compose.yml 用於本地開發和測試
- [x] 建立 GitHub Actions CD 工作流程檔案 (.github/workflows/cd.yml)
- [x] 配置 CD 工作流程以在 CI 成功後自動觸發
- [x] 設定構建 Docker 映像檔的步驟
- [x] 配置將映像檔推送到 GitHub Container Registry
- [x] 添加自動部署到目標伺服器的步驟
- [x] 設定必要的 GitHub Secrets (SSH_HOST, SSH_USERNAME, SSH_PRIVATE_KEY)
- [x] 寫入部署文檔說明如何設定 CD 環境
- [x] 測試構建 Docker 映像檔

## 技術要求
- 使用 GitHub Actions 進行 CD 設定
- 使用 Docker 進行容器化
- 配置 SSH 部署到遠程伺服器

## 成果物
- GitHub Actions 工作流程檔案 (.github/workflows/cd.yml)
- Dockerfile 和相關配置檔案
- 部署文檔

## 完成標準
- CD 工作流程在 CI 通過後自動觸發
- Docker 映像檔成功構建並推送到 GitHub Container Registry
- 應用程式能夠自動部署到目標環境
- 提供了完整的部署文檔和操作說明

## 注意事項
- 確保敏感資訊（如 SSH 密鑰、伺服器 IP 等）保存在 GitHub Secrets 中
- 確保 Dockerfile 遵循最佳實踐，例如多階段構建、使用非 root 用戶等
- 提供詳細的部署和故障排除文檔

## 細化步驟

1.  [ ] 在 `.github/workflows/` 目錄下創建或修改 CI 工作流程檔案 (`ci.yml` 或新的 `cd.yml`)，以便在 CI 成功後觸發 CD Job。
    *   **選項一 (整合到 ci.yml):** 在現有的 `ci.yml` 中新增一個 CD Job，並設定它依賴於 CI Job 的成功 (`needs: build`)。
    *   **選項二 (獨立 cd.yml):** 創建一個新的 `cd.yml` 檔案，並設定它在 `push` 到 `main` 分支且 CI 工作流程成功完成後觸發 (這通常需要在 CD Job 中檢查 CI 的狀態或使用特定的 GitHub Actions 功能)。
    *   **推薦方式：** 通常會建立一個獨立的 `cd.yml`，並設定其觸發條件為在 `main` 分支上的 push，並在 Job 中加入判斷前一個 CI 工作流程是否成功的步驟，或者使用 GitHub Actions 的環境和 Approval 機制。

2.  [ ] 在 CD 工作流程檔案中，定義一個新的 Job (例如 `deploy`)。
    *   設定運行環境 (例如 `runs-on: ubuntu-latest`)。
    *   如果使用獨立的 `cd.yml`，設定它依賴於 CI Job 的成功 (例如 `needs: ci_job_name`)。

3.  [ ] 定義 CD Job 的步驟 (Steps)：
    *   **Checkout 程式碼：** 使用 `actions/checkout@v4` Action。
        ```yaml
        - uses: actions/checkout@v4
        ```
    *   **設定 Docker Buildx (如果需要)：** 用於建置多平台 Docker 映像檔。
        ```yaml
        - name: Set up Docker Buildx
          uses: docker/setup-buildx-action@v3
        ```
    *   **登入容器註冊中心：** 登入 Docker Hub, GitHub Container Registry (GHCR) 或其他註冊中心。需要使用 GitHub Secrets 來儲存您的註冊中心憑證。
        ```yaml
        - name: Login to Docker Hub
          uses: docker/login-action@v3
          with:
            username: ${{ secrets.DOCKER_HUB_USERNAME }}
            password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
        # 或登入 GHCR
        # - name: Login to GitHub Container Registry
        #   uses: docker/login-action@v3
        #   with:
        #     registry: ghcr.io
        #     username: ${{ github.actor }}
        #     password: ${{ secrets.GITHUB_TOKEN }}
        ```
    *   **建置並推送 Docker 映像檔：** 使用 `docker/build-and-push-action` Action。
        *   指定 Dockerfile 的路徑 (`context: .`)。
        *   指定建置的平台 (`platforms: linux/amd64`)。
        *   設定映像檔的 Tag (可以使用 commit SHA, 版本號等)。
        *   設定要推送到的註冊中心。
        ```yaml
        - name: Build and push Docker image
          uses: docker/build-and-push-action@v5
          with:
            context: .
            push: true
            tags: your_dockerhub_username/mcp_server:latest,your_dockerhub_username/mcp_server:${{ github.sha }}
            # 或推送到 GHCR
            # tags: ghcr.io/your_github_username/mcp_server:latest,ghcr.io/your_github_username/mcp_server:${{ github.sha }}
        ```
    *   **部署應用程式：** 這部分取決於您的部署策略。
        *   **方式一 (SSH 到伺服器)：** 使用 Action SSH 到您的伺服器，然後執行命令 (例如 `docker pull`, `docker run` 或更新 Docker Compose)。需要設定 SSH 相關的 Secrets。
            ```yaml
            - name: Deploy via SSH
              uses: appleboy/ssh-action@v1.0.3
              with:
                host: ${{ secrets.SSH_HOST }}
                username: ${{ secrets.SSH_USERNAME }}
                key: ${{ secrets.SSH_KEY }}
                script: |
                  cd /path/to/your/app
                  docker pull your_dockerhub_username/mcp_server:${{ github.sha }}
                  docker stop mcp_server || true
                  docker rm mcp_server || true
                  docker run -d --name mcp_server -p 8000:8000 your_dockerhub_username/mcp_server:${{ github.sha }}
            ```
        *   **方式二 (使用雲端服務提供商的部署工具)：** 如果部署到 AWS ECS, Google Cloud Run, Azure Container Instances 等，可以使用相應雲端提供商的 GitHub Actions。
        *   **方式三 (Kubernetes)：** 使用 Actions 來更新 Kubernetes Deployment 或使用 Flux/Argo CD 等 GitOps 工具。
    *   **部署後驗證：** 在應用程式部署成功後，執行一些自動化的測試或健康檢查，確保應用程式正常運行。這可以包括：
        *   向應用程式的健康檢查端點發送 HTTP 請求 (例如 `/health`)。
        *   執行一些關鍵的 API 調用 (例如測試紀錄和搜尋功能的基本流程)。
        *   簡單驗證 SSE 連接是否能建立。
        *   這部分可以重用或改寫 `Task/07` 中定義的部分整合測試。
        ```yaml
        - name: Run post-deployment validation tests
          run: |
            # 這裡放置執行測試腳本的命令
            # 例如：
            # python tests/post_deploy_tests.py
            # 或者使用 curl/ अन्य 工具檢查健康狀態和關鍵 API
            curl http://localhost:8000/health
        ```

4.  [ ] 配置 GitHub Secrets。
    *   在您的 GitHub 倉庫設定中，添加用於 Docker 註冊中心登入和/或 SSH 部署所需的 Secrets (例如 `DOCKER_HUB_USERNAME`, `DOCKER_HUB_ACCESS_TOKEN`, `SSH_HOST`, `SSH_USERNAME`, `SSH_KEY` 等)。
5.  [ ] 提交並推送 CD 工作流程檔案到 GitHub 倉庫。
6.  [ ] 在 GitHub 倉庫的 Actions 選項卡中，檢查 CD 工作流程是否在 CI 成功後自動觸發並執行。確保部署步驟成功完成。 
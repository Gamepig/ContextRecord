# 03_設定 GitHub Actions 的 CI 工作流程

## 目標
設定自動化的持續整合 (CI) 工作流程，以確保程式碼在提交和合併到主分支之前通過 Linting、格式化檢查和單元測試。

## 細化步驟

1.  [x] 在專案根目錄下建立 `.github/workflows/` 目錄 (如果步驟 1 未創建)。
    *   執行命令：`mkdir -p .github/workflows`
2.  [x] 在 `.github/workflows/` 目錄下創建一個新的 YAML 檔案作為 CI 工作流程定義 (例如 `ci.yml`)。
    *   檔案路徑：`.github/workflows/ci.yml`
3.  [x] 編輯 `ci.yml` 檔案，定義 CI 工作流程。
    *   設定工作流程名稱 (例如 `Python CI`)。
    *   設定觸發條件：在 `push` 到 `main` 分支以及針對 `main` 分支的 `pull_request` 時觸發。
        ```yaml
        on:
          push:
            branches:
              - main
          pull_request:
            branches:
              - main
        ```
    *   定義一個或多個 Job (例如 `build`)。
    *   在 Job 中設定運行環境 (例如 `runs-on: ubuntu-latest`)。
    *   定義 Job 的步驟 (Steps)：
        *   **Checkout 程式碼：** 使用 `actions/checkout@v4` Action。
            ```yaml
            - uses: actions/checkout@v4
            ```
        *   **設定 Python 環境：** 使用 `actions/setup-python@v5` Action，指定 Python 版本 (建議使用與您開發環境相同的版本)。
            ```yaml
            - name: Set up Python
              uses: actions/setup-python@v5
              with:
                python-version: '3.9' # 或您使用的版本
                cache: 'uv' # 使用 uv 緩存依賴
            ```
        *   **安裝依賴：** 使用 UV 安裝 `requirements.txt` 中的套件。
            ```yaml
            - name: Install dependencies
              run: uv install -r requirements.txt
            ```
        *   **執行 Linting 和格式化檢查：** 運行程式碼檢查工具。
            *   例如使用 Flake8 和 Black：
                ```yaml
                - name: Run linter and formatter checks
                  run: |
                    uv install flake8 black
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                    black --check .
                ```
            *   **注意：** 需要在 `requirements.txt` 或 CI 安裝步驟中包含 `flake8` 和 `black`。
        *   **執行單元測試：** 運行專案中的測試套件 (假設您使用 `pytest`)。
            ```yaml
            - name: Run unit tests
              run: | 
                uv install pytest
                pytest
            ```
            *   **注意：** 需要在 `requirements.txt` 或 CI 安裝步驟中包含 `pytest`。
4.  [x] 提交並推送 `ci.yml` 檔案到 GitHub 倉庫。
5.  [x] 在 GitHub 倉庫的 Actions 選項卡中，檢查工作流程是否成功觸發並執行。
    *   確保所有步驟都成功通過，特別是 Linting 和測試。 
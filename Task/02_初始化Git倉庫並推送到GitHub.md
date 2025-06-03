# 02_初始化 Git 倉庫並推送到 GitHub

## 目標
初始化專案的 Git 倉庫，配置忽略文件，並將程式碼推送到遠端的 GitHub 倉庫，建立版本控制的基礎。

## 細化步驟

1.  [x] 在專案根目錄下初始化一個新的 Git 倉庫。
    *   執行命令：`git init`
2.  [x] 建立 `.gitignore` 檔案。
    *   在專案根目錄下創建名為 `.gitignore` 的檔案。
    *   編輯 `.gitignore` 檔案，加入需要忽略的文件和目錄規則。建議至少包含：
        ```gitignore
        .venv/
        venv/
        __pycache__/
        *.pyc
        *.log
        .env
        !.env.example # 如果有範例檔案則保留
        /docker/data/ # 如果數據卷在專案目錄內
        /Task/*.md # 忽略 Task 目錄下的步驟文件，避免重複提交計畫內容
        ```
3.  [x] 將所有當前專案文件（除了 `.gitignore` 中指定的）加入到 Git 暫存區。
    *   執行命令：`git add .`
4.  [x] 執行首次程式碼提交。
    *   執行命令：`git commit -m "Initial project setup and git init"`
5.  [x] 在 GitHub 網站上建立一個新的空遠端倉庫。
    *   登入 GitHub。
    *   創建一個新的倉庫，不要初始化 README、.gitignore 或 License。
    *   複製新倉庫的 HTTPS 或 SSH URL。
6.  [x] 將本地倉庫與剛剛在 GitHub 上建立的遠端倉庫關聯。
    *   執行命令：`git remote add origin [您的遠端倉庫 URL]` (將 `[您的遠端倉庫 URL]` 替換為實際 URL)
7.  [x] 將本地主分支的程式碼推送到 GitHub 遠端倉庫。
    *   執行命令：`git push -u origin main` (如果您使用 `master` 作為主分支，則替換 `main`)
8.  [x] 驗證程式碼是否成功推送到 GitHub 倉庫頁面。 
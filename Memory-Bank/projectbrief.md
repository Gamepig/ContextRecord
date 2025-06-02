# 專案簡介 (Project Brief)

## 專案名稱
MCP Server (ContextRecord)

## 專案目標
建立一個基於 Python 的 MCP Server，用於紀錄對話內容、支援 AI 搜尋、使用 Server-Sent Events (SSE) 技術進行即時通訊，並可透過 Docker 容器化部署。

## 核心功能
- 對話內容紀錄：將使用者和 AI 之間的對話儲存到資料庫。
- AI 搜尋：支援對儲存的對話進行智慧搜尋，包括未來的向量搜尋。
- 即時通訊：使用 SSE 技術實現伺服器向客戶端推送即時更新。
- Docker 容器化：提供一致的建置和運行環境。

## 技術棧
- 後端：Python, FastAPI
- 資料庫：PostgreSQL (考慮使用 pgvector)
- 即時通訊：Server-Sent Events (SSE)
- 容器化：Docker, Docker Compose
- 版本控制：Git, GitHub
- 持續整合/部署：GitHub Actions

## 專案背景與動機
建立一個能夠可靠紀錄和檢索對話歷史的後端服務，特別是為了支援 AI 應用程式的需求，包括未來進行語義搜尋的能力。容器化和自動化流程確保了開發和部署的效率與一致性。

## 專案範圍
- 實作核心的對話紀錄和基本文字搜尋 API。
- 實作基於 SSE 的即時訊息推送功能。
- 完成應用程式的 Dockerfile 和 Docker Compose 設定。
- 設定基本的 CI/CD 工作流程。
- 撰寫必要的專案文件。

## 非專案範圍 (目前)
- 前端使用者介面。
- 複雜的 AI 處理邏輯 (專注於基礎設施和數據儲存/檢索)。
- 複雜的使用者認證和授權機制 (基礎版本)。
- 高可用性或負載平衡的生產環境部署架構。 
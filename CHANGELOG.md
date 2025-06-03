# 📝 變更日誌

所有重要的專案變更都會記錄在此檔案中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
並且此專案遵循 [語義化版本](https://semver.org/lang/zh-TW/)。

## [未發布]

### 新增
- 待發布的新功能

### 變更
- 待發布的變更

### 修復
- 待發布的錯誤修復

---

## [1.0.0] - 2025-01-27

### 新增
- 🎯 **核心 MCP Server 功能**
  - 完整的 Model Context Protocol 實現
  - 支援工具 (Tools)、資源 (Resources) 和提示 (Prompts)
  - 與 Cursor IDE 完美整合

- 💬 **對話記錄系統**
  - `create_conversation` - 創建新的對話記錄
  - `search_conversations` - 搜尋對話記錄
  - `get_conversation_stats` - 獲取對話統計資訊
  - `delete_conversation` - 刪除指定對話記錄

- 🤖 **自動記錄功能**
  - `enable_auto_recording` - 啟用自動記錄
  - `disable_auto_recording` - 停用自動記錄
  - `auto_record_conversation` - 自動記錄對話內容
  - `get_auto_recording_status` - 獲取自動記錄狀態
  - 多會話支援，每個會話獨立配置
  - 靈活的記錄選項（用戶訊息、助理回應或兩者）

- 🗄️ **資料庫系統**
  - SQLite 資料庫支援
  - 異步資料庫操作
  - 自動資料庫初始化
  - 完整的 CRUD 操作

- 📚 **資源與提示**
  - Recent Conversations 資源
  - 對話模式分析提示
  - 對話總結提示

- 🐳 **Docker 支援**
  - 完整的 Docker 容器化
  - Docker Compose 配置
  - 開發和生產環境支援

- 🧪 **測試套件**
  - 完整的單元測試
  - 整合測試
  - MCP 協議測試
  - 自動記錄功能測試

- 📖 **完整文件**
  - 詳細的 README 說明
  - API 文件
  - 技術文件
  - 開發指南
  - 貢獻指南

### 技術特性
- **Python 3.13+** 支援
- **FastAPI** 框架
- **SQLAlchemy** 異步 ORM
- **Pydantic** 資料驗證
- **MCP SDK** 整合
- **UV** 套件管理

### 安全性
- 輸入驗證和清理
- SQL 注入防護
- 錯誤處理和日誌記錄

### 效能
- 異步資料庫操作
- 連接池管理
- 查詢優化
- 記憶體效率

---

## 版本說明

### 版本號格式
我們使用 [語義化版本](https://semver.org/lang/zh-TW/) 格式：`MAJOR.MINOR.PATCH`

- **MAJOR** - 不相容的 API 變更
- **MINOR** - 向後相容的功能新增
- **PATCH** - 向後相容的錯誤修復

### 變更類型

- **新增** - 新功能
- **變更** - 現有功能的變更
- **棄用** - 即將移除的功能
- **移除** - 已移除的功能
- **修復** - 錯誤修復
- **安全性** - 安全性相關修復

---

## 貢獻

如果您想為此專案做出貢獻，請參閱我們的 [貢獻指南](CONTRIBUTING.md)。

## 授權

此專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案。 
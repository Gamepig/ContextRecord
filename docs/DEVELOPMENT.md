# 🛠️ ContextRecord MCP Server 開發指南

## 目錄

- [🛠️ ContextRecord MCP Server 開發指南](#️-contextrecord-mcp-server-開發指南)
  - [目錄](#目錄)
  - [🚀 開發環境設定](#-開發環境設定)
    - [系統需求](#系統需求)
    - [環境準備](#環境準備)
    - [IDE 配置](#ide-配置)
  - [📁 專案結構](#-專案結構)
  - [🔧 開發工作流程](#-開發工作流程)
    - [功能開發](#功能開發)
    - [測試流程](#測試流程)
    - [程式碼品質](#程式碼品質)
  - [🧪 測試指南](#-測試指南)
    - [測試類型](#測試類型)
    - [測試執行](#測試執行)
    - [測試覆蓋率](#測試覆蓋率)
  - [📦 部署指南](#-部署指南)
    - [本地部署](#本地部署)
    - [Docker 部署](#docker-部署)
    - [生產環境](#生產環境)
  - [🔍 除錯指南](#-除錯指南)
    - [常見問題](#常見問題)
    - [日誌分析](#日誌分析)
    - [效能分析](#效能分析)
  - [🤝 貢獻指南](#-貢獻指南)
    - [程式碼規範](#程式碼規範)
    - [提交規範](#提交規範)
    - [Pull Request 流程](#pull-request-流程)

---

## 🚀 開發環境設定

### 系統需求

- **作業系統**: macOS 15+, Linux, Windows 10+
- **Python**: 3.13+
- **UV**: 最新版本
- **Git**: 2.30+
- **Docker**: 20.10+ (可選)
- **Cursor IDE**: 最新版本 (推薦)

### 環境準備

#### 1. 克隆專案

```bash
git clone https://github.com/yourusername/ContextRecord.git
cd ContextRecord
```

#### 2. 設定 Python 環境

```bash
# 使用 UV 創建虛擬環境
uv venv

# 啟用虛擬環境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安裝開發依賴
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt  # 開發依賴（如果存在）
```

#### 3. 環境變數設定

創建 `.env` 檔案：

```bash
# 資料庫設定
DATABASE_PATH=data/conversations.db

# 開發模式
DEBUG=true

# 日誌等級
LOG_LEVEL=DEBUG
```

#### 4. 初始化資料庫

```bash
python src/mcp_server.py
```

### IDE 配置

#### Cursor IDE 設定

1. **MCP 配置** (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "contextrecord-dev": {
      "command": "/path/to/ContextRecord/.venv/bin/python",
      "args": ["/path/to/ContextRecord/src/mcp_server.py"],
      "env": {
        "DATABASE_PATH": "/path/to/ContextRecord/data/conversations.db",
        "DEBUG": "true"
      }
    }
  }
}
```

2. **VS Code 設定** (`.vscode/settings.json`):

```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"]
}
```

---

## 📁 專案結構

```
ContextRecord/
├── src/                          # 原始碼
│   ├── mcp_server.py            # MCP Server 主檔案
│   └── functions/               # 功能模組
│       ├── __init__.py
│       ├── conversations.py     # 對話相關功能
│       └── server.py           # 伺服器設定
├── data/                        # 資料目錄
│   └── conversations.db        # SQLite 資料庫
├── tests/                       # 測試檔案
│   ├── __init__.py
│   ├── test_mcp_tools.py       # 工具測試
│   ├── test_mcp_stdio.py       # STDIO 測試
│   └── test_auto_recording.py  # 自動記錄測試
├── docs/                        # 文件
│   ├── API.md                  # API 文件
│   ├── TECHNICAL.md            # 技術文件
│   └── DEVELOPMENT.md          # 開發指南
├── docker/                      # Docker 相關檔案
│   └── Dockerfile.dev          # 開發環境 Dockerfile
├── examples/                    # 範例檔案
│   └── auto_recording_demo.py  # 自動記錄示範
├── .github/                     # GitHub 工作流程
│   └── workflows/
│       ├── test.yml            # 測試工作流程
│       └── deploy.yml          # 部署工作流程
├── requirements.txt             # 生產依賴
├── requirements-dev.txt         # 開發依賴
├── docker-compose.yml          # Docker Compose 配置
├── .gitignore                  # Git 忽略檔案
├── .env.example               # 環境變數範例
└── README.md                  # 專案說明
```

---

## 🔧 開發工作流程

### 功能開發

#### 1. 創建功能分支

```bash
git checkout -b feature/new-awesome-feature
```

#### 2. 開發新功能

**添加新工具**:

```python
# 在 src/mcp_server.py 中添加工具定義
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        # 現有工具...
        types.Tool(
            name="new_awesome_tool",
            description="新的強大工具",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "參數1描述"
                    }
                },
                "required": ["param1"]
            }
        )
    ]

# 添加工具處理邏輯
@server.call_tool()
async def handle_call_tool(
    name: str, 
    arguments: dict | None
) -> list[types.TextContent]:
    if name == "new_awesome_tool":
        param1 = arguments.get("param1")
        # 實現工具邏輯
        result = {"success": True, "data": f"處理結果: {param1}"}
        return [types.TextContent(type="text", text=json.dumps(result))]
```

#### 3. 編寫測試

```python
# tests/test_new_feature.py
import pytest
import asyncio
from src.mcp_server import handle_call_tool

class TestNewAwesomeTool:
    @pytest.mark.asyncio
    async def test_new_awesome_tool_success(self):
        """測試新工具的成功情況"""
        result = await handle_call_tool(
            "new_awesome_tool",
            {"param1": "test_value"}
        )
        
        assert len(result) == 1
        data = json.loads(result[0].text)
        assert data["success"] is True
        assert "test_value" in data["data"]
    
    @pytest.mark.asyncio
    async def test_new_awesome_tool_missing_param(self):
        """測試缺少參數的情況"""
        with pytest.raises(ValueError):
            await handle_call_tool("new_awesome_tool", {})
```

### 測試流程

#### 1. 單元測試

```bash
# 執行所有測試
python -m pytest tests/

# 執行特定測試檔案
python -m pytest tests/test_new_feature.py

# 執行特定測試方法
python -m pytest tests/test_new_feature.py::TestNewAwesomeTool::test_new_awesome_tool_success
```

#### 2. 整合測試

```bash
# 測試 MCP 整合
python test_mcp_stdio.py

# 測試工具功能
python test_mcp_tools.py
```

#### 3. 手動測試

```bash
# 啟動開發伺服器
python src/mcp_server.py

# 在另一個終端測試
mcp dev src/mcp_server.py
```

### 程式碼品質

#### 1. 程式碼格式化

```bash
# 使用 Black 格式化
black src/ tests/

# 使用 isort 排序 import
isort src/ tests/
```

#### 2. 程式碼檢查

```bash
# 使用 pylint 檢查
pylint src/

# 使用 flake8 檢查
flake8 src/ tests/
```

#### 3. 類型檢查

```bash
# 使用 mypy 檢查類型
mypy src/
```

---

## 🧪 測試指南

### 測試類型

#### 1. 單元測試

**目的**: 測試個別函數和方法

**範例**:
```python
def test_get_auto_recording_config():
    """測試自動記錄配置獲取"""
    config = get_auto_recording_config("test_session")
    assert config["enabled"] is False
    assert config["record_user"] is True
    assert config["record_assistant"] is True
```

#### 2. 整合測試

**目的**: 測試組件間的互動

**範例**:
```python
@pytest.mark.asyncio
async def test_full_recording_workflow():
    """測試完整的記錄工作流程"""
    # 啟用自動記錄
    enable_result = await handle_call_tool(
        "enable_auto_recording",
        {"session_id": "test"}
    )
    
    # 記錄對話
    record_result = await handle_call_tool(
        "auto_record_conversation",
        {
            "user_message": "測試問題",
            "assistant_response": "測試回答",
            "session_id": "test"
        }
    )
    
    # 驗證記錄
    search_result = await handle_call_tool(
        "search_conversations",
        {"query": "測試問題"}
    )
    
    assert len(search_result) > 0
```

#### 3. 端到端測試

**目的**: 測試完整的用戶工作流程

**範例**:
```python
def test_mcp_client_integration():
    """測試 MCP Client 整合"""
    # 使用真實的 MCP Client 測試
    pass
```

### 測試執行

#### 1. 本地測試

```bash
# 快速測試
python -m pytest tests/ -v

# 詳細測試報告
python -m pytest tests/ -v --tb=long

# 並行測試
python -m pytest tests/ -n auto
```

#### 2. 測試覆蓋率

```bash
# 生成覆蓋率報告
python -m pytest tests/ --cov=src --cov-report=html

# 查看覆蓋率報告
open htmlcov/index.html
```

#### 3. 效能測試

```bash
# 使用 pytest-benchmark
python -m pytest tests/test_performance.py --benchmark-only
```

### 測試覆蓋率

**目標覆蓋率**: 90%+

**重點測試區域**:
- 所有 MCP 工具函數
- 資料庫操作
- 錯誤處理邏輯
- 自動記錄功能

---

## 📦 部署指南

### 本地部署

#### 1. 開發模式

```bash
# 啟動開發伺服器
python src/mcp_server.py

# 使用 MCP 開發工具
mcp dev src/mcp_server.py
```

#### 2. 生產模式

```bash
# 設定生產環境變數
export DEBUG=false
export LOG_LEVEL=INFO

# 啟動伺服器
python src/mcp_server.py
```

### Docker 部署

#### 1. 建構映像

```bash
# 開發映像
docker build -f docker/Dockerfile.dev -t contextrecord:dev .

# 生產映像
docker build -t contextrecord:latest .
```

#### 2. 運行容器

```bash
# 開發模式
docker-compose up -d

# 生產模式
docker run -d \
  --name contextrecord \
  -p 8812:8811 \
  -v $(pwd)/data:/app/data \
  -e DATABASE_PATH=/app/data/conversations.db \
  contextrecord:latest
```

### 生產環境

#### 1. 環境配置

```bash
# 生產環境變數
DATABASE_PATH=/var/lib/contextrecord/conversations.db
LOG_LEVEL=INFO
DEBUG=false
```

#### 2. 監控設定

```bash
# 使用 systemd 管理服務
sudo systemctl enable contextrecord
sudo systemctl start contextrecord
sudo systemctl status contextrecord
```

#### 3. 備份策略

```bash
# 資料庫備份腳本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /var/lib/contextrecord/conversations.db \
   /backup/contextrecord_$DATE.db
```

---

## 🔍 除錯指南

### 常見問題

#### 1. MCP Server 無法啟動

**症狀**: 伺服器啟動失敗

**可能原因**:
- Python 環境問題
- 依賴套件缺失
- 資料庫權限問題

**解決方案**:
```bash
# 檢查 Python 版本
python --version

# 重新安裝依賴
uv pip install --force-reinstall -r requirements.txt

# 檢查資料庫權限
ls -la data/
```

#### 2. Cursor IDE 無法連接

**症狀**: IDE 顯示 "No tools available"

**可能原因**:
- MCP 配置錯誤
- 路徑設定問題
- 權限問題

**解決方案**:
```bash
# 檢查配置檔案
cat ~/.cursor/mcp.json

# 測試 MCP Server
python src/mcp_server.py

# 檢查日誌
tail -f ~/.cursor/logs/mcp.log
```

#### 3. 資料庫錯誤

**症狀**: 資料庫操作失敗

**可能原因**:
- 資料庫檔案損壞
- 磁碟空間不足
- 權限問題

**解決方案**:
```bash
# 檢查資料庫完整性
sqlite3 data/conversations.db "PRAGMA integrity_check;"

# 檢查磁碟空間
df -h

# 重建資料庫
rm data/conversations.db
python src/mcp_server.py
```

### 日誌分析

#### 1. 啟用詳細日誌

```python
import logging

# 設定日誌等級
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### 2. 日誌檔案位置

- **開發環境**: `./logs/contextrecord.log`
- **生產環境**: `/var/log/contextrecord/contextrecord.log`
- **Docker**: 容器日誌 `docker logs contextrecord`

#### 3. 日誌分析工具

```bash
# 即時查看日誌
tail -f logs/contextrecord.log

# 搜尋錯誤
grep "ERROR" logs/contextrecord.log

# 分析效能
grep "SLOW" logs/contextrecord.log
```

### 效能分析

#### 1. 效能監控

```python
import time
import functools

def performance_monitor(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        
        if end_time - start_time > 1.0:  # 超過 1 秒
            logger.warning(f"SLOW: {func.__name__} took {end_time - start_time:.2f}s")
        
        return result
    return wrapper
```

#### 2. 資料庫效能

```sql
-- 分析查詢計劃
EXPLAIN QUERY PLAN SELECT * FROM conversations WHERE content LIKE '%keyword%';

-- 檢查索引使用
PRAGMA index_list(conversations);
```

#### 3. 記憶體使用

```python
import psutil
import os

def log_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
```

---

## 🤝 貢獻指南

### 程式碼規範

#### 1. Python 風格

- 遵循 **PEP 8** 標準
- 使用 **Black** 進行程式碼格式化
- 使用 **isort** 排序 import 語句
- 使用 **type hints** 進行類型註解

#### 2. 命名規範

```python
# 變數和函數：snake_case
user_message = "Hello"
def get_conversation_stats():
    pass

# 類別：PascalCase
class ConversationManager:
    pass

# 常數：UPPER_SNAKE_CASE
MAX_CONVERSATION_LENGTH = 10000
```

#### 3. 文件字串

```python
def create_conversation(role: str, content: str, metadata: str = None) -> dict:
    """
    創建新的對話記錄
    
    Args:
        role: 對話角色 (user, assistant, system)
        content: 對話內容
        metadata: JSON 格式的元數據 (可選)
    
    Returns:
        dict: 包含操作結果的字典
        
    Raises:
        ValueError: 當參數無效時
        DatabaseError: 當資料庫操作失敗時
    """
```

### 提交規範

#### 1. 提交訊息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**類型**:
- `feat`: 新功能
- `fix`: 錯誤修復
- `docs`: 文件更新
- `style`: 程式碼格式調整
- `refactor`: 程式碼重構
- `test`: 測試相關
- `chore`: 建構工具或輔助工具的變動

**範例**:
```
feat(tools): add conversation export functionality

Add new tool to export conversations in various formats:
- JSON export
- CSV export  
- Markdown export

Closes #123
```

#### 2. 分支命名

```
feature/description-of-feature
bugfix/description-of-bug
hotfix/critical-issue
docs/update-documentation
```

### Pull Request 流程

#### 1. 準備 PR

```bash
# 確保程式碼品質
black src/ tests/
isort src/ tests/
pylint src/
mypy src/

# 執行測試
python -m pytest tests/ --cov=src

# 更新文件
# 編輯 CHANGELOG.md
```

#### 2. 提交 PR

**PR 標題**: 簡潔描述變更內容

**PR 描述模板**:
```markdown
## 變更摘要
簡要描述這個 PR 的目的和變更內容。

## 變更類型
- [ ] 新功能
- [ ] 錯誤修復
- [ ] 文件更新
- [ ] 效能改善
- [ ] 重構

## 測試
- [ ] 已添加新的測試
- [ ] 所有現有測試通過
- [ ] 手動測試完成

## 檢查清單
- [ ] 程式碼遵循專案風格指南
- [ ] 自我檢查程式碼
- [ ] 程式碼有適當的註解
- [ ] 相關文件已更新
```

#### 3. 程式碼審查

**審查重點**:
- 功能正確性
- 程式碼品質
- 測試覆蓋率
- 文件完整性
- 效能影響

**回應審查**:
- 及時回應審查意見
- 解釋設計決策
- 根據建議進行修改

---

這份開發指南提供了完整的開發環境設定、工作流程、測試策略和貢獻指南，幫助開發者快速上手並維護高品質的程式碼。 
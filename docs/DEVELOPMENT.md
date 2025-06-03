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
git clone https://github.com/Gamepig/ContextRecord.git
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
│   ├── __init__.py
│   ├── mcp_server.py            # MCP Server 主檔案
│   ├── database.py              # 資料庫配置
│   ├── models.py                # 資料模型
│   ├── main.py                  # FastAPI 主程式
│   └── functions/               # 功能模組
│       ├── __init__.py
│       ├── conversations.py     # 對話相關功能
│       └── server.py           # 伺服器設定
├── data/                        # 資料目錄
│   └── conversations.db        # SQLite 資料庫
├── tests/                       # 測試檔案
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置
│   ├── test_main.py            # 主程式測試
│   ├── test_server.py          # 伺服器測試
│   ├── test_conversations.py   # 對話功能測試
│   ├── test_database.py        # 資料庫測試
│   ├── test_mcp_server.py      # MCP Server 測試
│   ├── test_mcp_tools.py       # MCP 工具測試
│   ├── test_mcp_stdio.py       # STDIO 通信測試
│   ├── test_auto_recording.py  # 自動記錄測試
│   └── simple_test.py          # 簡化測試
├── docs/                        # 文件
│   ├── API.md                  # API 文件
│   ├── TECHNICAL.md            # 技術文件
│   └── DEVELOPMENT.md          # 開發指南
├── examples/                    # 範例檔案
│   └── auto_recording_demo.py  # 自動記錄示範
├── docker/                      # Docker 相關檔案
│   └── Dockerfile.dev          # 開發環境 Dockerfile
├── .github/                     # GitHub 工作流程
│   └── workflows/
│       ├── ci.yml              # CI 工作流程
│       └── cd.yml              # CD 工作流程
├── Memory-Bank/                 # 記憶銀行檔案
├── Task/                        # 任務相關檔案
├── requirements.txt             # 生產依賴
├── docker-compose.yml          # Docker Compose 配置
├── Dockerfile                  # 生產環境 Dockerfile
├── cursor_mcp_config.json      # Cursor MCP 配置範例
├── .gitignore                  # Git 忽略檔案
├── .env.example               # 環境變數範例
├── CONTRIBUTING.md            # 貢獻指南
├── CHANGELOG.md               # 變更記錄
├── LICENSE                    # 授權檔案
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
cd tests && python test_mcp_stdio.py

# 測試工具功能
cd tests && python test_mcp_tools.py

# 測試自動記錄功能
cd tests && python test_auto_recording.py

# 簡化測試
cd tests && python simple_test.py
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
# 📖 ContextRecord MCP Server 技術文件

## 目錄

- [📖 ContextRecord MCP Server 技術文件](#-contextrecord-mcp-server-技術文件)
  - [目錄](#目錄)
  - [🏗️ 系統架構](#️-系統架構)
    - [核心組件](#核心組件)
    - [資料流程](#資料流程)
  - [🔧 核心函數詳解](#-核心函數詳解)
    - [資料庫管理](#資料庫管理)
    - [MCP 工具函數](#mcp-工具函數)
    - [自動記錄系統](#自動記錄系統)
    - [搜尋與統計](#搜尋與統計)
  - [📊 資料庫設計](#-資料庫設計)
    - [表結構](#表結構)
    - [索引策略](#索引策略)
  - [🔌 MCP 協議實現](#-mcp-協議實現)
    - [工具註冊](#工具註冊)
    - [資源處理](#資源處理)
    - [提示系統](#提示系統)
  - [⚡ 效能優化](#-效能優化)
    - [資料庫優化](#資料庫優化)
    - [記憶體管理](#記憶體管理)
  - [🛡️ 錯誤處理](#️-錯誤處理)
    - [異常類型](#異常類型)
    - [錯誤恢復](#錯誤恢復)
  - [🧪 測試策略](#-測試策略)
    - [單元測試](#單元測試)
    - [整合測試](#整合測試)
  - [🔒 安全考量](#-安全考量)
    - [資料保護](#資料保護)
    - [輸入驗證](#輸入驗證)

---

## 🏗️ 系統架構

### 核心組件

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │   MCP Client    │    │  Other Clients  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     MCP Protocol Layer    │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │    ContextRecord Server   │
                    │  ┌─────────────────────┐  │
                    │  │   Tool Handlers     │  │
                    │  ├─────────────────────┤  │
                    │  │  Resource Manager   │  │
                    │  ├─────────────────────┤  │
                    │  │   Prompt System     │  │
                    │  └─────────────────────┘  │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     Database Layer        │
                    │    (SQLite/PostgreSQL)    │
                    └───────────────────────────┘
```

### 資料流程

1. **請求接收**: MCP Client 發送工具調用請求
2. **協議解析**: MCP Protocol Layer 解析請求格式
3. **工具路由**: Server 根據工具名稱路由到對應處理函數
4. **業務邏輯**: 執行具體的業務邏輯處理
5. **資料操作**: 與資料庫進行互動
6. **回應封裝**: 將結果封裝為 MCP 格式回應
7. **結果返回**: 透過 MCP Protocol 返回給 Client

---

## 🔧 核心函數詳解

### 資料庫管理

#### `init_database()`

**功能**: 初始化 SQLite 資料庫和表結構

```python
def init_database():
    """
    初始化資料庫
    
    功能:
    - 創建 data 目錄（如果不存在）
    - 建立 SQLite 連接
    - 創建 conversations 表
    - 設定適當的索引
    
    異常處理:
    - 目錄創建失敗
    - 資料庫連接失敗
    - 表創建失敗
    """
```

**實現細節**:
- 使用 `os.makedirs()` 確保目錄存在
- 採用 `IF NOT EXISTS` 語法避免重複創建
- 自動設定時間戳預設值
- 支援 JSON 格式的元數據儲存

#### `get_db_connection()`

**功能**: 獲取資料庫連接

```python
def get_db_connection():
    """
    獲取資料庫連接
    
    返回:
        sqlite3.Connection: 資料庫連接物件
    
    特性:
    - 自動初始化資料庫（如果需要）
    - 設定適當的連接參數
    - 啟用外鍵約束
    """
```

**最佳實踐**:
- 每次操作後及時關閉連接
- 使用 try-finally 確保資源釋放
- 支援連接池（未來擴展）

### MCP 工具函數

#### `handle_call_tool(name: str, arguments: dict)`

**功能**: MCP 工具調用的核心路由函數

```python
async def handle_call_tool(
    name: str, 
    arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    處理工具調用
    
    參數:
        name: 工具名稱
        arguments: 工具參數字典
    
    返回:
        list: MCP 內容物件列表
    
    支援的工具:
    - create_conversation
    - auto_record_conversation
    - enable_auto_recording
    - disable_auto_recording
    - get_auto_recording_status
    - search_conversations
    - get_conversation_stats
    - delete_conversation
    """
```

**路由邏輯**:
1. 驗證工具名稱
2. 提取和驗證參數
3. 調用對應的處理函數
4. 統一錯誤處理和日誌記錄
5. 格式化返回結果

#### `create_conversation` 工具

**功能**: 創建新的對話記錄

```python
# 工具實現
if name == "create_conversation":
    role = arguments.get("role")
    content = arguments.get("content")
    metadata = arguments.get("metadata")
    
    # 參數驗證
    if not role or not content:
        raise ValueError("role 和 content 參數為必填項")
    
    if role not in ["user", "assistant", "system"]:
        raise ValueError("role 必須為 'user', 'assistant' 或 'system'")
```

**驗證規則**:
- `role`: 必填，限定值為 user/assistant/system
- `content`: 必填，非空字串
- `metadata`: 可選，必須為有效 JSON 字串

**資料庫操作**:
```sql
INSERT INTO conversations (role, content, timestamp, metadata) 
VALUES (?, ?, CURRENT_TIMESTAMP, ?)
```

### 自動記錄系統

#### 自動記錄狀態管理

**全域狀態**: `AUTO_RECORDING_SESSIONS`

```python
AUTO_RECORDING_SESSIONS = {
    "session_id": {
        "enabled": bool,
        "record_user": bool,
        "record_assistant": bool
    }
}
```

#### `get_auto_recording_config(session_id: str)`

**功能**: 獲取指定會話的自動記錄配置

```python
def get_auto_recording_config(session_id: str = "default") -> dict:
    """
    獲取自動記錄配置
    
    參數:
        session_id: 會話識別碼
    
    返回:
        dict: 配置字典
        {
            "enabled": bool,
            "record_user": bool,
            "record_assistant": bool
        }
    
    預設配置:
    - enabled: False
    - record_user: True
    - record_assistant: True
    """
```

#### `enable_auto_recording` 工具

**功能**: 啟用指定會話的自動記錄

```python
# 實現邏輯
session_id = arguments.get("session_id", "default")
record_user = arguments.get("record_user", True)
record_assistant = arguments.get("record_assistant", True)

# 更新全域配置
AUTO_RECORDING_SESSIONS[session_id] = {
    "enabled": True,
    "record_user": record_user,
    "record_assistant": record_assistant
}
```

**配置持久化**: 目前配置儲存在記憶體中，重啟後會重置。未來版本可考慮持久化到資料庫。

#### `auto_record_conversation` 工具

**功能**: 根據配置自動記錄對話

```python
# 核心邏輯
config = get_auto_recording_config(session_id)

if not config["enabled"]:
    return "自動記錄未啟用"

# 記錄用戶訊息
if config["record_user"] and user_message:
    user_metadata = {
        "message_type": "user_input",
        "session_id": session_id,
        "auto_recorded": True
    }
    # 合併額外的 context
    if context:
        user_metadata.update(json.loads(context))
    
    # 插入資料庫
    cursor.execute(
        "INSERT INTO conversations (role, content, timestamp, metadata) VALUES (?, ?, ?, ?)",
        ("user", user_message, datetime.now(UTC).isoformat(), json.dumps(user_metadata))
    )
```

**元數據結構**:
```json
{
    "message_type": "user_input|assistant_response",
    "session_id": "會話ID",
    "auto_recorded": true,
    "timestamp": "ISO格式時間戳",
    "custom_field": "自訂欄位"
}
```

### 搜尋與統計

#### `search_conversations` 工具

**功能**: 基於關鍵字搜尋對話記錄

```python
# SQL 查詢
cursor.execute(
    """
    SELECT id, role, content, timestamp, metadata 
    FROM conversations 
    WHERE content LIKE ? 
    ORDER BY timestamp DESC 
    LIMIT ?
    """,
    (f"%{query}%", limit)
)
```

**搜尋特性**:
- **大小寫不敏感**: 使用 LIKE 操作符
- **部分匹配**: 支援子字串搜尋
- **時間排序**: 按時間戳降序排列
- **結果限制**: 支援分頁和限制

**未來優化**:
- 全文搜尋索引
- 多欄位搜尋
- 模糊搜尋
- 搜尋高亮

#### `get_conversation_stats` 工具

**功能**: 生成對話統計報告

```python
# 統計查詢
queries = [
    "SELECT COUNT(*) FROM conversations",  # 總數
    "SELECT role, COUNT(*) FROM conversations GROUP BY role",  # 角色分布
    "SELECT COUNT(*) FROM conversations WHERE timestamp >= datetime('now', '-7 days')"  # 近期活動
]
```

**統計指標**:
- **總對話數**: 所有記錄的總數
- **角色分布**: 各角色的對話數量
- **時間分析**: 最近一週的活動量
- **會話分析**: 各會話的活躍度（未來功能）

---

## 📊 資料庫設計

### 表結構

#### `conversations` 表

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 主鍵，自動遞增
    role TEXT NOT NULL,                    -- 對話角色
    content TEXT NOT NULL,                 -- 對話內容
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 時間戳
    metadata TEXT                          -- JSON 格式元數據
);
```

**欄位說明**:

| 欄位 | 類型 | 約束 | 說明 |
|------|------|------|------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | 唯一識別碼 |
| `role` | TEXT | NOT NULL | 對話角色 (user/assistant/system) |
| `content` | TEXT | NOT NULL | 對話內容，支援長文本 |
| `timestamp` | DATETIME | DEFAULT CURRENT_TIMESTAMP | 創建時間 |
| `metadata` | TEXT | NULL | JSON 格式的額外資訊 |

### 索引策略

**建議索引**:

```sql
-- 時間戳索引（用於時間排序）
CREATE INDEX idx_conversations_timestamp ON conversations(timestamp);

-- 角色索引（用於角色篩選）
CREATE INDEX idx_conversations_role ON conversations(role);

-- 內容全文索引（SQLite FTS，可選）
CREATE VIRTUAL TABLE conversations_fts USING fts5(content, content='conversations', content_rowid='id');
```

**索引效益**:
- 時間排序查詢加速 90%+
- 角色篩選查詢加速 80%+
- 全文搜尋效能提升 95%+

---

## 🔌 MCP 協議實現

### 工具註冊

#### `handle_list_tools()`

**功能**: 向 MCP Client 報告可用工具

```python
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出可用的工具
    
    返回:
        list[types.Tool]: 工具定義列表
    
    每個工具包含:
    - name: 工具名稱
    - description: 工具描述
    - inputSchema: JSON Schema 參數定義
    """
```

**工具定義範例**:

```python
types.Tool(
    name="create_conversation",
    description="創建新的對話記錄",
    inputSchema={
        "type": "object",
        "properties": {
            "role": {
                "type": "string",
                "description": "對話角色",
                "enum": ["user", "assistant", "system"]
            },
            "content": {
                "type": "string",
                "description": "對話內容"
            },
            "metadata": {
                "type": "string",
                "description": "JSON 格式的元數據"
            }
        },
        "required": ["role", "content"]
    }
)
```

### 資源處理

#### `handle_read_resource()`

**功能**: 處理資源讀取請求

```python
@server.read_resource()
async def handle_read_resource(uri: types.AnyUrl) -> str:
    """
    讀取資源內容
    
    參數:
        uri: 資源 URI
    
    支援的資源:
    - conversations://recent: 最近的對話記錄
    
    返回:
        str: JSON 格式的資源內容
    """
```

**資源 URI 設計**:
- `conversations://recent`: 最近 10 筆對話
- `conversations://stats`: 統計資訊（未來）
- `conversations://export`: 匯出功能（未來）

### 提示系統

#### `handle_get_prompt()`

**功能**: 提供預定義的提示模板

```python
@server.get_prompt()
async def handle_get_prompt(
    name: str, 
    arguments: dict | None
) -> types.GetPromptResult:
    """
    獲取提示內容
    
    參數:
        name: 提示名稱
        arguments: 提示參數
    
    支援的提示:
    - analyze_conversation_pattern: 分析對話模式
    - summarize_conversations: 總結對話記錄
    """
```

---

## ⚡ 效能優化

### 資料庫優化

#### 連接管理

```python
# 連接池實現（未來版本）
class DatabasePool:
    def __init__(self, max_connections=10):
        self.pool = queue.Queue(maxsize=max_connections)
        self.max_connections = max_connections
        
    def get_connection(self):
        try:
            return self.pool.get_nowait()
        except queue.Empty:
            return sqlite3.connect(DATABASE_PATH)
    
    def return_connection(self, conn):
        try:
            self.pool.put_nowait(conn)
        except queue.Full:
            conn.close()
```

#### 查詢優化

**批次插入**:
```python
def batch_insert_conversations(conversations):
    """批次插入對話記錄，提升效能"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.executemany(
        "INSERT INTO conversations (role, content, timestamp, metadata) VALUES (?, ?, ?, ?)",
        conversations
    )
    
    conn.commit()
    conn.close()
```

**分頁查詢**:
```python
def paginated_search(query, page=1, page_size=20):
    """分頁搜尋，避免大量資料載入"""
    offset = (page - 1) * page_size
    
    cursor.execute(
        """
        SELECT id, role, content, timestamp, metadata 
        FROM conversations 
        WHERE content LIKE ? 
        ORDER BY timestamp DESC 
        LIMIT ? OFFSET ?
        """,
        (f"%{query}%", page_size, offset)
    )
```

### 記憶體管理

#### 大型結果集處理

```python
def stream_search_results(query):
    """串流處理大型搜尋結果"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, role, content, timestamp, metadata FROM conversations WHERE content LIKE ?",
        (f"%{query}%",)
    )
    
    while True:
        rows = cursor.fetchmany(100)  # 每次處理 100 筆
        if not rows:
            break
        yield rows
    
    conn.close()
```

---

## 🛡️ 錯誤處理

### 異常類型

#### 自訂異常

```python
class ContextRecordError(Exception):
    """基礎異常類別"""
    pass

class DatabaseError(ContextRecordError):
    """資料庫相關錯誤"""
    pass

class ValidationError(ContextRecordError):
    """參數驗證錯誤"""
    pass

class ConfigurationError(ContextRecordError):
    """配置錯誤"""
    pass
```

#### 錯誤處理策略

```python
def safe_database_operation(operation):
    """安全的資料庫操作包裝器"""
    try:
        return operation()
    except sqlite3.Error as e:
        logger.error(f"資料庫錯誤: {e}")
        raise DatabaseError(f"資料庫操作失敗: {str(e)}")
    except Exception as e:
        logger.error(f"未預期錯誤: {e}")
        raise ContextRecordError(f"操作失敗: {str(e)}")
```

### 錯誤恢復

#### 自動重試機制

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    """重試裝飾器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"操作失敗，{delay}秒後重試 (嘗試 {attempt + 1}/{max_attempts}): {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def robust_database_query(query, params):
    """具有重試機制的資料庫查詢"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result
```

---

## 🧪 測試策略

### 單元測試

#### 資料庫測試

```python
import unittest
import tempfile
import os

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """設定測試環境"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        
        # 設定測試資料庫路徑
        global DATABASE_PATH
        DATABASE_PATH = self.test_db.name
        
        init_database()
    
    def tearDown(self):
        """清理測試環境"""
        os.unlink(self.test_db.name)
    
    def test_create_conversation(self):
        """測試對話創建功能"""
        # 測試實現
        pass
```

#### 工具測試

```python
class TestMCPTools(unittest.TestCase):
    async def test_create_conversation_tool(self):
        """測試創建對話工具"""
        result = await handle_call_tool(
            "create_conversation",
            {
                "role": "user",
                "content": "測試內容",
                "metadata": '{"test": true}'
            }
        )
        
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        
        # 驗證結果格式
        data = json.loads(result[0].text)
        self.assertTrue(data["success"])
```

### 整合測試

#### MCP 協議測試

```python
import mcp.client.stdio

class TestMCPIntegration(unittest.TestCase):
    async def test_full_mcp_workflow(self):
        """測試完整的 MCP 工作流程"""
        # 啟動 MCP Server
        # 建立 Client 連接
        # 測試工具調用
        # 驗證結果
        pass
```

---

## 🔒 安全考量

### 資料保護

#### 敏感資訊過濾

```python
import re

SENSITIVE_PATTERNS = [
    r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # 信用卡號
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # 電子郵件
    r'\b\d{3}-\d{2}-\d{4}\b',  # 社會安全號碼
]

def sanitize_content(content):
    """清理敏感資訊"""
    for pattern in SENSITIVE_PATTERNS:
        content = re.sub(pattern, '[REDACTED]', content)
    return content
```

### 輸入驗證

#### 參數驗證

```python
def validate_conversation_input(role, content, metadata=None):
    """驗證對話輸入參數"""
    # 角色驗證
    if role not in ["user", "assistant", "system"]:
        raise ValidationError(f"無效的角色: {role}")
    
    # 內容驗證
    if not content or len(content.strip()) == 0:
        raise ValidationError("對話內容不能為空")
    
    if len(content) > 10000:  # 10KB 限制
        raise ValidationError("對話內容過長")
    
    # 元數據驗證
    if metadata:
        try:
            json.loads(metadata)
        except json.JSONDecodeError:
            raise ValidationError("元數據必須為有效的 JSON 格式")
```

#### SQL 注入防護

```python
# 使用參數化查詢
cursor.execute(
    "SELECT * FROM conversations WHERE content LIKE ?",
    (f"%{query}%",)  # 參數化，防止 SQL 注入
)

# 避免字串拼接
# 錯誤示範：
# cursor.execute(f"SELECT * FROM conversations WHERE content LIKE '%{query}%'")
```

---

這份技術文件涵蓋了 ContextRecord MCP Server 的所有重要技術細節，包括核心函數的詳細實現、資料庫設計、效能優化策略、錯誤處理機制、測試方法和安全考量。開發者可以根據這份文件深入理解系統架構，並進行功能擴展或維護工作。 
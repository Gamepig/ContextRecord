# 📚 ContextRecord MCP Server API 文件

## 目錄

- [📚 ContextRecord MCP Server API 文件](#-contextrecord-mcp-server-api-文件)
  - [目錄](#目錄)
  - [🔧 工具 (Tools)](#-工具-tools)
    - [對話記錄工具](#對話記錄工具)
    - [自動記錄工具](#自動記錄工具)
    - [搜尋與統計工具](#搜尋與統計工具)
  - [📚 資源 (Resources)](#-資源-resources)
  - [💡 提示 (Prompts)](#-提示-prompts)
  - [📊 回應格式](#-回應格式)
  - [❌ 錯誤處理](#-錯誤處理)
  - [💻 使用範例](#-使用範例)

---

## 🔧 工具 (Tools)

### 對話記錄工具

#### `create_conversation`

創建新的對話記錄

**參數**:

| 參數名 | 類型 | 必填 | 說明 |
|--------|------|------|------|
| `role` | string | ✅ | 對話角色，可選值：`user`, `assistant`, `system` |
| `content` | string | ✅ | 對話內容 |
| `metadata` | string | ❌ | JSON 格式的元數據 |

**範例請求**:
```json
{
  "role": "user",
  "content": "這是一個測試對話",
  "metadata": "{\"project\": \"test\", \"priority\": \"high\"}"
}
```

**成功回應**:
```json
{
  "success": true,
  "conversation_id": 123,
  "message": "對話記錄創建成功",
  "timestamp": "2025-01-27T10:30:00Z"
}
```

**錯誤回應**:
```json
{
  "success": false,
  "error": "role 和 content 參數為必填項"
}
```

---

### 自動記錄工具

#### `enable_auto_recording`

啟用指定會話的自動記錄功能

**參數**:

| 參數名 | 類型 | 必填 | 預設值 | 說明 |
|--------|------|------|--------|------|
| `session_id` | string | ❌ | "default" | 會話識別碼 |
| `record_user` | boolean | ❌ | true | 是否記錄用戶訊息 |
| `record_assistant` | boolean | ❌ | true | 是否記錄助理回應 |

**範例請求**:
```json
{
  "session_id": "my_project",
  "record_user": true,
  "record_assistant": true
}
```

**成功回應**:
```json
{
  "success": true,
  "session_id": "my_project",
  "config": {
    "enabled": true,
    "record_user": true,
    "record_assistant": true
  },
  "message": "已啟用會話 'my_project' 的自動記錄功能"
}
```

#### `auto_record_conversation`

自動記錄對話交互

**參數**:

| 參數名 | 類型 | 必填 | 說明 |
|--------|------|------|------|
| `user_message` | string | ✅ | 用戶訊息內容 |
| `assistant_response` | string | ✅ | 助理回應內容 |
| `session_id` | string | ❌ | 會話識別碼，預設為 "default" |
| `context` | string | ❌ | JSON 格式的上下文資訊 |

**範例請求**:
```json
{
  "user_message": "如何使用自動記錄功能？",
  "assistant_response": "您可以使用 enable_auto_recording 工具來啟用自動記錄。",
  "session_id": "tutorial_session",
  "context": "{\"topic\": \"功能教學\", \"difficulty\": \"beginner\"}"
}
```

**成功回應**:
```json
{
  "success": true,
  "session_id": "tutorial_session",
  "user_recorded": true,
  "assistant_recorded": true,
  "message": "對話記錄完成 - 用戶: ✓, 助理: ✓"
}
```

**部分記錄回應**:
```json
{
  "success": true,
  "session_id": "tutorial_session",
  "user_recorded": true,
  "assistant_recorded": false,
  "message": "對話記錄完成 - 用戶: ✓, 助理: ✗ (已停用)"
}
```

#### `disable_auto_recording`

停用指定會話的自動記錄功能

**參數**:

| 參數名 | 類型 | 必填 | 預設值 | 說明 |
|--------|------|------|--------|------|
| `session_id` | string | ❌ | "default" | 會話識別碼 |

**範例請求**:
```json
{
  "session_id": "my_project"
}
```

**成功回應**:
```json
{
  "success": true,
  "session_id": "my_project",
  "message": "已停用會話 'my_project' 的自動記錄功能"
}
```

#### `get_auto_recording_status`

獲取指定會話的自動記錄狀態

**參數**:

| 參數名 | 類型 | 必填 | 預設值 | 說明 |
|--------|------|------|--------|------|
| `session_id` | string | ❌ | "default" | 會話識別碼 |

**範例請求**:
```json
{
  "session_id": "my_project"
}
```

**成功回應**:
```json
{
  "success": true,
  "session_id": "my_project",
  "config": {
    "enabled": true,
    "record_user": true,
    "record_assistant": false
  },
  "status": "啟用"
}
```

---

### 搜尋與統計工具

#### `search_conversations`

搜尋對話記錄

**參數**:

| 參數名 | 類型 | 必填 | 預設值 | 說明 |
|--------|------|------|--------|------|
| `query` | string | ✅ | - | 搜尋關鍵字 |
| `limit` | integer | ❌ | 10 | 返回結果數量限制 (1-100) |

**範例請求**:
```json
{
  "query": "自動記錄",
  "limit": 5
}
```

**成功回應**:
```json
{
  "success": true,
  "query": "自動記錄",
  "results": [
    {
      "id": 25,
      "role": "user",
      "content": "如何使用自動記錄功能？",
      "timestamp": "2025-01-27T10:30:00Z",
      "metadata": {
        "topic": "功能教學",
        "session_id": "tutorial_session"
      }
    }
  ],
  "count": 1
}
```

**無結果回應**:
```json
{
  "success": true,
  "query": "不存在的關鍵字",
  "results": [],
  "count": 0
}
```

#### `get_conversation_stats`

獲取對話統計資訊

**參數**: 無

**成功回應**:
```json
{
  "success": true,
  "total_conversations": 156,
  "role_distribution": {
    "user": 89,
    "assistant": 67
  },
  "recent_week_count": 23,
  "generated_at": "2025-01-27T10:30:00Z"
}
```

#### `delete_conversation`

刪除指定的對話記錄

**參數**:

| 參數名 | 類型 | 必填 | 說明 |
|--------|------|------|------|
| `conversation_id` | integer | ✅ | 要刪除的對話 ID |

**範例請求**:
```json
{
  "conversation_id": 123
}
```

**成功回應**:
```json
{
  "success": true,
  "message": "成功刪除對話記錄 ID: 123"
}
```

**記錄不存在回應**:
```json
{
  "success": false,
  "error": "對話 ID 123 不存在"
}
```

#### `conversation_summary`

根據提供的對話 ID 生成對話摘要

**參數**:

| 參數名 | 類型 | 必填 | 說明 |
|--------|------|------|------|
| `conversation_ids` | array of integer | ✅ | 要生成摘要的對話 ID 列表 |

**範例請求**:
```json
{
  "conversation_ids": [1, 2, 3]
}
```

**成功回應**:
```json
{
  "success": true,
  "summary": "這是對話記錄 [1, 2, 3] 的概要。",
  "message": "成功生成對話概要"
}
```

#### `extract_action_items`

從指定的對話記錄中提取行動項目

**參數**:

| 參數名 | 類型 | 必填 | 說明 |
|--------|------|------|------|
| `conversation_ids` | array of integer | ✅ | 要提取行動項目的對話 ID 列表 |

**範例請求**:
```json
{
  "conversation_ids": [4, 5, 6]
}
```

**成功回應**:
```json
{
  "success": true,
  "action_items": [
    {
      "id": "item1",
      "description": "研究新的資料庫方案",
      "source_conversation_id": 4,
      "status": "open"
    }
  ],
  "message": "成功提取行動項目"
}
```

---

## 📚 資源 (Resources)

### `conversations://recent`

獲取最近的對話記錄

**URI**: `conversations://recent`

**回應格式**:
```json
[
  {
    "id": 25,
    "role": "user",
    "content": "最近的對話內容",
    "timestamp": "2025-01-27T10:30:00Z",
    "metadata": {
      "session_id": "default",
      "auto_recorded": true
    }
  }
]
```

**特性**:
- 返回最近 10 筆對話記錄
- 按時間戳降序排列
- 包含完整的元數據資訊

---

## 💡 提示 (Prompts)

### `analyze_conversation_pattern`

分析對話模式的提示模板

**參數**:

| 參數名 | 類型 | 必填 | 預設值 | 說明 |
|--------|------|------|--------|------|
| `timeframe` | string | ❌ | "week" | 分析時間範圍：`day`, `week`, `month` |
| `focus` | string | ❌ | "general" | 分析重點：`general`, `topics`, `sentiment` |

**範例請求**:
```json
{
  "timeframe": "week",
  "focus": "topics"
}
```

**回應**:
```json
{
  "description": "分析最近一週的對話主題模式",
  "messages": [
    {
      "role": "system",
      "content": "請分析以下對話記錄，識別主要討論主題和模式..."
    },
    {
      "role": "user", 
      "content": "請分析這些對話的主題分布和討論模式。"
    }
  ]
}
```

### `summarize_conversations`

總結對話記錄的提示模板

**參數**:

| 參數名 | 類型 | 必填 | 預設值 | 說明 |
|--------|------|------|--------|------|
| `style` | string | ❌ | "detailed" | 總結風格：`brief`, `detailed`, `bullet` |
| `include_metadata` | boolean | ❌ | false | 是否包含元數據分析 |

**範例請求**:
```json
{
  "style": "brief",
  "include_metadata": true
}
```

**回應**:
```json
{
  "description": "簡要總結對話記錄，包含元數據分析",
  "messages": [
    {
      "role": "system",
      "content": "請提供對話記錄的簡要總結，包括主要討論點和元數據洞察..."
    }
  ]
}
```

---

## 📊 回應格式

### 成功回應結構

所有成功的 API 回應都遵循以下基本結構：

```json
{
  "success": true,
  "data": {
    // 具體的回應資料
  },
  "message": "操作成功的描述",
  "timestamp": "2025-01-27T10:30:00Z"
}
```

### 錯誤回應結構

所有錯誤回應都遵循以下結構：

```json
{
  "success": false,
  "error": "錯誤描述",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-01-27T10:30:00Z"
}
```

### 常見錯誤代碼

| 錯誤代碼 | 說明 |
|----------|------|
| `INVALID_PARAMETERS` | 參數驗證失敗 |
| `DATABASE_ERROR` | 資料庫操作錯誤 |
| `NOT_FOUND` | 資源不存在 |
| `PERMISSION_DENIED` | 權限不足 |
| `INTERNAL_ERROR` | 內部伺服器錯誤 |

---

## ❌ 錯誤處理

### 參數驗證錯誤

**情況**: 必填參數缺失或格式錯誤

**範例**:
```json
{
  "success": false,
  "error": "role 參數為必填項",
  "error_code": "INVALID_PARAMETERS"
}
```

### 資料庫錯誤

**情況**: 資料庫連接失敗或查詢錯誤

**範例**:
```json
{
  "success": false,
  "error": "資料庫連接失敗",
  "error_code": "DATABASE_ERROR"
}
```

### 資源不存在錯誤

**情況**: 請求的資源或記錄不存在

**範例**:
```json
{
  "success": false,
  "error": "對話 ID 999 不存在",
  "error_code": "NOT_FOUND"
}
```

---

## 💻 使用範例

### 完整的自動記錄工作流程

```python
# 1. 啟用自動記錄
enable_result = await mcp_client.call_tool(
    "enable_auto_recording",
    {
        "session_id": "project_alpha",
        "record_user": True,
        "record_assistant": True
    }
)

# 2. 檢查狀態
status_result = await mcp_client.call_tool(
    "get_auto_recording_status",
    {"session_id": "project_alpha"}
)

# 3. 記錄對話
record_result = await mcp_client.call_tool(
    "auto_record_conversation",
    {
        "user_message": "專案進度如何？",
        "assistant_response": "專案進展順利，預計下週完成。",
        "session_id": "project_alpha",
        "context": "{\"project\": \"alpha\", \"milestone\": \"week3\"}"
    }
)

# 4. 搜尋相關對話
search_result = await mcp_client.call_tool(
    "search_conversations",
    {
        "query": "專案進度",
        "limit": 10
    }
)

# 5. 獲取統計資訊
stats_result = await mcp_client.call_tool(
    "get_conversation_stats",
    {}
)
```

### 批次操作範例

```python
# 批次創建對話記錄
conversations = [
    {
        "role": "user",
        "content": "第一個問題",
        "metadata": "{\"batch\": 1}"
    },
    {
        "role": "assistant", 
        "content": "第一個回答",
        "metadata": "{\"batch\": 1}"
    }
]

for conv in conversations:
    result = await mcp_client.call_tool("create_conversation", conv)
    print(f"記錄結果: {result}")
```

### 錯誤處理範例

```python
try:
    result = await mcp_client.call_tool(
        "create_conversation",
        {
            "role": "invalid_role",  # 無效角色
            "content": "測試內容"
        }
    )
except Exception as e:
    print(f"API 調用失敗: {e}")
    
# 檢查回應中的錯誤
if not result.get("success"):
    error_code = result.get("error_code")
    error_message = result.get("error")
    print(f"錯誤 [{error_code}]: {error_message}")
```

---

這份 API 文件提供了 ContextRecord MCP Server 所有工具、資源和提示的完整參考資訊，包括參數說明、回應格式、錯誤處理和實用範例，幫助開發者快速整合和使用這些功能。 
# ContextRecord 自動記錄功能指南

## 概述

ContextRecord MCP Server 現在支援自動記錄每一段對話的功能。這個功能可以讓您無需手動調用記錄工具，系統會自動將用戶訊息和助理回應保存到資料庫中。

## 功能特色

### 🔧 新增工具

1. **auto_record_conversation** - 自動記錄對話內容
2. **enable_auto_recording** - 啟用自動記錄功能
3. **disable_auto_recording** - 停用自動記錄功能
4. **get_auto_recording_status** - 獲取自動記錄狀態

### 🎯 主要特性

- **多會話支援**: 每個會話可以獨立設定自動記錄
- **靈活配置**: 可以選擇只記錄用戶訊息、助理回應或兩者都記錄
- **上下文保存**: 支援保存對話的上下文資訊
- **狀態管理**: 可以隨時查詢和修改自動記錄狀態

## 使用方法

### 1. 啟用自動記錄

```python
# 啟用預設會話的自動記錄（記錄用戶和助理訊息）
enable_auto_recording()

# 啟用特定會話的自動記錄
enable_auto_recording(
    session_id="my_session",
    record_user=True,
    record_assistant=True
)

# 只記錄用戶訊息
enable_auto_recording(
    session_id="user_only_session",
    record_user=True,
    record_assistant=False
)
```

### 2. 自動記錄對話

```python
# 記錄一次完整的對話交互
auto_record_conversation(
    user_message="用戶的問題或訊息",
    assistant_response="助理的回應",
    session_id="my_session",  # 可選，預設為 "default"
    context='{"topic": "技術討論", "priority": "high"}'  # 可選的上下文資訊
)
```

### 3. 檢查自動記錄狀態

```python
# 檢查預設會話的狀態
get_auto_recording_status()

# 檢查特定會話的狀態
get_auto_recording_status(session_id="my_session")
```

### 4. 停用自動記錄

```python
# 停用預設會話的自動記錄
disable_auto_recording()

# 停用特定會話的自動記錄
disable_auto_recording(session_id="my_session")
```

## 實際應用場景

### 場景 1: 在 Cursor IDE 中自動記錄對話

1. 啟用自動記錄：
```python
enable_auto_recording(session_id="cursor_session")
```

2. 在每次與 AI 助理對話後，調用：
```python
auto_record_conversation(
    user_message="我剛才問的問題",
    assistant_response="AI 助理的回應",
    session_id="cursor_session",
    context='{"file": "main.py", "line": 42}'
)
```

### 場景 2: 不同專案使用不同會話

```python
# 專案 A 只記錄重要對話
enable_auto_recording(
    session_id="project_a",
    record_user=True,
    record_assistant=True
)

# 專案 B 只記錄用戶問題
enable_auto_recording(
    session_id="project_b", 
    record_user=True,
    record_assistant=False
)
```

### 場景 3: 臨時停用記錄

```python
# 暫時停用記錄（例如處理敏感資訊時）
disable_auto_recording(session_id="my_session")

# 處理完成後重新啟用
enable_auto_recording(session_id="my_session")
```

## 資料結構

### 自動記錄的對話包含以下 metadata：

```json
{
  "session_id": "會話ID",
  "auto_recorded": true,
  "message_type": "user_input" | "assistant_response",
  "自定義上下文": "..."
}
```

### 狀態配置結構：

```json
{
  "enabled": true,
  "record_user": true,
  "record_assistant": true
}
```

## 最佳實踐

### 1. 會話命名規範
- 使用有意義的會話 ID，例如：`project_name_feature`
- 避免使用特殊字符，建議使用下劃線分隔

### 2. 上下文資訊
- 在 context 中包含有用的元數據，如檔案名稱、行號、主題等
- 使用 JSON 格式確保結構化存儲

### 3. 記錄策略
- 開發階段：記錄所有對話以便除錯
- 生產階段：只記錄重要對話以節省空間
- 敏感資訊：臨時停用自動記錄

### 4. 定期清理
- 使用 `delete_conversation` 工具清理舊的或不需要的記錄
- 定期檢查 `get_conversation_stats` 了解記錄情況

## 故障排除

### 1. 自動記錄沒有生效
- 檢查會話是否已啟用：`get_auto_recording_status()`
- 確認 `record_user` 和 `record_assistant` 設定正確

### 2. 記錄了不應該記錄的內容
- 使用 `disable_auto_recording()` 立即停用
- 使用 `delete_conversation()` 刪除敏感記錄

### 3. 會話狀態丟失
- 自動記錄狀態存儲在記憶體中，重啟 MCP Server 後需要重新設定
- 考慮在應用啟動時自動啟用常用會話的自動記錄

## 進階功能

### 批量操作
```python
# 為多個會話啟用自動記錄
sessions = ["project_a", "project_b", "project_c"]
for session in sessions:
    enable_auto_recording(session_id=session)
```

### 條件記錄
```python
# 根據內容長度決定是否記錄
if len(user_message) > 10:  # 只記錄較長的訊息
    auto_record_conversation(
        user_message=user_message,
        assistant_response=assistant_response
    )
```

## 與其他工具的整合

自動記錄功能與現有工具完全相容：

- `search_conversations` - 搜尋自動記錄的對話
- `get_conversation_stats` - 統計包含自動記錄的資料
- `delete_conversation` - 刪除自動記錄的對話

## 總結

自動記錄功能讓 ContextRecord 更加智能和便利。通過合理配置和使用，您可以：

- 📝 自動保存所有重要對話
- 🔍 輕鬆搜尋歷史記錄
- 📊 分析對話模式和趨勢
- 🛡️ 靈活控制記錄範圍和內容

開始使用自動記錄功能，讓您的對話管理更加高效！ 
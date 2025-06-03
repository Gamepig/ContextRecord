# 🤝 貢獻指南

感謝您對 ContextRecord MCP Server 的關注！我們歡迎所有形式的貢獻，包括但不限於：

- 🐛 錯誤報告
- 💡 功能建議
- 📝 文件改善
- 🔧 程式碼貢獻
- 🧪 測試改善

## 📋 目錄

- [🤝 貢獻指南](#-貢獻指南)
  - [📋 目錄](#-目錄)
  - [🚀 快速開始](#-快速開始)
  - [🐛 報告問題](#-報告問題)
  - [💡 功能請求](#-功能請求)
  - [🔧 程式碼貢獻](#-程式碼貢獻)
    - [開發環境設定](#開發環境設定)
    - [分支策略](#分支策略)
    - [程式碼規範](#程式碼規範)
    - [提交規範](#提交規範)
  - [🧪 測試](#-測試)
  - [📝 文件](#-文件)
  - [🔍 程式碼審查](#-程式碼審查)
  - [📦 發布流程](#-發布流程)
  - [❓ 獲得幫助](#-獲得幫助)

---

## 🚀 快速開始

1. **Fork 專案**
   ```bash
   # 在 GitHub 上 Fork 專案
   # 然後克隆您的 Fork
   git clone https://github.com/yourusername/ContextRecord.git
   cd ContextRecord
   ```

2. **設定開發環境**
   ```bash
   # 創建虛擬環境
   uv venv
   source .venv/bin/activate
   
   # 安裝依賴
   uv pip install -r requirements.txt
   ```

3. **創建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **進行開發**
   - 編寫程式碼
   - 添加測試
   - 更新文件

5. **提交變更**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

6. **創建 Pull Request**
   - 在 GitHub 上創建 PR
   - 填寫 PR 模板
   - 等待審查

---

## 🐛 報告問題

在報告問題之前，請：

1. **搜尋現有 Issues** - 確認問題尚未被報告
2. **使用最新版本** - 確認問題在最新版本中仍然存在
3. **提供詳細資訊** - 使用我們的 Issue 模板

### Issue 模板

```markdown
## 問題描述
簡要描述遇到的問題。

## 重現步驟
1. 執行 '...'
2. 點擊 '....'
3. 滾動到 '....'
4. 看到錯誤

## 預期行為
描述您期望發生的行為。

## 實際行為
描述實際發生的行為。

## 環境資訊
- OS: [例如 macOS 15.0]
- Python 版本: [例如 3.13.0]
- ContextRecord 版本: [例如 1.0.0]
- Cursor IDE 版本: [例如 0.42.0]

## 額外資訊
添加任何其他有助於解決問題的資訊。
```

---

## 💡 功能請求

我們歡迎新功能的建議！請：

1. **檢查現有 Issues** - 確認功能尚未被請求
2. **描述使用場景** - 解釋為什麼需要這個功能
3. **提供詳細規格** - 描述功能應該如何工作

### 功能請求模板

```markdown
## 功能描述
簡要描述您希望添加的功能。

## 問題解決
這個功能解決了什麼問題？

## 建議解決方案
描述您希望的實現方式。

## 替代方案
描述您考慮過的其他解決方案。

## 額外資訊
添加任何其他相關資訊或截圖。
```

---

## 🔧 程式碼貢獻

### 開發環境設定

詳細的開發環境設定請參考 [開發指南](docs/DEVELOPMENT.md)。

### 分支策略

我們使用 **Git Flow** 分支策略：

- `main` - 穩定的生產版本
- `develop` - 開發分支
- `feature/*` - 功能分支
- `bugfix/*` - 錯誤修復分支
- `hotfix/*` - 緊急修復分支

### 程式碼規範

#### Python 風格指南

- 遵循 **PEP 8** 標準
- 使用 **Black** 進行程式碼格式化
- 使用 **isort** 排序 import 語句
- 使用 **type hints** 進行類型註解

#### 程式碼品質檢查

```bash
# 格式化程式碼
black src/ tests/
isort src/ tests/

# 檢查程式碼品質
pylint src/
flake8 src/ tests/

# 類型檢查
mypy src/
```

#### 命名規範

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

# 私有成員：前綴 _
def _internal_function():
    pass
```

### 提交規範

我們使用 **Conventional Commits** 規範：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 提交類型

- `feat`: 新功能
- `fix`: 錯誤修復
- `docs`: 文件更新
- `style`: 程式碼格式調整（不影響功能）
- `refactor`: 程式碼重構
- `test`: 測試相關
- `chore`: 建構工具或輔助工具的變動
- `perf`: 效能改善
- `ci`: CI/CD 相關變更

#### 提交範例

```bash
# 新功能
git commit -m "feat(tools): add conversation export functionality"

# 錯誤修復
git commit -m "fix(database): resolve connection timeout issue"

# 文件更新
git commit -m "docs(api): update tool parameter descriptions"

# 重構
git commit -m "refactor(server): simplify error handling logic"
```

---

## 🧪 測試

### 測試要求

- **所有新功能必須包含測試**
- **錯誤修復必須包含回歸測試**
- **測試覆蓋率應保持在 90% 以上**

### 測試類型

1. **單元測試** - 測試個別函數
2. **整合測試** - 測試組件互動
3. **端到端測試** - 測試完整工作流程

### 執行測試

```bash
# 執行所有測試
python -m pytest tests/ -v

# 執行特定測試
python -m pytest tests/test_specific.py

# 生成覆蓋率報告
python -m pytest tests/ --cov=src --cov-report=html
```

### 測試範例

```python
import pytest
import asyncio
from src.mcp_server import handle_call_tool

class TestConversationTools:
    @pytest.mark.asyncio
    async def test_create_conversation_success(self):
        """測試成功創建對話"""
        result = await handle_call_tool(
            "create_conversation",
            {
                "role": "user",
                "content": "測試內容",
                "metadata": '{"test": true}'
            }
        )
        
        assert len(result) == 1
        data = json.loads(result[0].text)
        assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_create_conversation_invalid_role(self):
        """測試無效角色錯誤"""
        with pytest.raises(ValueError, match="role 必須為"):
            await handle_call_tool(
                "create_conversation",
                {
                    "role": "invalid",
                    "content": "測試內容"
                }
            )
```

---

## 📝 文件

### 文件要求

- **所有公開 API 必須有文件**
- **複雜邏輯必須有註解**
- **README 和 API 文件必須保持最新**

### 文件類型

1. **程式碼註解** - 解釋複雜邏輯
2. **Docstring** - 函數和類別說明
3. **API 文件** - 工具和資源說明
4. **使用者指南** - 使用範例和教學

### Docstring 格式

```python
def create_conversation(role: str, content: str, metadata: str = None) -> dict:
    """
    創建新的對話記錄
    
    Args:
        role: 對話角色，可選值為 'user', 'assistant', 'system'
        content: 對話內容，不能為空
        metadata: JSON 格式的元數據，可選
    
    Returns:
        dict: 包含操作結果的字典
        {
            "success": bool,
            "conversation_id": int,
            "message": str
        }
        
    Raises:
        ValueError: 當參數無效時
        DatabaseError: 當資料庫操作失敗時
        
    Example:
        >>> result = create_conversation("user", "Hello world")
        >>> print(result["success"])
        True
    """
```

---

## 🔍 程式碼審查

### 審查流程

1. **自我審查** - 提交前檢查自己的程式碼
2. **自動檢查** - CI/CD 自動執行測試和檢查
3. **同儕審查** - 至少一位維護者審查
4. **修改回應** - 根據審查意見進行修改

### 審查重點

#### 功能性
- [ ] 功能是否正確實現
- [ ] 是否處理了邊界情況
- [ ] 錯誤處理是否適當

#### 程式碼品質
- [ ] 程式碼是否清晰易讀
- [ ] 是否遵循專案規範
- [ ] 是否有適當的註解

#### 測試
- [ ] 是否包含足夠的測試
- [ ] 測試是否覆蓋主要場景
- [ ] 測試是否通過

#### 效能
- [ ] 是否有效能問題
- [ ] 資源使用是否合理
- [ ] 是否有記憶體洩漏

#### 安全性
- [ ] 是否有安全漏洞
- [ ] 輸入驗證是否充分
- [ ] 敏感資料是否適當處理

### 審查回應

- **及時回應** - 在 24 小時內回應審查意見
- **建設性討論** - 開放討論設計決策
- **學習態度** - 將審查視為學習機會

---

## 📦 發布流程

### 版本號規則

我們使用 **語義化版本** (Semantic Versioning)：

- `MAJOR.MINOR.PATCH`
- `MAJOR` - 不相容的 API 變更
- `MINOR` - 向後相容的功能新增
- `PATCH` - 向後相容的錯誤修復

### 發布步驟

1. **更新版本號**
2. **更新 CHANGELOG.md**
3. **創建 Release PR**
4. **合併到 main 分支**
5. **創建 Git Tag**
6. **發布 GitHub Release**

### CHANGELOG 格式

```markdown
## [1.2.0] - 2025-01-27

### Added
- 新增對話匯出功能
- 支援 CSV 格式匯出

### Changed
- 改善搜尋效能
- 更新 API 文件

### Fixed
- 修復資料庫連接問題
- 解決記憶體洩漏

### Deprecated
- 舊版 API 將在 v2.0 中移除

### Removed
- 移除已棄用的功能

### Security
- 修復 SQL 注入漏洞
```

---

## ❓ 獲得幫助

如果您在貢獻過程中遇到問題，可以：

1. **查看文件** - 檢查 [開發指南](docs/DEVELOPMENT.md)
2. **搜尋 Issues** - 查看是否有類似問題
3. **創建 Discussion** - 在 GitHub Discussions 中提問
4. **聯繫維護者** - 透過 Issue 或 Email 聯繫

### 聯繫方式

- **GitHub Issues** - 技術問題和錯誤報告
- **GitHub Discussions** - 一般討論和問題
- **Email** - 私人或敏感問題

---

## 🙏 致謝

感謝所有為 ContextRecord 做出貢獻的開發者！您的貢獻讓這個專案變得更好。

### 貢獻者

- 查看 [Contributors](https://github.com/yourusername/ContextRecord/graphs/contributors) 頁面

### 特別感謝

- [Model Context Protocol](https://modelcontextprotocol.io/) 團隊
- [Cursor IDE](https://cursor.sh/) 團隊
- 所有提供回饋和建議的使用者

---

**再次感謝您的貢獻！** 🎉 
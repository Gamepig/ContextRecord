import pytest
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy import select

from src.main import app
from src.models import Conversation
from src.database import Base

# 測試資料
test_conversation = {
    "role": "user",
    "content": "這是一條測試對話",
    "extra_metadata": {"test_key": "test_value"},
}


# 測試建立對話記錄
@pytest.mark.asyncio
async def test_create_conversation(client):
    response = client.post("/api/conversations/", json=test_conversation)
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == test_conversation["role"]
    assert data["content"] == test_conversation["content"]
    assert data["extra_metadata"] == test_conversation["extra_metadata"]
    assert "id" in data
    assert "timestamp" in data


# 測試獲取所有對話
@pytest.mark.asyncio
async def test_get_all_conversations(client):
    # 先創建一條對話記錄
    client.post("/api/conversations/", json=test_conversation)

    # 獲取所有對話
    response = client.get("/api/conversations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# 測試根據ID獲取對話
@pytest.mark.asyncio
async def test_get_conversation_by_id(client):
    # 先創建一條對話記錄
    create_response = client.post("/api/conversations/", json=test_conversation)
    conversation_id = create_response.json()["id"]

    # 獲取該對話
    response = client.get(f"/api/conversations/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation_id
    assert data["role"] == test_conversation["role"]
    assert data["content"] == test_conversation["content"]


# 測試搜尋功能
@pytest.mark.asyncio
async def test_search_conversations(client):
    # 創建一些測試數據
    client.post(
        "/api/conversations/",
        json={
            "role": "user",
            "content": "這是一個搜尋測試對話",
        },
    )
    client.post(
        "/api/conversations/",
        json={
            "role": "assistant",
            "content": "這是另一個對話，不包含搜尋關鍵字",
        },
    )

    # 測試搜尋功能
    response = client.get("/api/search/", params={"query": "搜尋"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "搜尋" in data[0]["content"]

    # 測試沒有匹配結果的情況
    response = client.get("/api/search/", params={"query": "不存在的關鍵字xyz123"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

import pytest
from fastapi.testclient import TestClient

from src.main import app

def test_read_root(client):
    """測試根路徑回應是否正確"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

# 以下是資料庫相關的API測試
# 在實現相關路由後可以取消註解

# @pytest.mark.asyncio
# async def test_create_conversation_api(client, db_session):
#     """測試建立對話API"""
#     response = client.post(
#         "/conversations/",
#         json={
#             "role": "user",
#             "content": "API測試訊息",
#             "extra_metadata": {"source": "api_test"}
#         }
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["role"] == "user"
#     assert data["content"] == "API測試訊息"
#     assert data["extra_metadata"] == {"source": "api_test"}

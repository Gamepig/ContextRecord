import pytest
from fastapi.testclient import TestClient
import json
from datetime import datetime

from src.main import app
from src.models import Conversation
from src.functions.server import register_tool

# 創建測試客戶端
client = TestClient(app)

def test_server_root():
    """測試伺服器根端點是否正常工作"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_tools_list_endpoint():
    """測試工具列表端點是否可訪問"""
    # 註冊一個測試工具
    async def test_tool_handler(param1: str, param2: int = 0):
        return {"result": f"{param1}-{param2}"}
    
    register_tool(
        name="test_tool_list",
        description="A test tool for testing list endpoint",
        handler_func=test_tool_handler
    )
    
    response = client.get("/api/tools/list")
    assert response.status_code == 200
    
    # 確認響應是有效的JSON
    tools = response.json()
    assert isinstance(tools, list)
    
    # 檢查我們的測試工具是否在列表中
    test_tool = next((tool for tool in tools if tool["name"] == "test_tool_list"), None)
    assert test_tool is not None
    assert test_tool["description"] == "A test tool for testing list endpoint"

def test_tool_call_endpoint():
    """測試工具呼叫端點是否可訪問"""
    # 註冊一個測試工具
    async def echo_tool(message: str):
        return {"echo": message}
    
    register_tool(
        name="echo_tool",
        description="A tool that echoes back the message",
        handler_func=echo_tool
    )
    
    tool_call_data = {
        "tool_name": "echo_tool",
        "parameters": {"message": "Hello, World!"},
        "request_id": "test-123"
    }
    
    response = client.post("/api/tools/call", json=tool_call_data)
    assert response.status_code == 200
    
    result = response.json()
    assert result["request_id"] == "test-123"
    assert result["result"]["echo"] == "Hello, World!"
    assert result["error"] is None 
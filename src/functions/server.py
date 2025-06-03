from fastapi import APIRouter, Request, Response, BackgroundTasks, HTTPException, Depends
from fastapi.responses import StreamingResponse
import asyncio
from typing import AsyncGenerator, Dict, List, Any, Optional
import json
from datetime import datetime, UTC, timezone
from pydantic import BaseModel, Field

# 創建一個路由器來處理SSE事件
router = APIRouter()

# 使用一個簡單的事件隊列和連接管理器
class EventManager:
    def __init__(self):
        self.clients: List[asyncio.Queue] = []
        self._lock = asyncio.Lock()
    
    async def register(self) -> asyncio.Queue:
        """註冊一個新的客戶端，返回客戶端的事件隊列"""
        queue = asyncio.Queue()
        async with self._lock:
            self.clients.append(queue)
        return queue
    
    async def unregister(self, queue: asyncio.Queue) -> None:
        """從事件管理器中移除客戶端"""
        async with self._lock:
            if queue in self.clients:
                self.clients.remove(queue)
    
    async def broadcast(self, event: Dict[str, Any]) -> None:
        """向所有已連接的客戶端廣播事件"""
        # 轉換事件為SSE格式的字符串
        event_str = json.dumps(event)
        message = f"data: {event_str}\n\n"
        
        # 將消息添加到每個客戶端的隊列中
        async with self._lock:
            # 複製客戶端列表，避免在迭代過程中修改列表
            clients = self.clients.copy()
        
        # 向所有客戶端發送消息
        for queue in clients:
            await queue.put(message)
    
    async def broadcast_conversation(self, conversation: Dict[str, Any]) -> None:
        """特定功能：廣播新對話記錄事件"""
        event = {
            "type": "new_conversation",
            "data": conversation,
            "timestamp": datetime.now(UTC).isoformat()
        }
        await self.broadcast(event)

# 創建一個全局事件管理器實例
event_manager = EventManager()

# 定義SSE端點
@router.get("/events/")
async def events(request: Request) -> StreamingResponse:
    """
    SSE端點，客戶端通過此端點訂閱實時事件
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        # 註冊客戶端
        client_queue = await event_manager.register()
        
        # 發送一個初始連接成功消息
        await client_queue.put("data: {\"type\": \"connected\"}\n\n")
        
        try:
            # 持續從隊列中獲取並發送事件
            while True:
                # 等待來自事件管理器的消息
                message = await client_queue.get()
                yield message
                
                # 檢查客戶端是否斷開連接
                if await request.is_disconnected():
                    break
        finally:
            # 客戶端斷開連接時移除它
            await event_manager.unregister(client_queue)
    
    # 返回StreamingResponse，設置正確的內容類型和其他頭部信息
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",  # CORS支持，根據需要調整
        }
    )

# 用於工具呼叫概念設計的模型
class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    request_id: str

class ToolResponse(BaseModel):
    request_id: str
    result: Any
    error: str = None

# 工具註冊表，用於存儲可用工具
tool_registry = {}

# 註冊新工具的函數
def register_tool(name: str, description: str, handler_func: callable):
    """
    註冊一個工具到工具註冊表
    
    參數:
    - name: 工具名稱
    - description: 工具描述
    - handler_func: 工具處理函數，應該是一個異步函數
    """
    tool_registry[name] = {
        "name": name,
        "description": description,
        "handler": handler_func
    }

# 工具呼叫的API端點
@router.post("/tools/call")
async def call_tool(tool_call: ToolCall):
    """
    接收工具呼叫請求，執行相應的工具，並返回結果
    """
    # 檢查工具是否已註冊
    if tool_call.tool_name not in tool_registry:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_call.tool_name}' not found")
    
    try:
        # 獲取工具處理函數
        tool_handler = tool_registry[tool_call.tool_name]["handler"]
        
        # 執行工具處理函數並獲取結果
        result = await tool_handler(**tool_call.parameters)
        
        # 返回工具執行結果
        return ToolResponse(
            request_id=tool_call.request_id,
            result=result
        )
    except Exception as e:
        # 如果執行過程中發生錯誤，返回錯誤信息
        return ToolResponse(
            request_id=tool_call.request_id,
            result=None,
            error=str(e)
        )

# 獲取已註冊工具列表的端點
@router.get("/tools/list")
async def list_tools():
    """
    返回所有已註冊的工具列表
    """
    tools_list = []
    for name, tool_info in tool_registry.items():
        tools_list.append({
            "name": name,
            "description": tool_info["description"]
        })
    
    return {
        "tools": tools_list,
        "total": len(tools_list)
    }

# 延遲註冊對話相關的工具，避免循環導入
def register_conversation_tools():
    """延遲註冊對話相關工具"""
    try:
        from .conversations import (
            create_conversation as create_conv_handler,
            search_conversations as search_conv_handler,
            get_all_conversations as get_all_conv_handler,
            get_conversation as get_conv_handler
        )
        
        # 註冊對話相關的工具
        register_tool(
            name="create_conversation",
            description="創建新的對話記錄",
            handler_func=create_conv_handler
        )

        register_tool(
            name="search_conversations",
            description="搜索對話記錄",
            handler_func=search_conv_handler
        )

        register_tool(
            name="get_all_conversations",
            description="獲取所有對話記錄",
            handler_func=get_all_conv_handler
        )

        register_tool(
            name="get_conversation",
            description="根據ID獲取單個對話記錄",
            handler_func=get_conv_handler
        )
    except ImportError as e:
        print(f"Warning: Could not register conversation tools: {e}") 
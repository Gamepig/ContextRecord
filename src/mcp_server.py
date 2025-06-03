#!/usr/bin/env python3
"""
ContextRecord MCP Server

一個用於記錄和搜尋對話內容的 MCP 伺服器。
提供對話記錄、搜尋和管理功能。
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime, UTC
import json
import sqlite3
import os

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 資料庫設定
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/conversations.db")

# 自動記錄狀態管理
AUTO_RECORDING_SESSIONS = {}  # 存儲每個會話的自動記錄設定

def get_auto_recording_config(session_id: str = "default") -> dict:
    """獲取自動記錄配置"""
    return AUTO_RECORDING_SESSIONS.get(session_id, {
        "enabled": False,
        "record_user": True,
        "record_assistant": True
    })

def set_auto_recording_config(session_id: str = "default", **config) -> None:
    """設定自動記錄配置"""
    if session_id not in AUTO_RECORDING_SESSIONS:
        AUTO_RECORDING_SESSIONS[session_id] = {
            "enabled": False,
            "record_user": True,
            "record_assistant": True
        }
    AUTO_RECORDING_SESSIONS[session_id].update(config)

async def auto_record_message(role: str, content: str, session_id: str = "default", metadata: dict = None) -> bool:
    """自動記錄訊息"""
    config = get_auto_recording_config(session_id)
    
    if not config["enabled"]:
        return False
    
    if role == "user" and not config["record_user"]:
        return False
    
    if role == "assistant" and not config["record_assistant"]:
        return False
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 添加會話 ID 到 metadata
        if metadata is None:
            metadata = {}
        metadata["session_id"] = session_id
        metadata["auto_recorded"] = True
        
        cursor.execute(
            "INSERT INTO conversations (role, content, metadata) VALUES (?, ?, ?)",
            (role, content, json.dumps(metadata))
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"自動記錄 {role} 訊息: {content[:50]}...")
        return True
        
    except Exception as e:
        logger.error(f"自動記錄失敗: {e}")
        return False

def init_database():
    """初始化資料庫"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def get_db_connection():
    """獲取資料庫連接"""
    return sqlite3.connect(DATABASE_PATH)

# 創建 MCP 伺服器
server = Server("contextrecord")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """列出可用的資源"""
    return [
        types.Resource(
            uri="conversations://recent",
            name="Recent Conversations",
            description="最近的對話記錄",
            mimeType="application/json",
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: types.AnyUrl) -> str:
    """讀取資源內容"""
    if str(uri) == "conversations://recent":
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, role, content, timestamp, metadata FROM conversations ORDER BY timestamp DESC LIMIT 10"
            )
            
            rows = cursor.fetchall()
            conn.close()
            
            conversations = []
            for row in rows:
                conversations.append({
                    "id": row[0],
                    "role": row[1],
                    "content": row[2],
                    "timestamp": row[3],
                    "metadata": json.loads(row[4]) if row[4] else None
                })
            
            return json.dumps(conversations, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.error(f"獲取最近對話資源時發生錯誤: {e}")
            return f"錯誤: {str(e)}"
    
    raise ValueError(f"未知的資源: {uri}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """列出可用的工具"""
    return [
        types.Tool(
            name="create_conversation",
            description="創建新的對話記錄",
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "對話角色 (user, assistant, system)"
                    },
                    "content": {
                        "type": "string",
                        "description": "對話內容"
                    },
                    "metadata": {
                        "type": "string",
                        "description": "額外的元數據 (JSON 字串)",
                        "default": None
                    }
                },
                "required": ["role", "content"]
            },
        ),
        types.Tool(
            name="auto_record_conversation",
            description="自動記錄對話內容（用於每次對話交互）",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_message": {
                        "type": "string",
                        "description": "用戶的訊息內容"
                    },
                    "assistant_response": {
                        "type": "string",
                        "description": "助理的回應內容"
                    },
                    "session_id": {
                        "type": "string",
                        "description": "對話會話 ID",
                        "default": None
                    },
                    "context": {
                        "type": "string",
                        "description": "對話上下文資訊 (JSON 字串)",
                        "default": None
                    }
                },
                "required": ["user_message", "assistant_response"]
            },
        ),
        types.Tool(
            name="enable_auto_recording",
            description="啟用自動記錄功能",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "要啟用自動記錄的會話 ID",
                        "default": "default"
                    },
                    "record_user": {
                        "type": "boolean",
                        "description": "是否記錄用戶訊息",
                        "default": True
                    },
                    "record_assistant": {
                        "type": "boolean",
                        "description": "是否記錄助理回應",
                        "default": True
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="disable_auto_recording",
            description="停用自動記錄功能",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "要停用自動記錄的會話 ID",
                        "default": "default"
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_auto_recording_status",
            description="獲取自動記錄狀態",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "要查詢的會話 ID",
                        "default": "default"
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="search_conversations",
            description="搜尋對話記錄",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜尋關鍵字"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回結果數量限制",
                        "default": 10
                    }
                },
                "required": ["query"]
            },
        ),
        types.Tool(
            name="get_conversation_stats",
            description="獲取對話統計資訊",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="delete_conversation",
            description="刪除指定的對話記錄",
            inputSchema={
                "type": "object",
                "properties": {
                    "conversation_id": {
                        "type": "integer",
                        "description": "要刪除的對話 ID"
                    }
                },
                "required": ["conversation_id"]
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """處理工具調用"""
    
    if name == "create_conversation":
        role = arguments.get("role")
        content = arguments.get("content")
        metadata = arguments.get("metadata")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 解析 metadata
            metadata_dict = None
            if metadata:
                try:
                    metadata_dict = json.loads(metadata)
                except json.JSONDecodeError:
                    metadata_dict = {"raw": metadata}
            
            cursor.execute(
                "INSERT INTO conversations (role, content, metadata) VALUES (?, ?, ?)",
                (role, content, json.dumps(metadata_dict) if metadata_dict else None)
            )
            
            conversation_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            result = {
                "success": True,
                "conversation_id": conversation_id,
                "message": f"成功創建對話記錄，ID: {conversation_id}"
            }
            
        except Exception as e:
            logger.error(f"創建對話時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    elif name == "auto_record_conversation":
        user_message = arguments.get("user_message")
        assistant_response = arguments.get("assistant_response")
        session_id = arguments.get("session_id", "default")
        context = arguments.get("context")
        
        try:
            # 解析上下文
            context_dict = None
            if context:
                try:
                    context_dict = json.loads(context)
                except json.JSONDecodeError:
                    context_dict = {"raw": context}
            
            # 記錄用戶訊息
            user_recorded = await auto_record_message(
                "user", 
                user_message, 
                session_id, 
                {**(context_dict or {}), "message_type": "user_input"}
            )
            
            # 記錄助理回應
            assistant_recorded = await auto_record_message(
                "assistant", 
                assistant_response, 
                session_id, 
                {**(context_dict or {}), "message_type": "assistant_response"}
            )
            
            result = {
                "success": True,
                "session_id": session_id,
                "user_recorded": user_recorded,
                "assistant_recorded": assistant_recorded,
                "message": f"對話記錄完成 - 用戶: {'✓' if user_recorded else '✗'}, 助理: {'✓' if assistant_recorded else '✗'}"
            }
            
        except Exception as e:
            logger.error(f"自動記錄對話時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    elif name == "enable_auto_recording":
        session_id = arguments.get("session_id", "default")
        record_user = arguments.get("record_user", True)
        record_assistant = arguments.get("record_assistant", True)
        
        try:
            set_auto_recording_config(
                session_id=session_id,
                enabled=True,
                record_user=record_user,
                record_assistant=record_assistant
            )
            
            result = {
                "success": True,
                "session_id": session_id,
                "config": get_auto_recording_config(session_id),
                "message": f"已啟用會話 '{session_id}' 的自動記錄功能"
            }
            
        except Exception as e:
            logger.error(f"啟用自動記錄時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    elif name == "disable_auto_recording":
        session_id = arguments.get("session_id", "default")
        
        try:
            set_auto_recording_config(session_id=session_id, enabled=False)
            
            result = {
                "success": True,
                "session_id": session_id,
                "message": f"已停用會話 '{session_id}' 的自動記錄功能"
            }
            
        except Exception as e:
            logger.error(f"停用自動記錄時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    elif name == "get_auto_recording_status":
        session_id = arguments.get("session_id", "default")
        
        try:
            config = get_auto_recording_config(session_id)
            
            result = {
                "success": True,
                "session_id": session_id,
                "config": config,
                "status": "啟用" if config["enabled"] else "停用"
            }
            
        except Exception as e:
            logger.error(f"獲取自動記錄狀態時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    elif name == "search_conversations":
        query = arguments.get("query")
        limit = arguments.get("limit", 10)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
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
            
            rows = cursor.fetchall()
            conn.close()
            
            conversations = []
            for row in rows:
                conversations.append({
                    "id": row[0],
                    "role": row[1],
                    "content": row[2],
                    "timestamp": row[3],
                    "metadata": json.loads(row[4]) if row[4] else None
                })
            
            result = {
                "success": True,
                "query": query,
                "results": conversations,
                "count": len(conversations)
            }
            
        except Exception as e:
            logger.error(f"搜尋對話時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    elif name == "get_conversation_stats":
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 總對話數
            cursor.execute("SELECT COUNT(*) FROM conversations")
            total_count = cursor.fetchone()[0]
            
            # 按角色統計
            cursor.execute("SELECT role, COUNT(*) FROM conversations GROUP BY role")
            role_stats = dict(cursor.fetchall())
            
            # 最近一週的對話數
            cursor.execute(
                "SELECT COUNT(*) FROM conversations WHERE timestamp >= datetime('now', '-7 days')"
            )
            recent_count = cursor.fetchone()[0]
            
            conn.close()
            
            result = {
                "success": True,
                "total_conversations": total_count,
                "role_distribution": role_stats,
                "recent_week_count": recent_count
            }
            
        except Exception as e:
            logger.error(f"獲取統計資訊時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    elif name == "delete_conversation":
        conversation_id = arguments.get("conversation_id")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            
            if cursor.rowcount == 0:
                conn.close()
                result = {
                    "success": False,
                    "error": f"對話 ID {conversation_id} 不存在"
                }
            else:
                conn.commit()
                conn.close()
                result = {
                    "success": True,
                    "message": f"成功刪除對話記錄 ID: {conversation_id}"
                }
            
        except Exception as e:
            logger.error(f"刪除對話時發生錯誤: {e}")
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    else:
        raise ValueError(f"未知的工具: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """列出可用的提示"""
    return [
        types.Prompt(
            name="analyze_conversation_pattern",
            description="分析對話模式",
            arguments=[],
        ),
        types.Prompt(
            name="summarize_conversations",
            description="總結對話記錄",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="總結風格 (brief 或 detailed)",
                    required=False,
                )
            ],
        ),
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict | None
) -> types.GetPromptResult:
    """處理提示請求"""
    
    if name == "analyze_conversation_pattern":
        return types.GetPromptResult(
            description="分析對話模式的提示",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="""請分析提供的對話記錄，識別以下模式：

1. 對話流程和結構
2. 常見的問題類型
3. 回應的品質和一致性
4. 可能的改進建議

請提供詳細的分析報告。"""
                    ),
                )
            ],
        )
    
    elif name == "summarize_conversations":
        style = arguments.get("style", "brief") if arguments else "brief"
        
        if style == "detailed":
            messages = [
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="請提供詳細的對話記錄總結，包括："
                    ),
                ),
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="- 主要討論主題\n- 關鍵決策點\n- 未解決的問題\n- 後續行動項目"
                    ),
                ),
            ]
        else:
            messages = [
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="請提供簡潔的對話記錄總結，重點關注主要結論和行動項目。"
                    ),
                )
            ]
        
        return types.GetPromptResult(
            description="總結對話記錄的提示",
            messages=messages,
        )
    
    else:
        raise ValueError(f"未知的提示: {name}")

async def main():
    """主函數"""
    # 初始化資料庫
    init_database()
    logger.info("ContextRecord MCP Server 正在啟動...")
    
    # 運行伺服器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="contextrecord",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 
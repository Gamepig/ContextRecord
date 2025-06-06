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
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Body
from mcp.server.fastmcp import FastMCP
import uvicorn
from pydantic import BaseModel

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 資料庫設定
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/conversations.db")

# 自動記錄狀態管理
AUTO_RECORDING_SESSIONS = {}  # 存儲每個會話的自動記錄設定


def get_auto_recording_config(session_id: str = "default") -> dict:
    """獲取自動記錄配置"""
    return AUTO_RECORDING_SESSIONS.get(
        session_id, {"enabled": False, "record_user": True, "record_assistant": True}
    )


def set_auto_recording_config(session_id: str = "default", **config) -> None:
    """設定自動記錄配置"""
    if session_id not in AUTO_RECORDING_SESSIONS:
        AUTO_RECORDING_SESSIONS[session_id] = {
            "enabled": False,
            "record_user": True,
            "record_assistant": True,
        }
    AUTO_RECORDING_SESSIONS[session_id].update(config)


async def auto_record_message(
    role: str, content: str, session_id: str = "default", metadata: dict = None
) -> bool:
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
            (role, content, json.dumps(metadata)),
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT
        )
    """
    )

    conn.commit()
    conn.close()


def get_db_connection():
    """獲取資料庫連接"""
    return sqlite3.connect(DATABASE_PATH)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 應用程式啟動時執行
    init_database()
    logger.info("ContextRecord MCP Server 正在啟動...")
    yield
    # 應用程式關閉時執行 (如果需要清理資源)
    logger.info("ContextRecord MCP Server 正在關閉...")


# 創建 MCP 伺服器
# server = Server("contextrecord") # 移除原始的 server 實例

app = FastAPI(title="ContextRecord MCP Server", lifespan=lifespan)
mcp_app_instance = FastMCP(
    "contextrecord",
    app=app,
    description="一個用於記錄和搜尋對話內容的 MCP 伺服器。提供對話記錄、搜尋和管理功能。",
)

# 新增標準 FastAPI 端點來提供最近的對話記錄
@app.get("/conversations/recent", operation_id="conversations_recent")
async def get_recent_conversations() -> List[Dict[str, Any]]:
    """獲取最近的對話記錄"""
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
            conversations.append(
                {
                    "id": row[0],
                    "role": row[1],
                    "content": row[2],
                    "timestamp": row[3],
                    "metadata": json.loads(row[4]) if row[4] else None,
                }
            )

        return conversations

    except Exception as e:
        logger.error(f"獲取最近對話資源時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class CreateConversationRequest(BaseModel):
    role: str
    content: str
    metadata: Optional[str] = None


@mcp_app_instance.tool()
@app.post("/tools/create_conversation", operation_id="create_conversation")
async def create_conversation(request: CreateConversationRequest) -> Dict[str, Any]:
    """創建新的對話記錄"""
    logger.info(f"調用工具: create_conversation, 參數: {request.role}, {request.content}, {request.metadata}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 解析 metadata
        metadata_dict = None
        if request.metadata:
            try:
                metadata_dict = json.loads(request.metadata)
            except json.JSONDecodeError:
                metadata_dict = {"raw": request.metadata}

        cursor.execute(
            "INSERT INTO conversations (role, content, metadata) VALUES (?, ?, ?)",
            (request.role, request.content, json.dumps(metadata_dict) if metadata_dict else None),
        )

        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()

        result = {
            "success": True,
            "conversation_id": conversation_id,
            "message": f"成功創建對話記錄，ID: {conversation_id}",
        }

        return result

    except Exception as e:
        logger.error(f"創建對話時發生錯誤: {e}")
        return {"success": False, "error": str(e)}


class AutoRecordConversationRequest(BaseModel):
    user_message: str
    assistant_response: str
    session_id: Optional[str] = None
    context: Optional[str] = None


@mcp_app_instance.tool()
@app.post("/tools/auto_record_conversation", operation_id="auto_record_conversation")
async def auto_record_conversation(request: AutoRecordConversationRequest) -> Dict[str, Any]:
    """自動記錄對話內容（用於每次對話交互）"""
    logger.info(f"調用工具: auto_record_conversation, 參數: {request.user_message}, {request.assistant_response}, {request.session_id}, {request.context}")
    try:
        # 解析上下文
        context_dict = None
        if request.context:
            try:
                context_dict = json.loads(request.context)
            except json.JSONDecodeError:
                context_dict = {"raw": request.context}

        # 記錄用戶訊息
        user_recorded = await auto_record_message(
            "user",
            request.user_message,
            request.session_id,
            metadata=context_dict,
        )

        # 記錄助理回應
        assistant_recorded = await auto_record_message(
            "assistant",
            request.assistant_response,
            request.session_id,
            metadata=context_dict,
        )

        return {"success": user_recorded and assistant_recorded}

    except Exception as e:
        logger.error(f"自動記錄對話時發生錯誤: {e}")
        return {"success": False, "error": str(e)}


class EnableAutoRecordingRequest(BaseModel):
    session_id: Optional[str] = "default"
    record_user: bool = True
    record_assistant: bool = True


@mcp_app_instance.tool()
@app.post("/tools/enable_auto_recording", operation_id="enable_auto_recording")
async def enable_auto_recording(request: EnableAutoRecordingRequest) -> Dict[str, Any]:
    """啟用自動記錄功能"""
    logger.info(f"調用工具: enable_auto_recording, 參數: {request.session_id}, {request.record_user}, {request.record_assistant}")
    try:
        set_auto_recording_config(
            request.session_id,
            enabled=True,
            record_user=request.record_user,
            record_assistant=request.record_assistant,
        )
        return {"success": True, "message": "自動記錄已啟用"}
    except Exception as e:
        logger.error(f"啟用自動記錄時發生錯誤: {e}")
        return {"success": False, "error": str(e)}


class DisableAutoRecordingRequest(BaseModel):
    session_id: Optional[str] = None


@mcp_app_instance.tool()
@app.post("/tools/disable_auto_recording", operation_id="disable_auto_recording")
async def disable_auto_recording(request: DisableAutoRecordingRequest) -> Dict[str, Any]:
    """禁用自動記錄功能"""
    logger.info(f"調用工具: disable_auto_recording, 參數: {request.session_id}")
    try:
        set_auto_recording_config(request.session_id, enabled=False)
        return {"success": True, "message": "自動記錄已禁用"}
    except Exception as e:
        logger.error(f"禁用自動記錄時發生錯誤: {e}")
        return {"success": False, "error": str(e)}


class GetAutoRecordingStatusRequest(BaseModel):
    session_id: Optional[str] = None


@mcp_app_instance.tool()
@app.post("/tools/get_auto_recording_status", operation_id="get_auto_recording_status")
async def get_auto_recording_status(request: GetAutoRecordingStatusRequest) -> Dict[str, Any]:
    """獲取自動記錄狀態"""
    logger.info(f"調用工具: get_auto_recording_status, 參數: {request.session_id}")
    try:
        config = get_auto_recording_config(request.session_id)
        return {"success": True, "status": config}
    except Exception as e:
        logger.error(f"獲取自動記錄狀態時發生錯誤: {e}")
        return {"success": False, "error": str(e)}


class SearchConversationsRequest(BaseModel):
    query: str
    limit: Optional[int] = None


@mcp_app_instance.tool()
@app.post("/tools/search_conversations", operation_id="search_conversations")
async def search_conversations(request: SearchConversationsRequest) -> List[Dict[str, Any]]:
    """搜尋對話記錄"""
    logger.info(f"調用工具: search_conversations, 參數: {request.query}, {request.limit}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 使用 LIKE 進行簡單的內容模糊搜尋
        sql_query = "SELECT id, role, content, timestamp, metadata FROM conversations WHERE content LIKE ? ORDER BY timestamp DESC"
        params = [f"%{request.query}%"]

        if request.limit:
            sql_query += " LIMIT ?"
            params.append(request.limit)

        cursor.execute(sql_query, params)

        rows = cursor.fetchall()
        conn.close()

        conversations = []
        for row in rows:
            conversations.append(
                {
                    "id": row[0],
                    "role": row[1],
                    "content": row[2],
                    "timestamp": row[3],
                    "metadata": json.loads(row[4]) if row[4] else None,
                }
            )
        return conversations

    except Exception as e:
        logger.error(f"搜尋對話記錄時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@mcp_app_instance.tool()
@app.post("/tools/get_conversation_stats", operation_id="get_conversation_stats")
async def get_conversation_stats() -> Dict[str, Any]:
    """獲取對話統計信息"""
    logger.info("調用工具: get_conversation_stats")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM conversations")
        total_conversations = cursor.fetchone()[0]

        cursor.execute("SELECT role, COUNT(*) FROM conversations GROUP BY role")
        role_counts = dict(cursor.fetchall())

        conn.close()

        return {
            "success": True,
            "total_conversations": total_conversations,
            "role_counts": role_counts,
        }

    except Exception as e:
        logger.error(f"獲取對話統計信息時發生錯誤: {e}")
        return {"success": False, "error": str(e)}


class DeleteConversationRequest(BaseModel):
    conversation_id: int


@mcp_app_instance.tool()
@app.post("/tools/delete_conversation", operation_id="delete_conversation")
async def delete_conversation(request: DeleteConversationRequest) -> Dict[str, Any]:
    """刪除指定 ID 的對話記錄"""
    logger.info(f"調用工具: delete_conversation, 參數: {request.conversation_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM conversations WHERE id = ?", (request.conversation_id,))
        conn.commit()

        if cursor.rowcount > 0:
            result = {"success": True, "message": f"成功刪除對話記錄 ID: {request.conversation_id}"}
        else:
            result = {"success": False, "message": f"未找到對話記錄 ID: {request.conversation_id}"}

        conn.close()
        return result

    except Exception as e:
        logger.error(f"刪除對話時發生錯誤: {e}")
        return {"success": False, "error": str(e)}


class ConversationIdsRequest(BaseModel):
    conversation_ids: List[int]


@mcp_app_instance.tool()
@app.post("/prompts/conversation_summary", operation_id="conversation_summary")
async def conversation_summary(request: ConversationIdsRequest) -> str:
    """根據提供的對話 ID 生成對話摘要"""
    logger.info(f"調用工具: conversation_summary, 參數: {request.conversation_ids}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 構建 SQL 查詢，用於根據 ID 列表獲取對話內容
        placeholders = ", ".join("?" * len(request.conversation_ids))
        query = f"SELECT role, content FROM conversations WHERE id IN ({placeholders}) ORDER BY timestamp ASC"
        cursor.execute(query, tuple(request.conversation_ids))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "未找到指定 ID 的對話記錄。"

        summary_parts = []
        for role, content in rows:
            summary_parts.append(f"{role.capitalize()}: {content}")

        # 這裡可以加入更複雜的摘要邏輯，例如調用 LLM
        return "\n".join(summary_parts)

    except Exception as e:
        logger.error(f"生成對話摘要時發生錯誤: {e}")
        return f"生成摘要失敗: {e}"


@mcp_app_instance.tool()
@app.post("/prompts/extract_action_items", operation_id="extract_action_items")
async def extract_action_items(request: ConversationIdsRequest) -> str:
    """從指定的對話記錄中提取行動項目"""
    logger.info(f"調用工具: extract_action_items, 參數: {request.conversation_ids}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        placeholders = ", ".join("?" * len(request.conversation_ids))
        query = f"SELECT role, content FROM conversations WHERE id IN ({placeholders}) ORDER BY timestamp ASC"
        cursor.execute(query, tuple(request.conversation_ids))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "未找到指定 ID 的對話記錄。"

        full_conversation_text = "\n".join([f"{role.capitalize()}: {content}" for role, content in rows])

        # 在這裡可以添加調用 LLM 以提取行動項目的邏輯
        # 這裡只是一個佔位符，實際應該調用一個能夠理解並提取行動項目的模型
        if "行動" in full_conversation_text or "action item" in full_conversation_text.lower():
            return f"以下是對話中的潛在行動項目 (需進一步分析):\n{full_conversation_text}"
        else:
            return "在提供的對話記錄中未發現明確的行動項目。"

    except Exception as e:
        logger.error(f"提取行動項目時發生錯誤: {e}")
        return f"提取行動項目失敗: {e}"


# 啟動 MCP 伺服器 (僅在直接運行時)
if __name__ == "__main__":
    init_database() # 確保在啟動時初始化資料庫
    logger.info("直接啟動 ContextRecord MCP Server (STDIO 模式)...")
    asyncio.run(mcp_app_instance.run()) # 使用 asyncio.run 包裹 mcp_app_instance.run()
 
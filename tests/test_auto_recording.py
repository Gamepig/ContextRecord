#!/usr/bin/env python3
"""
測試 ContextRecord MCP Server 的自動記錄功能
"""

import asyncio
import json
import sys
import os
import pytest

# 添加根目錄到路徑，以便正確導入 src 模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.mcp_server import (
    server,
    init_database,
    handle_call_tool,
    get_auto_recording_config,
    AUTO_RECORDING_SESSIONS,
)


@pytest.mark.asyncio
async def test_auto_recording():
    """測試自動記錄功能"""
    print("🤖 測試 ContextRecord 自動記錄功能...")

    # 初始化資料庫
    init_database()
    print("✅ 資料庫初始化完成")

    # 1. 測試獲取自動記錄狀態（預設應該是停用）
    print("\n📊 測試獲取自動記錄狀態...")
    status_result = await handle_call_tool(
        "get_auto_recording_status", {"session_id": "test_session"}
    )
    print(f"✅ 初始狀態: {status_result[0].text}")

    # 2. 測試啟用自動記錄
    print("\n🔛 測試啟用自動記錄...")
    enable_result = await handle_call_tool(
        "enable_auto_recording",
        {"session_id": "test_session", "record_user": True, "record_assistant": True},
    )
    print(f"✅ 啟用結果: {enable_result[0].text}")

    # 3. 再次檢查狀態
    print("\n📊 檢查啟用後的狀態...")
    status_result = await handle_call_tool(
        "get_auto_recording_status", {"session_id": "test_session"}
    )
    print(f"✅ 啟用後狀態: {status_result[0].text}")

    # 4. 測試自動記錄對話
    print("\n💬 測試自動記錄對話...")
    auto_record_result = await handle_call_tool(
        "auto_record_conversation",
        {
            "user_message": "你好，這是一個自動記錄的測試訊息",
            "assistant_response": "您好！我已經收到您的測試訊息，自動記錄功能正在運作中。",
            "session_id": "test_session",
            "context": '{"test_mode": true, "feature": "auto_recording"}',
        },
    )
    print(f"✅ 自動記錄結果: {auto_record_result[0].text}")

    # 5. 搜尋剛才記錄的對話
    print("\n🔍 搜尋自動記錄的對話...")
    search_result = await handle_call_tool(
        "search_conversations", {"query": "自動記錄", "limit": 5}
    )
    print(f"✅ 搜尋結果: {search_result[0].text}")

    # 6. 測試停用自動記錄
    print("\n🔴 測試停用自動記錄...")
    disable_result = await handle_call_tool(
        "disable_auto_recording", {"session_id": "test_session"}
    )
    print(f"✅ 停用結果: {disable_result[0].text}")

    # 7. 測試停用後的自動記錄（應該不會記錄）
    print("\n❌ 測試停用後的自動記錄...")
    auto_record_result2 = await handle_call_tool(
        "auto_record_conversation",
        {
            "user_message": "這個訊息不應該被記錄",
            "assistant_response": "這個回應也不應該被記錄",
            "session_id": "test_session",
        },
    )
    print(f"✅ 停用後記錄結果: {auto_record_result2[0].text}")

    # 8. 測試多會話支援
    print("\n🔄 測試多會話支援...")

    # 啟用另一個會話的自動記錄
    enable_result2 = await handle_call_tool(
        "enable_auto_recording",
        {
            "session_id": "session_2",
            "record_user": True,
            "record_assistant": False,  # 只記錄用戶訊息
        },
    )
    print(f"✅ 會話2啟用結果: {enable_result2[0].text}")

    # 在會話2中記錄對話
    auto_record_result3 = await handle_call_tool(
        "auto_record_conversation",
        {
            "user_message": "會話2的用戶訊息",
            "assistant_response": "會話2的助理回應（不應該被記錄）",
            "session_id": "session_2",
        },
    )
    print(f"✅ 會話2記錄結果: {auto_record_result3[0].text}")

    # 9. 檢查所有會話狀態
    print("\n📋 檢查所有會話狀態...")
    print(f"當前自動記錄會話: {list(AUTO_RECORDING_SESSIONS.keys())}")
    for session_id in AUTO_RECORDING_SESSIONS:
        config = get_auto_recording_config(session_id)
        print(f"  - {session_id}: {config}")

    # 10. 獲取統計資訊
    print("\n📊 獲取最終統計資訊...")
    stats_result = await handle_call_tool("get_conversation_stats", {})
    print(f"✅ 統計資訊: {stats_result[0].text}")

    print("\n🎉 自動記錄功能測試完成！")


if __name__ == "__main__":
    asyncio.run(test_auto_recording())

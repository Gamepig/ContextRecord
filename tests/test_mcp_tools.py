#!/usr/bin/env python3
"""
測試 ContextRecord MCP Server 的工具功能
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
    handle_list_tools,
    handle_call_tool,
    handle_list_resources,
    handle_read_resource,
    handle_list_prompts,
    handle_get_prompt,
)


@pytest.mark.asyncio
async def test_tools():
    """測試所有工具功能"""
    print("🔧 測試 ContextRecord MCP Server 工具...")

    # 初始化資料庫
    init_database()
    print("✅ 資料庫初始化完成")

    # 測試列出工具
    print("\n📋 測試列出工具...")
    tools = await handle_list_tools()
    print(f"✅ 找到 {len(tools)} 個工具:")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description}")

    # 測試創建對話
    print("\n💬 測試創建對話...")
    create_result = await handle_call_tool(
        "create_conversation",
        {"role": "user", "content": "這是一個測試對話", "metadata": '{"test": true}'},
    )
    print(f"✅ 創建對話結果: {create_result[0].text}")

    # 測試搜尋對話
    print("\n🔍 測試搜尋對話...")
    search_result = await handle_call_tool(
        "search_conversations", {"query": "測試", "limit": 5}
    )
    print(f"✅ 搜尋結果: {search_result[0].text}")

    # 測試獲取統計資訊
    print("\n📊 測試獲取統計資訊...")
    stats_result = await handle_call_tool("get_conversation_stats", {})
    print(f"✅ 統計資訊: {stats_result[0].text}")

    # 測試列出資源
    print("\n📚 測試列出資源...")
    resources = await handle_list_resources()
    print(f"✅ 找到 {len(resources)} 個資源:")
    for resource in resources:
        print(f"   - {resource.name}: {resource.description}")

    # 測試讀取資源
    print("\n📖 測試讀取資源...")
    from mcp.types import AnyUrl

    resource_content = await handle_read_resource(AnyUrl("conversations://recent"))
    print(f"✅ 資源內容: {resource_content[:200]}...")

    # 測試列出提示
    print("\n💡 測試列出提示...")
    prompts = await handle_list_prompts()
    print(f"✅ 找到 {len(prompts)} 個提示:")
    for prompt in prompts:
        print(f"   - {prompt.name}: {prompt.description}")

    # 測試獲取提示
    print("\n📝 測試獲取提示...")
    prompt_result = await handle_get_prompt("analyze_conversation_pattern", {})
    print(f"✅ 提示內容: {prompt_result.description}")

    print("\n🎉 所有測試完成！MCP Server 工具功能正常。")


if __name__ == "__main__":
    asyncio.run(test_tools())

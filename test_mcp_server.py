#!/usr/bin/env python3
"""
測試 ContextRecord MCP Server 的功能
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """測試 MCP Server 的所有功能"""
    
    # 設定伺服器參數
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp_server.py"],
        env={"DATABASE_PATH": "data/test_conversations.db"}
    )
    
    print("🚀 正在連接到 ContextRecord MCP Server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化連接
            await session.initialize()
            print("✅ 成功連接到 MCP Server")
            
            # 測試列出工具
            print("\n📋 測試列出工具...")
            tools = await session.list_tools()
            print(f"可用工具數量: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # 測試列出資源
            print("\n📚 測試列出資源...")
            resources = await session.list_resources()
            print(f"可用資源數量: {len(resources.resources)}")
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            # 測試列出提示
            print("\n💭 測試列出提示...")
            prompts = await session.list_prompts()
            print(f"可用提示數量: {len(prompts.prompts)}")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            
            # 測試創建對話
            print("\n🔧 測試創建對話...")
            result = await session.call_tool(
                "create_conversation",
                arguments={
                    "role": "user",
                    "content": "這是一個測試對話",
                    "metadata": '{"test": true}'
                }
            )
            print(f"創建對話結果: {result.content}")
            
            # 測試搜尋對話
            print("\n🔍 測試搜尋對話...")
            search_result = await session.call_tool(
                "search_conversations",
                arguments={
                    "query": "測試",
                    "limit": 5
                }
            )
            print(f"搜尋結果: {search_result.content}")
            
            # 測試獲取統計資訊
            print("\n📊 測試獲取統計資訊...")
            stats_result = await session.call_tool(
                "get_conversation_stats",
                arguments={}
            )
            print(f"統計資訊: {stats_result.content}")
            
            # 測試讀取資源
            print("\n📖 測試讀取最近對話資源...")
            try:
                recent_conversations = await session.read_resource("conversations://recent")
                print(f"最近對話: {recent_conversations[:200]}...")
            except Exception as e:
                print(f"讀取資源時發生錯誤: {e}")
            
            # 測試獲取提示
            print("\n💬 測試獲取提示...")
            try:
                prompt_result = await session.get_prompt(
                    "summarize_conversations",
                    arguments={"style": "brief"}
                )
                print(f"提示內容: {prompt_result.description}")
                print(f"提示訊息數量: {len(prompt_result.messages)}")
            except Exception as e:
                print(f"獲取提示時發生錯誤: {e}")
            
            print("\n🎉 所有測試完成！")

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 
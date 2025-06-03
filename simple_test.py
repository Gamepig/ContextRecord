#!/usr/bin/env python3
"""
簡化的 MCP Server 測試
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def simple_test():
    """簡單測試 MCP Server"""

    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp_server.py"],
        env={"DATABASE_PATH": "data/test_conversations.db"},
    )

    print("🚀 連接到 MCP Server...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ 連接成功")

            # 測試創建對話（不使用 metadata）
            print("\n🔧 創建對話...")
            result = await session.call_tool(
                "create_conversation",
                arguments={"role": "user", "content": "這是一個測試對話"},
            )
            print(f"結果: {result.content[0].text}")

            # 測試搜尋
            print("\n🔍 搜尋對話...")
            search_result = await session.call_tool(
                "search_conversations", arguments={"query": "測試", "limit": 5}
            )
            print(f"搜尋結果: {search_result.content[0].text}")

            print("\n✅ 測試完成！")


if __name__ == "__main__":
    asyncio.run(simple_test())

#!/usr/bin/env python3
"""
測試 ContextRecord MCP Server 的 STDIO 通信
"""

import asyncio
import json
import subprocess
import sys
import os
import pytest


@pytest.mark.asyncio
async def test_mcp_stdio():
    """測試 MCP Server 的 STDIO 通信"""
    print("🔧 測試 ContextRecord MCP Server STDIO 通信...")

    # 啟動 MCP Server 進程
    server_path = os.path.join(os.path.dirname(__file__), "..", "src", "mcp_server.py")
    python_path = os.path.join(
        os.path.dirname(__file__), "..", ".venv", "bin", "python"
    )

    env = os.environ.copy()
    env["DATABASE_PATH"] = os.path.join(
        os.path.dirname(__file__), "..", "data", "conversations.db"
    )

    process = await asyncio.create_subprocess_exec(
        python_path,
        server_path,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    try:
        # 1. 發送初始化請求
        print("\n📡 發送初始化請求...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }

        process.stdin.write((json.dumps(init_request) + "\n").encode())
        await process.stdin.drain()

        # 讀取初始化回應
        response_line = await process.stdout.readline()
        init_response = json.loads(response_line.decode().strip())
        print(f"✅ 初始化回應: {init_response['result']['serverInfo']['name']}")

        # 2. 發送初始化完成通知
        print("\n📡 發送初始化完成通知...")
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }

        process.stdin.write((json.dumps(initialized_notification) + "\n").encode())
        await process.stdin.drain()

        # 3. 列出工具
        print("\n📡 請求列出工具...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }

        process.stdin.write((json.dumps(list_tools_request) + "\n").encode())
        await process.stdin.drain()

        # 讀取工具列表回應
        response_line = await process.stdout.readline()
        tools_response = json.loads(response_line.decode().strip())
        tools = tools_response["result"]["tools"]
        print(f"✅ 找到 {len(tools)} 個工具:")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description']}")

        # 4. 調用創建對話工具
        print("\n📡 調用創建對話工具...")
        create_conv_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "create_conversation",
                "arguments": {
                    "role": "user",
                    "content": "這是通過 STDIO 創建的測試對話",
                    "metadata": '{"source": "stdio_test"}',
                },
            },
        }

        process.stdin.write((json.dumps(create_conv_request) + "\n").encode())
        await process.stdin.drain()

        # 讀取創建對話回應
        response_line = await process.stdout.readline()
        create_response = json.loads(response_line.decode().strip())
        result = json.loads(create_response["result"]["content"][0]["text"])
        print(f"✅ 創建對話結果: {result['message']}")

        # 5. 列出資源
        print("\n📡 請求列出資源...")
        list_resources_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "resources/list",
            "params": {},
        }

        process.stdin.write((json.dumps(list_resources_request) + "\n").encode())
        await process.stdin.drain()

        # 讀取資源列表回應
        response_line = await process.stdout.readline()
        resources_response = json.loads(response_line.decode().strip())
        resources = resources_response["result"]["resources"]
        print(f"✅ 找到 {len(resources)} 個資源:")
        for resource in resources:
            print(f"   - {resource['name']}: {resource['description']}")

        print("\n🎉 STDIO 通信測試完成！MCP Server 工作正常。")

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        stderr_output = await process.stderr.read()
        if stderr_output:
            print(f"錯誤輸出: {stderr_output.decode()}")

    finally:
        # 關閉進程
        process.terminate()
        await process.wait()


if __name__ == "__main__":
    asyncio.run(test_mcp_stdio())

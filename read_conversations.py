#!/usr/bin/env python3
"""
讀取對話記錄的工具腳本
提供多種方式查看和搜尋對話記錄
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# 添加 src 目錄到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server import handle_call_tool, handle_read_resource

async def show_conversation_stats():
    """顯示對話統計資訊"""
    print("📊 對話統計資訊")
    print("=" * 50)
    
    result = await handle_call_tool("get_conversation_stats", {})
    data = json.loads(result[0].text)
    
    if data["success"]:
        print(f"總對話數: {data['total_conversations']}")
        print(f"角色分布: {data['role_distribution']}")
        print(f"最近一週: {data['recent_week_count']} 筆")
    else:
        print(f"錯誤: {data.get('error', '未知錯誤')}")

async def show_recent_conversations(limit=10):
    """顯示最近的對話記錄"""
    print(f"\n📖 最近 {limit} 筆對話記錄")
    print("=" * 50)
    
    try:
        result = await handle_read_resource("conversations://recent")
        conversations = json.loads(result)
        
        for i, conv in enumerate(conversations[:limit], 1):
            print(f"\n{i}. ID: {conv['id']} | 角色: {conv['role']} | 時間: {conv['timestamp']}")
            print(f"   內容: {conv['content']}")
            if conv.get('metadata'):
                print(f"   元數據: {conv['metadata']}")
            print("-" * 40)
            
    except Exception as e:
        print(f"讀取失敗: {e}")

async def search_conversations(query, limit=10):
    """搜尋對話記錄"""
    print(f"\n🔍 搜尋關鍵字「{query}」的對話記錄")
    print("=" * 50)
    
    result = await handle_call_tool("search_conversations", {
        "query": query,
        "limit": limit
    })
    
    data = json.loads(result[0].text)
    
    if data["success"]:
        print(f"找到 {data['count']} 筆相關對話:")
        
        for i, conv in enumerate(data['results'], 1):
            print(f"\n{i}. ID: {conv['id']} | 角色: {conv['role']} | 時間: {conv['timestamp']}")
            # 高亮顯示搜尋關鍵字
            content = conv['content']
            if query.lower() in content.lower():
                # 簡單的高亮顯示
                highlighted = content.replace(query, f"**{query}**")
                print(f"   內容: {highlighted}")
            else:
                print(f"   內容: {content}")
            
            if conv.get('metadata'):
                print(f"   元數據: {conv['metadata']}")
            print("-" * 40)
    else:
        print(f"搜尋失敗: {data.get('error', '未知錯誤')}")

async def show_conversations_by_role(role):
    """按角色顯示對話記錄"""
    print(f"\n👤 角色「{role}」的對話記錄")
    print("=" * 50)
    
    result = await handle_call_tool("search_conversations", {
        "query": "",  # 空查詢會返回所有記錄
        "limit": 50
    })
    
    data = json.loads(result[0].text)
    
    if data["success"]:
        role_conversations = [conv for conv in data['results'] if conv['role'] == role]
        print(f"找到 {len(role_conversations)} 筆「{role}」的對話:")
        
        for i, conv in enumerate(role_conversations[:10], 1):  # 只顯示前10筆
            print(f"\n{i}. ID: {conv['id']} | 時間: {conv['timestamp']}")
            print(f"   內容: {conv['content'][:100]}{'...' if len(conv['content']) > 100 else ''}")
            print("-" * 40)
    else:
        print(f"查詢失敗: {data.get('error', '未知錯誤')}")

async def main():
    """主函數"""
    print("🎯 ContextRecord 對話記錄讀取工具")
    print("=" * 60)
    
    # 1. 顯示統計資訊
    await show_conversation_stats()
    
    # 2. 顯示最近的對話
    await show_recent_conversations(5)
    
    # 3. 搜尋特定關鍵字
    await search_conversations("自動記錄", 5)
    
    # 4. 按角色顯示
    await show_conversations_by_role("user")
    
    print("\n🎉 讀取完成！")
    print("\n💡 使用提示:")
    print("   - 修改 search_conversations() 的查詢參數來搜尋不同內容")
    print("   - 修改 show_recent_conversations() 的 limit 參數來調整顯示數量")
    print("   - 使用 show_conversations_by_role() 來查看特定角色的對話")

if __name__ == "__main__":
    asyncio.run(main()) 
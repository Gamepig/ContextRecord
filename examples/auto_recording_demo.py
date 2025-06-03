#!/usr/bin/env python3
"""
ContextRecord 自動記錄功能演示

這個腳本展示如何在實際應用中使用自動記錄功能。
"""

import asyncio
import json
import sys
import os

# 添加 src 目錄到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server import handle_call_tool, init_database

async def demo_auto_recording():
    """演示自動記錄功能的實際使用"""
    print("🎯 ContextRecord 自動記錄功能演示")
    print("=" * 50)
    
    # 初始化資料庫
    init_database()
    
    # 模擬不同的使用場景
    scenarios = [
        {
            "name": "開發會話",
            "session_id": "dev_session",
            "conversations": [
                {
                    "user": "如何實現自動記錄功能？",
                    "assistant": "可以通過添加 enable_auto_recording 工具來實現自動記錄功能。",
                    "context": '{"file": "mcp_server.py", "topic": "功能開發"}'
                },
                {
                    "user": "需要支援多會話嗎？",
                    "assistant": "是的，每個會話可以獨立配置自動記錄設定。",
                    "context": '{"file": "mcp_server.py", "topic": "架構設計"}'
                }
            ]
        },
        {
            "name": "測試會話",
            "session_id": "test_session",
            "record_assistant": False,  # 只記錄用戶問題
            "conversations": [
                {
                    "user": "測試自動記錄是否正常？",
                    "assistant": "測試結果顯示功能正常（此回應不會被記錄）",
                    "context": '{"test_type": "功能測試", "priority": "high"}'
                }
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 場景: {scenario['name']}")
        print("-" * 30)
        
        session_id = scenario['session_id']
        record_assistant = scenario.get('record_assistant', True)
        
        # 1. 啟用自動記錄
        print(f"🔛 啟用會話 '{session_id}' 的自動記錄...")
        enable_result = await handle_call_tool(
            "enable_auto_recording",
            {
                "session_id": session_id,
                "record_user": True,
                "record_assistant": record_assistant
            }
        )
        
        result_data = json.loads(enable_result[0].text)
        if result_data["success"]:
            print(f"✅ 自動記錄已啟用")
            print(f"   配置: 用戶訊息={'✓' if result_data['config']['record_user'] else '✗'}, "
                  f"助理回應={'✓' if result_data['config']['record_assistant'] else '✗'}")
        
        # 2. 記錄對話
        for i, conv in enumerate(scenario['conversations'], 1):
            print(f"\n💬 記錄對話 {i}...")
            record_result = await handle_call_tool(
                "auto_record_conversation",
                {
                    "user_message": conv['user'],
                    "assistant_response": conv['assistant'],
                    "session_id": session_id,
                    "context": conv['context']
                }
            )
            
            record_data = json.loads(record_result[0].text)
            if record_data["success"]:
                print(f"✅ {record_data['message']}")
            else:
                print(f"❌ 記錄失敗: {record_data.get('error', '未知錯誤')}")
    
    # 3. 搜尋和統計
    print(f"\n📊 搜尋和統計")
    print("-" * 30)
    
    # 搜尋特定主題的對話
    search_result = await handle_call_tool(
        "search_conversations",
        {"query": "自動記錄", "limit": 3}
    )
    
    search_data = json.loads(search_result[0].text)
    if search_data["success"]:
        print(f"🔍 找到 {search_data['count']} 筆包含 '自動記錄' 的對話")
        for conv in search_data['results']:
            print(f"   - [{conv['role']}] {conv['content'][:50]}...")
    
    # 獲取統計資訊
    stats_result = await handle_call_tool("get_conversation_stats", {})
    stats_data = json.loads(stats_result[0].text)
    
    if stats_data["success"]:
        print(f"\n📈 對話統計:")
        print(f"   總對話數: {stats_data['total_conversations']}")
        print(f"   角色分布: {stats_data['role_distribution']}")
        print(f"   最近一週: {stats_data['recent_week_count']} 筆")
    
    # 4. 演示停用功能
    print(f"\n🔴 停用自動記錄演示")
    print("-" * 30)
    
    disable_result = await handle_call_tool(
        "disable_auto_recording",
        {"session_id": "dev_session"}
    )
    
    disable_data = json.loads(disable_result[0].text)
    if disable_data["success"]:
        print(f"✅ 已停用 'dev_session' 的自動記錄")
    
    # 測試停用後的記錄（應該不會記錄）
    test_record = await handle_call_tool(
        "auto_record_conversation",
        {
            "user_message": "這個訊息不應該被記錄",
            "assistant_response": "這個回應也不應該被記錄",
            "session_id": "dev_session"
        }
    )
    
    test_data = json.loads(test_record[0].text)
    print(f"🧪 停用後測試: {test_data['message']}")
    
    print(f"\n🎉 演示完成！")
    print("\n💡 提示:")
    print("   - 使用有意義的 session_id 來組織不同專案的對話")
    print("   - 在 context 中包含有用的元數據")
    print("   - 定期檢查統計資訊了解記錄情況")
    print("   - 處理敏感資訊時記得停用自動記錄")

if __name__ == "__main__":
    asyncio.run(demo_auto_recording()) 
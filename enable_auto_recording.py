#!/usr/bin/env python3
"""
啟用自動記錄功能的腳本
"""

import asyncio
import sys
import json
import os

# 添加 src 目錄到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server import handle_call_tool

async def enable_auto_recording():
    """啟用自動記錄功能"""
    print('🔛 啟動自動記錄功能')
    print('=' * 50)
    
    # 啟用自動記錄
    enable_result = await handle_call_tool('enable_auto_recording', {
        'session_id': 'default',
        'record_user': True,
        'record_assistant': True
    })
    
    enable_data = json.loads(enable_result[0].text)
    print(f'啟用結果: {"成功" if enable_data["success"] else "失敗"}')
    
    if enable_data['success']:
        print(f'會話ID: {enable_data["session_id"]}')
        config = enable_data.get('config', {})
        print(f'配置: 啟用={config.get("enabled")}, 用戶訊息={config.get("record_user")}, 助理回應={config.get("record_assistant")}')
    
    # 再次檢查狀態
    print('\n📊 確認自動記錄狀態')
    print('-' * 30)
    
    status_result = await handle_call_tool('get_auto_recording_status', {
        'session_id': 'default'
    })
    
    status_data = json.loads(status_result[0].text)
    print(f'最終狀態: {status_data.get("status")}')
    config = status_data.get('config', {})
    print(f'詳細配置: 啟用={config.get("enabled")}, 用戶={config.get("record_user")}, 助理={config.get("record_assistant")}')
    
    # 測試自動記錄功能
    print('\n🧪 測試自動記錄功能')
    print('-' * 30)
    
    test_result = await handle_call_tool('auto_record_conversation', {
        'user_message': '測試自動記錄功能是否正常運作',
        'assistant_response': '自動記錄功能已成功啟用並正常運作',
        'session_id': 'default',
        'context': '{"test": "auto_recording_enabled", "timestamp": "' + str(asyncio.get_event_loop().time()) + '"}'
    })
    
    test_data = json.loads(test_result[0].text)
    print(f'測試結果: {test_data.get("message", "未知")}')
    
    if test_data.get('success'):
        print('✅ 自動記錄功能已成功啟用並測試通過！')
    else:
        print(f'❌ 測試失敗: {test_data.get("error", "未知錯誤")}')

if __name__ == "__main__":
    asyncio.run(enable_auto_recording()) 
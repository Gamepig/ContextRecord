import requests
import json

def create_conversation_test():
    url = "http://127.0.0.1:8811/tools/create_conversation"
    headers = {"Content-Type": "application/json"}
    data = {"role": "user", "content": "你好，這是一個從 Python 腳本發送的測試訊息。"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 如果響應狀態碼不是 2xx，則引發 HTTPError
        print("create_conversation 成功：")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"create_conversation 失敗: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("錯誤回應內容：", e.response.text)

def search_conversations_test(query: str, limit: int = None):
    url = "http://127.0.0.1:8811/tools/search_conversations"
    headers = {"Content-Type": "application/json"}
    data = {"query": query}
    if limit is not None:
        data["limit"] = limit

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 如果響應狀態碼不是 2xx，則引發 HTTPError
        print(f"search_conversations (query='{query}') 成功：")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"search_conversations (query='{query}') 失敗: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("錯誤回應內容：", e.response.text)

if __name__ == "__main__":
    create_conversation_test()
    print("\n" + "="*50 + "\n") # 分隔線
    search_conversations_test(query="測試訊息")
    search_conversations_test(query="你好", limit=5)
    search_conversations_test(query="不存在的訊息") 
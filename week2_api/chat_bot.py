import requests
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 保存对话历史
messages = [
    {"role": "system", "content": "你是一个友好的AI助手，喜欢用简短的话回答问题。"}
]

print("🤖 AI聊天机器人启动！输入 'quit' 退出\n")

while True:
    # 获取用户输入
    user_input = input("你: ")
    
    if user_input.lower() == "quit":
        print("再见！")
        break
    
    # 把用户消息加入历史
    messages.append({"role": "user", "content": user_input})
    
    # 调用API
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": messages
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    ai_reply = result["choices"][0]["message"]["content"]
    
    # 把AI回复加入历史
    messages.append({"role": "assistant", "content": ai_reply})
    
    print(f"AI: {ai_reply}\n")
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 定义一个工具函数
def get_current_time():
    """获取当前时间"""
    return f"现在是 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"

# 手动工具调用逻辑
tools_info = """
你可以使用以下工具：
- get_current_time: 获取当前日期和时间

当用户问时间相关问题时，请回复：[TOOL:get_current_time]
"""

messages = [
    {"role": "system", "content": f"你是一个有用的助手。{tools_info}"}
]

print("🤖 带工具的AI助手启动！输入 'quit' 退出\n")

while True:
    user_input = input("你: ")
    
    if user_input.lower() == "quit":
        print("再见！")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {"model": "deepseek-chat", "messages": messages}
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    ai_reply = result["choices"][0]["message"]["content"]
    
    # 检查是否需要调用工具
    if "[TOOL:get_current_time]" in ai_reply:
        tool_result = get_current_time()
        messages.append({"role": "assistant", "content": ai_reply})
        messages.append({"role": "user", "content": f"工具返回结果：{tool_result}。请根据这个结果回答用户。"})
        
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]
    
    messages.append({"role": "assistant", "content": ai_reply})
    print(f"AI: {ai_reply}\n")
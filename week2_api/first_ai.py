import requests
import os
from dotenv import load_dotenv

# 加载API Key
load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 调用DeepSeek
url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "你好，用一句话介绍你自己"}
    ]
}

response = requests.post(url, json=data, headers=headers)
result = response.json()
print(result["choices"][0]["message"]["content"])
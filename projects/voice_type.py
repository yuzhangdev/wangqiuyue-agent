import pyttsx3
import requests
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print(f"🤖 王秋月: {text}")
    engine.say(text)
    engine.runAndWait()

def chat(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，友好简洁，50字以内。"},
        {"role": "user", "content": text}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

print("=" * 50)
print("⌨️ 打字版王秋月（语音播报）")
print("输入 'quit' 退出")
print("=" * 50)

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() == "quit":
        speak("好的大哥，再见！")
        break
    ai_reply = chat(user_input)
    speak(ai_reply)
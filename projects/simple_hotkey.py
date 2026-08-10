import pyttsx3
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print(f"🌙 王秋月: {text}")
    # 用新引擎实例避免冲突
    tts = pyttsx3.init()
    tts.setProperty('rate', 180)
    tts.say(text)
    tts.runAndWait()
    tts.stop()

def chat_ai(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，回复简洁，30字以内。"},
        {"role": "user", "content": text}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

print("=" * 50)
print("🎤 王秋月语音对话模式")
print("打字 + 语音回复，输入 quit 退出")
print("=" * 50)

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() == "quit":
        speak("再见！")
        break
    reply = chat_ai(user_input)
    speak(reply)
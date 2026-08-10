import keyboard
import pyttsx3
import requests
import os
import threading
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print(f"🌙 王秋月: {text}")
    engine.say(text)
    engine.runAndWait()

def chat_ai(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，回复简洁，30字以内。"},
        {"role": "user", "content": text}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def on_hotkey():
    """按下快捷键触发"""
    speak("我在，请说")
    user_input = input("👤 你说: ")
    if user_input:
        reply = chat_ai(user_input)
        speak(reply)

# 注册快捷键 Ctrl+Shift+W
keyboard.add_hotkey('ctrl+shift+a', on_hotkey)

print("=" * 50)
print("⌨️ 快捷键唤醒模式")
print("按 Ctrl+Shift+A 叫醒王秋月")
print("按 Ctrl+C 退出")
print("=" * 50)

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\n👋 退出")
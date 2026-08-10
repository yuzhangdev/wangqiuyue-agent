import speech_recognition as sr
import pyttsx3
import requests
import os
import threading
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

engine = pyttsx3.init()
engine.setProperty('rate', 180)

WAKE_WORD = "王秋月"  # 唤醒词

def speak(text):
    print(f"🌙 王秋月: {text}")
    engine.say(text)
    engine.runAndWait()

def chat_ai(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，回复极度简洁，15字以内。"},
        {"role": "user", "content": text}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def listen_for_wake():
    """持续监听唤醒词"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("👂 等待唤醒词 '王秋月'...")
        while True:
            try:
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                text = r.recognize_google(audio, language="zh-CN")
                if WAKE_WORD in text:
                    print(f"🔔 唤醒词检测到: {text}")
                    speak("我在，请说")
                    return text.replace(WAKE_WORD, "").strip()
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception:
                continue

print("=" * 50)
print("🎤 语音唤醒模式 - 说 '王秋月' 叫醒我")
print("Ctrl+C 退出")
print("=" * 50)

# 先装依赖检查
try:
    import speech_recognition
except:
    print("需要安装: pip install SpeechRecognition pyaudio")

while True:
    try:
        user_text = listen_for_wake()
        if user_text:
            print(f"👤 你: {user_text}")
            reply = chat_ai(user_text)
            speak(reply)
    except KeyboardInterrupt:
        print("\n👋 退出")
        break
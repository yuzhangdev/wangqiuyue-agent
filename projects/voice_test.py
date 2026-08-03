import speech_recognition as sr
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

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️  正在听...(说 '退出' 结束)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language='zh-CN')
            print(f"👤 你: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⏰ 超时，没听到声音")
            return None
        except sr.UnknownValueError:
            print("❓ 没听清")
            return None

def chat(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，友好简洁，回复50字以内。"},
        {"role": "user", "content": text}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

print("=" * 50)
print("🎤 语音版王秋月启动！")
print("=" * 50)

while True:
    user_text = listen()
    if user_text is None:
        continue
    if "退出" in user_text:
        speak("好的大哥，再见！")
        break
    
    ai_reply = chat(user_text)
    speak(ai_reply)
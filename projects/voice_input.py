import whisper
import pyttsx3
import requests
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

print("⏳ 加载语音模型（首次需要下载small模型，约500MB）...")
model = whisper.load_model("small")

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print(f"🌙 王秋月: {text}")
    engine.say(text)
    engine.runAndWait()

def chat_with_ai(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，友好简洁，50字以内。"},
        {"role": "user", "content": text}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

print("=" * 50)
print("🎤 语音版王秋月（Whisper）")
print("输入 'quit' 退出")
print("=" * 50)

# 用麦克风录音保存为文件
import sounddevice as sd
import numpy as np
import wave

def record_audio(filename="input.wav", duration=5, fs=16000):
    print(f"🎙️ 录音 {duration} 秒...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    # 保存为wav
    audio = (recording * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    return filename

while True:
    cmd = input("\n按回车开始录音（quit退出）: ")
    if cmd.lower() == "quit":
        break
    
    try:
        audio_file = record_audio()
        print("🔍 识别中...")
        result = model.transcribe(audio_file, language="zh")
        user_text = result["text"].strip()
        print(f"👤 你: {user_text}")
        
        if user_text:
            reply = chat_with_ai(user_text)
            speak(reply)
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("可能需要装 sounddevice: pip install sounddevice")
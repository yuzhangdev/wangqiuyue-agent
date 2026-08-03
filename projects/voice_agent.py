import streamlit as st
import requests
import os
import speech_recognition as sr
import pyttsx3
import threading
from datetime import datetime
from dotenv import load_dotenv

st.set_page_config(page_title="🎤 语音王秋月", page_icon="🎤")
st.title("🎤 语音版王秋月")
st.caption("点击按钮，用嘴跟王秋月对话")

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化语音引擎
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # 语速
engine.setProperty('volume', 1.0)  # 音量

def speak(text):
    """文字转语音"""
    def _speak():
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=_speak)
    thread.start()

def listen():
    """语音转文字"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ 正在听...请说话")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language='zh-CN')
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception:
            return None

def chat_with_ai(user_text):
    """调用DeepSeek"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，是个友好的语音助手，回答简洁，50字以内。"},
        {"role": "user", "content": user_text}
    ]
    response = requests.post(
        url,
        json={"model": "deepseek-chat", "messages": messages},
        headers=headers
    )
    return response.json()["choices"][0]["message"]["content"]

# ========== 界面 ==========
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 手动输入
text_input = st.chat_input("打字输入...")

# 语音输入按钮
col1, col2 = st.columns(2)
with col1:
    if st.button("🎤 点击说话", use_container_width=True):
        user_text = listen()
        if user_text:
            st.success(f"你说：{user_text}")
            ai_reply = chat_with_ai(user_text)
            st.session_state.chat_history.append(("你", user_text))
            st.session_state.chat_history.append(("王秋月", ai_reply))
            speak(ai_reply)
        else:
            st.warning("没听清，请重试")

with col2:
    if st.button("🗑️ 清空记录", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

if text_input:
    ai_reply = chat_with_ai(text_input)
    st.session_state.chat_history.append(("你", text_input))
    st.session_state.chat_history.append(("王秋月", ai_reply))
    speak(ai_reply)

# 显示聊天记录
for role, content in st.session_state.chat_history:
    with st.chat_message("user" if role == "你" else "assistant"):
        st.write(f"**{role}**：{content}")
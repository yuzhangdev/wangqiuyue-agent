import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 页面设置
st.set_page_config(page_title="王秋月 AI助手", page_icon="🤖")
st.title("🤖 王秋月 - AI智能助手")
st.caption("你的专属AI助手，能聊天、能调工具、能数据分析")

# 加载API Key
load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你叫王秋月，是一个聪明、友好的AI助手，喜欢用简洁的话回答。"}
    ]

# 显示历史消息
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 用户输入
if user_input := st.chat_input("说点什么吧..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_input)
    
    # 加入历史
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 调用DeepSeek
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": st.session_state.messages
    }
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = requests.post(url, json=data, headers=headers)
            result = response.json()
            ai_reply = result["choices"][0]["message"]["content"]
            st.write(ai_reply)
    
    # 加入历史
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
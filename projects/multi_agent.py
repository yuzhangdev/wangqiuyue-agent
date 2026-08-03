import streamlit as st
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import random

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="🤖 王秋月·多功能Agent", page_icon="🤖")
st.title("🤖 王秋月 · 多功能智能 Agent")
st.caption("能聊天 · 能分析Excel · 能算数 · 能讲笑话")

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# ========== 工具函数 ==========
def tool_get_time():
    return f"现在是 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"

def tool_calculator(expression):
    try:
        import re
        # 只允许数字和运算符，防止安全问题
        expression = expression.strip()
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"算不出来（{str(e)}），换个表达试试？"

def tool_tell_joke():
    jokes = [
        "为什么程序员总在晚上工作？因为他们喜欢「黑」科技！",
        "为什么Python程序员不会迷路？因为他们有「import 方向」！",
        "一个布尔值走进酒吧，酒保说：你不是true就是false。布尔值说：我可能是None。",
    ]
    return random.choice(jokes)

# ========== 工具描述 ==========
tools_info = """
你叫王秋月，是一个多功能AI助手。你可以使用以下工具（回复时用标记触发）：
- 当用户问时间/日期：回复 [TOOL:get_time]
- 当用户要你算数学：回复 [TOOL:calculator|表达式]
- 当用户要你讲笑话：回复 [TOOL:tell_joke]
- 其他情况正常回复
"""

# ========== 初始化对话 ==========
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": tools_info}
    ]

# ========== 侧边栏：Excel分析 ==========
with st.sidebar:
    st.header("📁 上传Excel分析")
    uploaded_file = st.file_uploader("选择Excel文件", type=["xlsx", "xls"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ 加载成功！{len(df)}行 × {len(df.columns)}列")
        with st.expander("📋 数据预览"):
            st.dataframe(df.head())
        
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if num_cols and len(df) <= 15:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            ax1.bar(df.iloc[:, 0].astype(str), df[num_cols[0]])
            ax1.set_title(f'{num_cols[0]} 柱状图')
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            if len(df) <= 10:
                ax2.pie(df[num_cols[0]], labels=df.iloc[:, 0].astype(str), autopct='%1.1f%%')
                ax2.set_title(f'{num_cols[0]} 占比')
            
            st.pyplot(fig)
            plt.close()

# ========== 对话区域 ==========
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_input := st.chat_input("跟王秋月说点什么..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = requests.post(
                url,
                json={"model": "deepseek-chat", "messages": st.session_state.messages},
                headers=headers
            )
            ai_reply = response.json()["choices"][0]["message"]["content"]
            
            # 检查工具调用
            if "[TOOL:get_time]" in ai_reply:
                tool_result = tool_get_time()
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                st.session_state.messages.append({"role": "user", "content": f"工具结果：{tool_result}。请直接告诉用户。"})
                response2 = requests.post(url, json={"model": "deepseek-chat", "messages": st.session_state.messages}, headers=headers)
                ai_reply = response2.json()["choices"][0]["message"]["content"]
            
            elif "[TOOL:calculator" in ai_reply:
                expr = ai_reply.split("|")[-1].strip("]")
                tool_result = tool_calculator(expr)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                st.session_state.messages.append({"role": "user", "content": f"工具结果：{tool_result}。请直接告诉用户。"})
                response2 = requests.post(url, json={"model": "deepseek-chat", "messages": st.session_state.messages}, headers=headers)
                ai_reply = response2.json()["choices"][0]["message"]["content"]
            
            elif "[TOOL:tell_joke]" in ai_reply:
                tool_result = tool_tell_joke()
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                st.session_state.messages.append({"role": "user", "content": f"工具结果：{tool_result}。请直接告诉用户。"})
                response2 = requests.post(url, json={"model": "deepseek-chat", "messages": st.session_state.messages}, headers=headers)
                ai_reply = response2.json()["choices"][0]["message"]["content"]
            
            st.write(ai_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
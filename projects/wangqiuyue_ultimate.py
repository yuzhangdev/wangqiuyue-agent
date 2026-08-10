import streamlit as st
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import random
import json
import sqlite3
import urllib.parse
import re

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="🌙 王秋月·终极版", page_icon="🌙", layout="wide")

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# ========== 记忆系统 ==========
MEMORY_FILE = "ultimate_memory.json"

def load_memories():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_memory(user, ai):
    memories = load_memories()
    memories.append({"user": user, "ai": ai})
    if len(memories) > 50:
        memories = memories[-50:]
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False)

def search_memory(query):
    memories = load_memories()
    related = []
    for m in memories:
        score = sum(1 for c in query if c in m["user"] or c in m["ai"])
        if score > 0:
            related.append(m)
    return related[-5:]

# ========== 用户画像数据库 ==========
PROFILE_DB = "user_profile.db"

def init_profile_db():
    conn = sqlite3.connect(PROFILE_DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS profile (
        key TEXT PRIMARY KEY, value TEXT, updated_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT, ai_reply TEXT, timestamp TEXT)""")
    conn.commit()
    conn.close()

def get_profile():
    conn = sqlite3.connect(PROFILE_DB)
    c = conn.cursor()
    c.execute("SELECT key, value FROM profile")
    rows = c.fetchall()
    conn.close()
    return dict(rows) if rows else {}

def save_conversation(user, ai):
    conn = sqlite3.connect(PROFILE_DB)
    c = conn.cursor()
    c.execute("INSERT INTO conversations VALUES (NULL, ?, ?, datetime('now','localtime'))", (user, ai))
    conn.commit()
    conn.close()

def update_profile():
    conn = sqlite3.connect(PROFILE_DB)
    c = conn.cursor()
    c.execute("SELECT user_input FROM conversations ORDER BY id DESC LIMIT 30")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return
    history = "\n".join([r[0] for r in rows])
    messages = [
        {"role": "system", "content": "提取用户画像，返回JSON：{\"name\":\"\",\"interests\":[],\"goals\":[],\"habits\":[]}，只返回JSON。"},
        {"role": "user", "content": history}
    ]
    try:
        result = call_deepseek(messages)
        data = json.loads(result)
        conn = sqlite3.connect(PROFILE_DB)
        c = conn.cursor()
        for k, v in data.items():
            val = ", ".join(v) if isinstance(v, list) else str(v)
            c.execute("INSERT OR REPLACE INTO profile VALUES (?, ?, datetime('now','localtime'))", (k, val))
        conn.commit()
        conn.close()
    except:
        pass

init_profile_db()

# ========== DeepSeek调用 ==========
def call_deepseek(messages):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# ========== 样式 ==========
st.markdown("""
<style>
    .main-title {text-align:center;font-size:3rem;font-weight:bold;
        background:linear-gradient(135deg,#667eea,#764ba2);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    .sub-title {text-align:center;color:#888;margin-bottom:1rem;}
    .stChatMessage {border-radius:15px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌙 王秋月 · 终极版</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">记忆 · 工具调用 · 自主规划 · 文档问答 · 联网搜索 · Excel分析 · 用户画像</p>', unsafe_allow_html=True)

# ========== 侧边栏 ==========
with st.sidebar:
    st.header("📁 Excel分析")
    uploaded_file = st.file_uploader("上传Excel", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success(f"{len(df)}行 × {len(df.columns)}列")
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if num_cols and len(df) <= 15:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
            ax1.bar(df.iloc[:,0].astype(str), df[num_cols[0]], color=colors[:len(df)])
            ax1.set_title(f'{num_cols[0]} 柱状图')
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            if len(df) <= 10:
                ax2.pie(df[num_cols[0]], labels=df.iloc[:,0].astype(str), autopct='%1.1f%%', colors=colors[:len(df)])
                ax2.set_title(f'{num_cols[0]} 占比')
            st.pyplot(fig)
            plt.close()
    
    st.divider()
    st.header("🧠 用户画像")
    profile = get_profile()
    if profile:
        for k, v in profile.items():
            st.write(f"**{k}**: {v}")
    else:
        st.write("聊几句自动生成...")
    
    st.divider()
    st.header("🛠️ 功能面板")
    st.code("查天气 深圳\n搜新闻 AI\n算 128*35\n讲个笑话\n现在几点了？")

# ========== 对话 ==========
if "ultimate_messages" not in st.session_state:
    st.session_state.ultimate_messages = [
        {"role": "system", "content": "你叫王秋月，是张羽开发的AI助手。友好、专业、简洁。能调用工具：时间、计算、笑话、天气、新闻、规划。根据用户画像提供个性化回复。"}
    ]
    st.session_state.msg_count = 0

for msg in st.session_state.ultimate_messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_input := st.chat_input("跟王秋月说点什么..."):
    with st.chat_message("user"):
        st.write(user_input)
    
    # 搜索记忆
    memories = search_memory(user_input)
    memory_text = "相关记忆：\n" + "\n".join([f"用户: {m['user']} | 王秋月: {m['ai']}" for m in memories]) if memories else ""
    
    # 加入用户画像
    profile = get_profile()
    if profile:
        profile_text = "用户画像：" + ", ".join([f"{k}:{v}" for k, v in profile.items()])
        memory_text = memory_text + "\n" + profile_text if memory_text else profile_text
    
    st.session_state.ultimate_messages.append({"role": "user", "content": user_input})
    st.session_state.msg_count += 1
    
    messages = [st.session_state.ultimate_messages[0]]
    if memory_text:
        messages.append({"role": "system", "content": memory_text})
    messages.extend(st.session_state.ultimate_messages[1:])
    
    with st.chat_message("assistant"):
        with st.spinner("🌙 思考中..."):
            reply = call_deepseek(messages)
            
            # 工具检测
            if "天气" in user_input or "weather" in user_input.lower():
                try:
                    city = user_input.replace("查天气", "").replace("天气", "").strip() or "深圳"
                    w = requests.get(f"https://wttr.in/{urllib.parse.quote(city)}?format=%C+%t", timeout=5, headers={"User-Agent": "curl"})
                    reply = f"🌤️ {city}天气：{w.text.strip()}"
                except:
                    pass
            elif any(w in user_input for w in ["算", "计算", "+", "-", "*", "/"]):
                try:
                    expr = user_input.replace("算", "").replace("计算", "").replace("帮我", "").replace(" ", "")
                    nums = re.findall(r'[\d.]+', expr)
                    ops = re.findall(r'[+\-*/]', expr)
                    if nums and ops:
                        expr_clean = nums[0] + ops[0] + nums[1]
                        result = eval(expr_clean)
                        reply = f"🧮 {expr_clean} = {result}"
                except:
                    pass
            elif "笑话" in user_input:
                jokes = ["为什么程序员总在晚上工作？因为他们喜欢「黑」科技！","为什么Python程序员不会迷路？因为他们有「import 方向」！"]
                reply = random.choice(jokes)
            
            st.write(reply)
    
    st.session_state.ultimate_messages.append({"role": "assistant", "content": reply})
    save_memory(user_input, reply)
    save_conversation(user_input, reply)
    
    # 每10条对话自动更新画像
    if st.session_state.msg_count % 10 == 0:
        update_profile()
import streamlit as st
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import random
from bs4 import BeautifulSoup

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 页面配置 ==========
st.set_page_config(
    page_title="🤖 王秋月·AI智能助手",
    page_icon="🌙",
    layout="wide"
)

# ========== 自定义CSS样式 ==========
st.markdown("""
<style>
    /* 隐藏默认header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 主标题渐变 */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
    }
    
    /* 副标题 */
    .sub-title {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    
    /* 功能卡片 */
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-icon { font-size: 2rem; }
    .feature-name { font-weight: bold; margin-top: 10px; }
    
    /* 侧边栏美化 */
    .sidebar-title {
        color: #667eea;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* 聊天框美化 */
    .stChatMessage {
        border-radius: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== 加载API ==========
load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# ========== 工具函数 ==========
def tool_get_time():
    return f"现在是 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"

def tool_calculator(expression):
    try:
        expression = expression.strip().replace(" ", "")
        result = eval(expression)
        return f"{expression} = {result}"
    except:
        return "算不出来，换个表达试试？"

def tool_tell_joke():
    jokes = [
        "为什么程序员总在晚上工作？因为他们喜欢「黑」科技！🖤",
        "为什么Python程序员不会迷路？因为他们有「import 方向」！🧭",
        "一个布尔值走进酒吧，酒保说：你不是true就是false。布尔值说：我可能是None。🤷",
        "程序员最怕什么？怕自己写的代码在别人电脑上跑不起来。💻",
        "产品经理：这个需求很简单。程序员：你来写。😤",
    ]
    return random.choice(jokes)

def tool_get_weather(city="深圳"):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%h+%w&lang=zh"
        response = requests.get(url, timeout=10)
        return f"🌤️ {city}天气：{response.text.strip()}"
    except:
        return f"查不到{city}的天气"

def tool_search_news(keyword="科技"):
    try:
        url = f"https://www.bing.com/search?q={keyword}&format=rss"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'xml')
        items = soup.find_all('item')[:3]
        if items:
            news = [f"📰 {item.title.text}" for item in items]
            return "\n".join(news)
        return "没找到相关新闻"
    except:
        return "新闻搜索暂时不可用"

# ========== 工具描述 ==========
tools_info = """
你叫王秋月，是一个聪明、友好的AI助手。回复简洁，50字以内。
工具触发标记：
- 时间：[TOOL:get_time]
- 计算：[TOOL:calculator|表达式]
- 笑话：[TOOL:tell_joke]
- 天气：[TOOL:weather|城市]
- 新闻：[TOOL:news|关键词]
"""

# ========== 初始化 ==========
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": tools_info}]

# ========== 页面头部 ==========
st.markdown('<p class="main-title">🌙 王秋月</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">你的专属AI智能助手 · 聊天 · 分析 · 查天气 · 搜新闻</p>', unsafe_allow_html=True)

# ========== 功能介绍卡片 ==========
col1, col2, col3, col4, col5 = st.columns(5)
features = [
    ("💬", "智能聊天"),
    ("📊", "数据分析"),
    ("🌤️", "查天气"),
    ("📰", "搜新闻"),
    ("🧮", "计算器"),
]
for col, (icon, name) in zip([col1, col2, col3, col4, col5], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown('<p class="sidebar-title">📁 Excel 数据分析</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx", "xls"], key="file_uploader")
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ {len(df)}行 × {len(df.columns)}列")
        with st.expander("📋 数据预览"):
            st.dataframe(df.head())
        
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if num_cols and len(df) <= 15:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
            ax1.bar(df.iloc[:, 0].astype(str), df[num_cols[0]], color=colors[:len(df)])
            ax1.set_title(f'📊 {num_cols[0]} 柱状图')
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            if len(df) <= 10:
                ax2.pie(df[num_cols[0]], labels=df.iloc[:, 0].astype(str), 
                       autopct='%1.1f%%', colors=colors[:len(df)])
                ax2.set_title(f'🍩 {num_cols[0]} 占比')
            st.pyplot(fig)
            plt.close()
    
    st.divider()
    st.markdown('<p class="sidebar-title">🛠️ 快捷命令</p>', unsafe_allow_html=True)
    st.code("查天气 深圳\n搜新闻 AI\n算 128*35\n讲个笑话\n现在几点了？")

# ========== 对话区域 ==========
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_input := st.chat_input("💬 跟王秋月说点什么..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    with st.chat_message("assistant"):
        with st.spinner("🌙 王秋月思考中..."):
            response = requests.post(
                url,
                json={"model": "deepseek-chat", "messages": st.session_state.messages},
                headers=headers
            )
            ai_reply = response.json()["choices"][0]["message"]["content"]
            
            # 工具调度
            for tool_name in ["get_time", "calculator", "tell_joke", "weather", "news"]:
                tag = f"[TOOL:{tool_name}"
                if tag in ai_reply:
                    param = ""
                    if "|" in ai_reply:
                        param = ai_reply.split("|")[-1].strip("]").strip()
                    
                    if tool_name == "get_time":
                        tool_result = tool_get_time()
                    elif tool_name == "calculator":
                        tool_result = tool_calculator(param)
                    elif tool_name == "tell_joke":
                        tool_result = tool_tell_joke()
                    elif tool_name == "weather":
                        tool_result = tool_get_weather(param or "深圳")
                    elif tool_name == "news":
                        tool_result = tool_search_news(param or "科技")
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    st.session_state.messages.append({"role": "user", "content": f"工具结果：{tool_result}。请根据结果直接告诉用户。"})
                    response2 = requests.post(url, json={"model": "deepseek-chat", "messages": st.session_state.messages}, headers=headers)
                    ai_reply = response2.json()["choices"][0]["message"]["content"]
                    break
            
            st.write(ai_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# ========== 底部 ==========
st.divider()
st.markdown('<p style="text-align:center;color:#888;">🚀 Powered by DeepSeek · 张羽 独立开发 · <a href="https://gitee.com/zhangyu202/agent-study" target="_blank">项目源码</a></p>', unsafe_allow_html=True)
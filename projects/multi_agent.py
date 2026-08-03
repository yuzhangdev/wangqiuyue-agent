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

st.set_page_config(page_title="🤖 王秋月·多功能Agent", page_icon="🤖")
st.title("🤖 王秋月 · 多功能智能 Agent")
st.caption("聊天 · Excel分析 · 算数 · 讲笑话 · 查天气 · 搜新闻")

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# ========== 工具函数 ==========
def tool_get_time():
    return f"现在是 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"

def tool_calculator(expression):
    try:
        expression = expression.strip()
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"算不出来，换个表达试试？"

def tool_tell_joke():
    jokes = [
        "为什么程序员总在晚上工作？因为他们喜欢「黑」科技！",
        "为什么Python程序员不会迷路？因为他们有「import 方向」！",
        "一个布尔值走进酒吧，酒保说：你不是true就是false。布尔值说：我可能是None。",
        "为什么Java程序员要戴眼镜？因为他们看不到C#！",
    ]
    return random.choice(jokes)

def tool_get_weather(city="深圳"):
    """查天气"""
    try:
        # 使用wttr.in免费天气API
        url = f"https://wttr.in/{city}?format=%C+%t+%h+%w&lang=zh"
        response = requests.get(url, timeout=10)
        return f"{city}天气：{response.text.strip()}"
    except:
        return f"查不到{city}的天气，请检查城市名"

def tool_search_news(keyword="科技"):
    """搜新闻"""
    try:
        # 使用Bing搜索
        url = f"https://www.bing.com/search?q={keyword}&format=rss"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'xml')
        items = soup.find_all('item')[:3]
        if items:
            news = [f"- {item.title.text}" for item in items]
            return f"关于「{keyword}」的最新新闻：\n" + "\n".join(news)
        return f"没找到关于「{keyword}」的新闻"
    except:
        return "新闻搜索暂时不可用，请稍后再试"

# ========== 工具描述 ==========
tools_info = """
你叫王秋月，是一个多功能AI助手。你可以使用以下工具（回复时用标记触发）：
- 问时间/日期：[TOOL:get_time]
- 算数学：[TOOL:calculator|表达式]
- 讲笑话：[TOOL:tell_joke]
- 查天气：[TOOL:weather|城市名]
- 搜新闻：[TOOL:news|关键词]
- 其他情况正常回复
"""

# ========== 初始化对话 ==========
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": tools_info}]

# ========== 侧边栏 ==========
with st.sidebar:
    st.header("📁 Excel分析")
    uploaded_file = st.file_uploader("上传Excel", type=["xlsx", "xls"], key="file_uploader")
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ {len(df)}行 × {len(df.columns)}列")
        with st.expander("📋 预览"):
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
    
    st.divider()
    st.header("🛠️ 快捷命令")
    st.code("查天气 深圳\n搜新闻 AI\n算 128*35\n讲个笑话")

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
            
            # 工具调度
            tool_called = False
            for tool_name in ["get_time", "calculator", "tell_joke", "weather", "news"]:
                tag = f"[TOOL:{tool_name}"
                if tag in ai_reply:
                    # 提取参数
                    param = ""
                    if "|" in ai_reply:
                        param = ai_reply.split("|")[-1].strip("]").strip()
                    
                    # 执行工具
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
                    
                    # 把结果喂回AI
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    st.session_state.messages.append({"role": "user", "content": f"工具结果：{tool_result}。请根据这个结果直接告诉用户。"})
                    response2 = requests.post(url, json={"model": "deepseek-chat", "messages": st.session_state.messages}, headers=headers)
                    ai_reply = response2.json()["choices"][0]["message"]["content"]
                    tool_called = True
                    break
            
            st.write(ai_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
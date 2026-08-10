import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="📊 王秋月·数据大屏", page_icon="📊", layout="wide")

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 模拟数据 ==========
def generate_data():
    now = datetime.now()
    times = [now - timedelta(minutes=i*10) for i in range(23, -1, -1)]
    return {
        "时间": times,
        "对话次数": [random.randint(5, 50) for _ in range(24)],
        "工具调用": [random.randint(1, 20) for _ in range(24)],
        "响应时间(ms)": [random.randint(200, 800) for _ in range(24)],
    }

data = generate_data()
df = pd.DataFrame(data)

# ========== 顶部标题 ==========
st.markdown("""
<h1 style='text-align:center;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:3rem;'>
📊 王秋月 · 数据大屏
</h1>
""", unsafe_allow_html=True)

# ========== 核心指标 ==========
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💬 今日对话", f"{sum(data['对话次数'])}次", "+12%")
with col2:
    st.metric("🔧 工具调用", f"{sum(data['工具调用'])}次", "+8%")
with col3:
    st.metric("⚡ 平均响应", f"{sum(data['响应时间(ms)'])//24}ms", "-15%")
with col4:
    st.metric("🧠 记忆条数", "1,247条", "+23")

# ========== 图表区 ==========
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💬 24小时对话趋势")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(range(24), df["对话次数"], alpha=0.3, color='#667eea')
    ax.plot(range(24), df["对话次数"], color='#667eea', linewidth=2, marker='o')
    ax.set_xticks(range(0, 24, 4))
    ax.set_xticklabels([f"{i}:00" for i in range(0, 24, 4)])
    ax.set_ylabel("对话次数")
    st.pyplot(fig)

with col_right:
    st.subheader("🔧 工具调用分布")
    tools = ["查天气", "算数学", "讲笑话", "Excel分析", "搜新闻", "查时间"]
    values = [random.randint(10, 80) for _ in range(6)]
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#43e97b']
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.pie(values, labels=tools, autopct='%1.1f%%', colors=colors)
    st.pyplot(fig)

# ========== 实时日志 ==========
st.subheader("📋 实时运行日志")
log_container = st.empty()

# ========== 自动刷新 ==========
if st.button("🔄 刷新数据"):
    st.rerun()

# 模拟实时日志
logs = [
    "[14:23] 用户问天气 → 查询深圳 → 返回'多云 33°C'",
    "[14:25] 用户算数学 → 128×35=4480 → 耗时0.7s",
    "[14:28] 用户上传Excel → 8行5列 → 生成2张图表",
    "[14:30] 用户问记忆 → 检索到3条相关记忆",
    "[14:32] 用户讲笑话 → 返回程序员笑话",
]
for log in logs:
    log_container.write(f"`{log}`")
    time.sleep(0.3)
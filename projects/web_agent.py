import streamlit as st
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="📊 数据分析Agent", page_icon="📊")
st.title("📊 智能数据分析 Agent")
st.caption("上传Excel，AI自动分析+可视化")

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

uploaded_file = st.file_uploader("📁 上传Excel文件", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ 加载成功！{len(df)} 行 × {len(df.columns)} 列")
    
    # 数据预览
    with st.expander("📋 数据预览"):
        st.dataframe(df)
    
    # 自动画图
    st.subheader("📈 自动可视化")
    num_cols = df.select_dtypes(include='number').columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(num_cols) >= 1 and len(df) <= 15:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(df.iloc[:, 0].astype(str), df[num_cols[0]])
            ax.set_title(f'{num_cols[0]} 柱状图')
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    with col2:
        if len(num_cols) >= 1 and len(df) <= 10:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(df[num_cols[0]], labels=df.iloc[:, 0].astype(str), autopct='%1.1f%%')
            ax.set_title(f'{num_cols[0]} 占比')
            st.pyplot(fig)
    
    # AI分析
    st.subheader("🤖 AI 智能分析")
    question = st.text_input("输入你的问题（如：哪个产品销量最高？）")
    
    if question:
        with st.spinner("AI 分析中..."):
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data_summary = df.describe().to_string()
            messages = [
                {"role": "system", "content": "你是数据分析师，用简洁中文回答。"},
                {"role": "user", "content": f"数据统计:\n{data_summary}\n\n问题: {question}"}
            ]
            response = requests.post(
                url,
                json={"model": "deepseek-chat", "messages": messages},
                headers=headers
            )
            result = response.json()["choices"][0]["message"]["content"]
            st.write(result)
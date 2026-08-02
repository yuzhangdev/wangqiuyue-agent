import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

def load_excel(file_path):
    df = pd.read_excel(file_path)
    info = f"行数: {len(df)}, 列名: {list(df.columns)}"
    return df, info

def create_charts(df):
    """自动创建图表"""
    charts = []
    
    # 数值列
    num_cols = df.select_dtypes(include='number').columns.tolist()
    
    if len(num_cols) >= 1:
        # 柱状图 - 用第一列作为标签
        plt.figure(figsize=(10, 5))
        if len(df) <= 15:
            x_col = df.columns[0]
            y_col = num_cols[0]
            plt.bar(df[x_col].astype(str), df[y_col])
            plt.title(f'{y_col} 柱状图')
            plt.xticks(rotation=45)
            plt.tight_layout()
            charts.append(plt.gcf())
            plt.close()
    
    if len(num_cols) >= 1:
        # 饼图
        plt.figure(figsize=(8, 8))
        if len(df) <= 10:
            x_col = df.columns[0]
            y_col = num_cols[0]
            plt.pie(df[y_col], labels=df[x_col].astype(str), autopct='%1.1f%%')
            plt.title(f'{y_col} 占比')
            charts.append(plt.gcf())
            plt.close()
    
    return charts

def analyze_with_ai(data_summary, question):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": "你是数据分析师，用简洁中文回答，50字以内。"},
        {"role": "user", "content": f"数据: {data_summary}\n问题: {question}"}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# 主程序
print("=" * 50)
print("📊 数据分析Agent（带图表）")
print("=" * 50)

file_path = input("Excel文件路径: ").strip().strip('"')
df, info = load_excel(file_path)
print(f"\n📋 数据加载成功！{info}")

# 生成图表
print("\n🎨 生成图表中...")
charts = create_charts(df)
for i, chart in enumerate(charts):
    chart.savefig(f'chart_{i+1}.png')
    print(f"✅ 图表保存: chart_{i+1}.png")

# 交互分析
while True:
    question = input("\n🤔 想问什么？（quit退出）: ")
    if question.lower() == "quit":
        break
    print("\n🤖 分析中...\n")
    print(analyze_with_ai(df.describe().to_string(), question))
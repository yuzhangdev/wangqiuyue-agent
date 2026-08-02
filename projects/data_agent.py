import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 读取Excel文件
def load_excel(file_path):
    """加载Excel文件并返回摘要信息"""
    df = pd.read_excel(file_path)
    info = f"""
📊 数据加载成功！
- 行数: {len(df)}
- 列数: {len(df.columns)}
- 列名: {list(df.columns)}
- 前5行预览:
{df.head().to_string()}
- 基本统计:
{df.describe().to_string()}
"""
    return info

# 分析数据并调用AI解读
def analyze_with_ai(data_summary, question):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": "你是一个专业的数据分析师，擅长从数据中发现洞察。请用简洁的中文回答。"},
        {"role": "user", "content": f"以下是一份数据的摘要信息：\n{data_summary}\n\n用户的问题是：{question}\n\n请根据数据给出分析结论和建议。"}
    ]
    data = {"model": "deepseek-chat", "messages": messages}
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# 主程序
print("=" * 50)
print("📊 数据分析智能Agent")
print("=" * 50)

# 指定你的Excel文件路径
file_path = input("请输入Excel文件路径（直接把文件拖进来）: ").strip().strip('"')

# 加载数据
data_summary = load_excel(file_path)
print(data_summary)

# 交互分析
while True:
    question = input("\n🤔 你想了解什么？（输入 quit 退出）: ")
    if question.lower() == "quit":
        print("再见！")
        break
    
    print("\n🤖 AI分析中...\n")
    analysis = analyze_with_ai(data_summary, question)
    print(analysis)
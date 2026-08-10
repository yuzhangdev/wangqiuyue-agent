from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
)

# ========== 项目数据 ==========
project_data = """
项目名称：王秋月·AI智能助手
开发者：张羽
开发周期：3个月
技术栈：Python、DeepSeek API、LangChain、Streamlit、Flask、FAISS、SQLite
核心功能（13项）：
1. 多轮对话 2. JSON/FAISS/SQLite三级记忆 3. 5工具调用 4. Excel自动分析出图
5. RAG文档问答 6. 自主规划 7. 联网搜索 8. RESTful API 9. WebSocket实时通信
10. 异步并发(5倍提速) 11. 电脑控制 12. 定时提醒 13. AI写邮件自动发送
代码量：约2000行 Python
开源地址：Gitee + GitHub
"""

def generate_report(report_type):
    prompts = {
        "日报": f"根据以下项目数据，生成一份今日工作日报（简洁，200字以内）：\n{project_data}",
        "周报": f"根据以下项目数据，生成一份本周工作周报（含进展、问题、下周计划）：\n{project_data}",
        "项目总结": f"根据以下项目数据，生成一份完整的项目总结报告（含背景、技术方案、成果、展望）：\n{project_data}",
    }
    
    messages = [
        {"role": "system", "content": "你是专业的项目报告撰写助手。格式规范，用词专业。"},
        {"role": "user", "content": prompts.get(report_type, prompts["日报"])}
    ]
    return llm.invoke(messages).content

print("=" * 50)
print("📝 自动报告生成器")
print("=" * 50)

print("\n选择报告类型：")
print("1. 日报")
print("2. 周报")
print("3. 项目总结")

choice = input("\n选(1/2/3): ").strip()
types = {"1": "日报", "2": "周报", "3": "项目总结"}
report_type = types.get(choice, "日报")

print(f"\n⏳ 生成{report_type}中...\n")
report = generate_report(report_type)
print(report)

# 保存到文件
filename = f"{report_type}_{datetime.now().strftime('%Y%m%d')}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(report)
print(f"\n✅ 已保存到 {filename}")
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.5,
)

prompt = """你是职业规划师。为以下背景的人制定11月到明年11月的一年规划：

背景：
- 19岁，大专计算机专业，2026年11月开始实习
- 自学AI Agent开发3个月，独立完成王秋月AI助手项目（13项功能）
- 目标：在深圳找AI Agent开发实习，月薪10k+，后续薪资持续增长
- 技术栈：Python、LangChain、DeepSeek API、Streamlit、Flask、FAISS

要求：
1. 分季度制定目标（Q1-Q4）
2. 每季度包括：技术提升、项目产出、薪资目标
3. 输出Markdown格式
4. 具体可执行，不要空话
"""

result = llm.invoke(prompt)
print(result.content)

with open("career_plan_2026.md", "w", encoding="utf-8") as f:
    f.write(result.content)
print("\n✅ 已保存到 career_plan_2026.md")
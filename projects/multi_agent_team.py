from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.7,
)

def run_agent(agent_name, task):
    """让一个Agent干活"""
    messages = [
        {"role": "system", "content": f"你是{agent_name}，专门负责{task}。回答简洁，100字以内。"},
        {"role": "user", "content": task}
    ]
    result = llm.invoke(messages)
    return result.content

print("=" * 50)
print("🤖 多Agent协作系统")
print("=" * 50)

question = input("\n📋 请输入你的问题: ")

print("\n🔍 研究员Agent工作中...")
research = run_agent("研究员Agent", f"请搜集关于「{question}」的关键信息，列出3个要点")
print(f"研究员: {research}")

print("\n✍️ 写手Agent工作中...")
writer = run_agent("写手Agent", f"基于以下研究，写一段通俗易懂的解释：\n{research}")
print(f"写手: {writer}")

print("\n✅ 审核员Agent工作中...")
reviewer = run_agent("审核员Agent", f"请审核以下内容是否准确、清晰，给出改进建议：\n{writer}")
print(f"审核员: {reviewer}")

print("\n📊 最终总结Agent工作中...")
final = run_agent("总结Agent", f"请综合以下信息，给用户一个最终答案：\n研究: {research}\n文章: {writer}\n审核: {reviewer}")
print(f"\n🎯 最终答案:\n{final}")
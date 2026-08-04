from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
from datetime import datetime
import random
import chromadb
from chromadb.config import Settings

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

# 初始化 ChromaDB 记忆库
chroma_client = chromadb.Client(Settings())
collection = chroma_client.get_or_create_collection("wangqiuyue_memory")

def save_memory(user_input, ai_reply):
    """保存对话到记忆库"""
    collection.add(
        documents=[f"用户: {user_input}\n王秋月: {ai_reply}"],
        ids=[str(datetime.now().timestamp())]
    )

def search_memory(query, n=3):
    """搜索相关记忆"""
    results = collection.query(query_texts=[query], n_results=n)
    if results['documents'][0]:
        return "\n".join(results['documents'][0])
    return ""

# 工具定义
@tool
def get_current_time() -> str:
    """获取当前日期和时间"""
    return f"现在是 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"

@tool
def tell_joke() -> str:
    """讲一个笑话"""
    jokes = [
        "为什么程序员总在晚上工作？因为他们喜欢「黑」科技！",
        "为什么Python程序员不会迷路？因为他们有「import 方向」！",
        "一个布尔值走进酒吧，酒保说：你不是true就是false。布尔值说：我可能是None。",
    ]
    return random.choice(jokes)

@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        expression = expression.strip().replace(" ", "")
        result = eval(expression)
        return f"{expression} = {result}"
    except:
        return "算不出来"

tools = [get_current_time, tell_joke, calculator]

# 创建大模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.7,
)

agent = create_react_agent(llm, tools)

print("=" * 50)
print("🧠 带记忆的王秋月")
print("输入 'quit' 退出")
print("=" * 50)

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() == "quit":
        print("再见！")
        break
    
    # 搜索相关记忆
    memories = search_memory(user_input)
    memory_context = f"以下是之前的相关对话记录：\n{memories}" if memories else ""
    
    messages = [
        {"role": "system", "content": f"你叫王秋月，是个友好热情的AI助手。能用工具就用工具回答。回复简洁。{memory_context}"},
        {"role": "user", "content": user_input}
    ]
    
    result = agent.invoke({"messages": messages})
    ai_reply = result["messages"][-1].content
    
    # 保存记忆
    save_memory(user_input, ai_reply)
    
    print(f"🌙 王秋月: {ai_reply}")
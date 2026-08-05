from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
from datetime import datetime
import random
import numpy as np
import faiss
import json

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

# ========== 向量记忆库 ==========
DIM = 128  # 向量维度
INDEX_FILE = "memory_index.faiss"
DATA_FILE = "memory_data.json"

# 简易文本→向量（用哈希模拟，实际应用会用embedding模型）
def text_to_vector(text, dim=DIM):
    """把文字转成固定长度向量"""
    vec = np.zeros(dim, dtype=np.float32)
    for i, char in enumerate(text):
        vec[i % dim] += ord(char) / 1000.0
    # 归一化
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec

def load_index():
    """加载或创建索引"""
    if os.path.exists(INDEX_FILE):
        return faiss.read_index(INDEX_FILE)
    else:
        return faiss.IndexFlatL2(DIM)

def save_index(index):
    faiss.write_index(index, INDEX_FILE)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def add_memory(user_input, ai_reply):
    """添加记忆"""
    index = load_index()
    data = load_data()
    text = f"用户: {user_input} | 王秋月: {ai_reply}"
    vec = text_to_vector(text).reshape(1, -1)
    index.add(vec)
    data.append(text)
    save_index(index)
    save_data(data)

def search_memory(query, k=3):
    """搜索相关记忆"""
    index = load_index()
    data = load_data()
    if index.ntotal == 0:
        return ""
    vec = text_to_vector(query).reshape(1, -1)
    distances, indices = index.search(vec, min(k, index.ntotal))
    results = [data[i] for i in indices[0] if i < len(data)]
    return "\n".join(results) if results else ""

# ========== 工具 ==========
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
        "向量数据库和普通数据库的区别是什么？一个会思考，一个只会找。",
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

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.7,
)

agent = create_react_agent(llm, tools)

print("=" * 50)
print("🧠 向量记忆王秋月（FAISS版）")
print("输入 'quit' 退出")
print("=" * 50)

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() == "quit":
        print("再见！")
        break
    
    # 搜索相关记忆
    memories = search_memory(user_input)
    memory_context = f"相关记忆：\n{memories}" if memories else "暂无相关记忆"
    
    messages = [
        {"role": "system", "content": f"你叫王秋月，友好热情。回复简洁。\n{memory_context}"},
        {"role": "user", "content": user_input}
    ]
    
    result = agent.invoke({"messages": messages})
    ai_reply = result["messages"][-1].content
    
    # 保存新记忆
    add_memory(user_input, ai_reply)
    
    print(f"🌙 王秋月: {ai_reply}")
import sqlite3
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# ========== 数据库初始化 ==========
DB_FILE = "wangqiuyue_memory.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            ai_reply TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_memory(user_input, ai_reply):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memories (user_input, ai_reply, timestamp) VALUES (?, ?, ?)",
        (user_input, ai_reply, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def search_memory(query, limit=5):
    """模糊搜索记忆"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT user_input, ai_reply FROM memories WHERE user_input LIKE ? OR ai_reply LIKE ? ORDER BY id DESC LIMIT ?",
        (f"%{query}%", f"%{query}%", limit)
    )
    results = c.fetchall()
    conn.close()
    return results

def get_all_memories():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_input, ai_reply, timestamp FROM memories ORDER BY id DESC LIMIT 20")
    results = c.fetchall()
    conn.close()
    return results

def chat_with_ai(user_input, memory_context=""):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": f"你叫王秋月，友好简洁，50字以内。\n{memory_context}"},
        {"role": "user", "content": user_input}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# ========== 主程序 ==========
init_db()
print("=" * 50)
print("🗄️ SQLite 持久记忆王秋月")
print("输入 'quit' 退出，输入 '记忆' 查看所有记忆")
print("=" * 50)

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() == "quit":
        break
    
    if user_input == "记忆":
        memories = get_all_memories()
        if memories:
            print("\n📋 最近的记忆：")
            for u, a, t in memories:
                print(f"[{t}] 你: {u[:30]}... → 王秋月: {a[:30]}...")
        else:
            print("暂无记忆")
        continue
    
    # 搜索相关记忆
    results = search_memory(user_input)
    memory_text = ""
    if results:
        memory_text = "相关记忆：\n" + "\n".join([f"用户: {u} | 王秋月: {a}" for u, a in results])
    
    reply = chat_with_ai(user_input, memory_text)
    save_memory(user_input, reply)
    
    print(f"🌙 王秋月: {reply}")
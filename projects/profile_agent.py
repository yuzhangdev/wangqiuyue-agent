import sqlite3
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
)

# ========== 数据库 ==========
DB_FILE = "user_profile.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS profile (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        ai_reply TEXT,
        timestamp TEXT
    )""")
    conn.commit()
    conn.close()

def set_profile(key, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO profile VALUES (?, ?, ?)",
              (key, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_profile(key):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT value FROM profile WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_profile():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT key, value FROM profile")
    rows = c.fetchall()
    conn.close()
    return dict(rows) if rows else {}

def save_conversation(user_input, ai_reply):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO conversations VALUES (NULL, ?, ?, ?)",
              (user_input, ai_reply, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def analyze_profile():
    """AI分析对话记录，提取用户画像"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_input FROM conversations ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        return "暂无足够对话数据"
    
    history = "\n".join([r[0] for r in rows])
    
    messages = [
        {"role": "system", "content": """分析用户对话记录，提取用户画像。返回JSON格式：
{
    "name": "姓名（如有）",
    "interests": ["兴趣1", "兴趣2"],
    "occupation": "职业/身份",
    "personality": "性格特点",
    "goals": ["目标1"],
    "habits": ["习惯1"]
}
只返回JSON，不要其他内容。"""},
        {"role": "user", "content": f"对话记录：\n{history}"}
    ]
    
    result = llm.invoke(messages)
    return result.content

def update_profile_from_analysis():
    """从AI分析结果更新用户画像"""
    try:
        analysis = analyze_profile()
        profile_data = json.loads(analysis)
        
        for key, value in profile_data.items():
            if isinstance(value, list):
                value = ", ".join(value)
            set_profile(key, value)
        
        return profile_data
    except Exception as e:
        return f"分析失败: {e}"

# ========== 主程序 ==========
init_db()

print("=" * 50)
print("🧠 用户画像系统")
print("命令: 聊天内容 | 更新画像 | 查看画像 | quit")
print("=" * 50)

while True:
    user_input = input("\n👤 你: ")
    
    if user_input.lower() == "quit":
        break
    
    if user_input == "更新画像":
        print("🤖 分析对话记录中...")
        profile = update_profile_from_analysis()
        print(f"✅ 画像已更新:\n{json.dumps(profile, ensure_ascii=False, indent=2)}")
        continue
    
    if user_input == "查看画像":
        profile = get_all_profile()
        if profile:
            print(f"\n📊 用户画像:")
            for k, v in profile.items():
                print(f"  {k}: {v}")
        else:
            print("暂无画像，先聊几句再更新")
        continue
    
    # 正常对话
    profile = get_all_profile()
    profile_text = "用户画像：\n" + "\n".join([f"{k}: {v}" for k, v in profile.items()]) if profile else ""
    
    messages = [
        {"role": "system", "content": f"你叫王秋月。根据用户画像提供个性化回复。{profile_text}"},
        {"role": "user", "content": user_input}
    ]
    reply = llm.invoke(messages).content
    
    save_conversation(user_input, reply)
    print(f"🌙 王秋月: {reply}")
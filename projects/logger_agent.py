import logging
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# ========== 日志配置 ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("wangqiuyue.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("王秋月")

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

def chat(user_input):
    logger.info(f"用户输入: {user_input}")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，友好简洁，50字以内。"},
        {"role": "user", "content": user_input}
    ]
    
    try:
        start = datetime.now()
        response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        elapsed = (datetime.now() - start).total_seconds()
        
        logger.info(f"AI回复: {reply} | 耗时: {elapsed:.2f}s")
        return reply
    except Exception as e:
        logger.error(f"调用失败: {str(e)}")
        return "抱歉，我出问题了"

print("=" * 50)
print("📋 带日志的王秋月")
print("输入 'quit' 退出，输入 '日志' 查看最近日志")
print("=" * 50)

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() == "quit":
        logger.info("对话结束")
        break
    
    if user_input == "日志":
        try:
            with open("wangqiuyue.log", "r", encoding="utf-8") as f:
                lines = f.readlines()[-10:]
                print("\n📋 最近10条日志：")
                for line in lines:
                    print(line.strip())
        except:
            print("暂无日志")
        continue
    
    reply = chat(user_input)
    print(f"🌙 王秋月: {reply}")
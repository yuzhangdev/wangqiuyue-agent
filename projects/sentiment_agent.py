from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.1,
)

def analyze_sentiment(text):
    prompt = f"""分析以下文本的情感，只返回JSON格式：
{{"sentiment": "正面/负面/中性", "emotion": "开心/难过/愤怒/焦虑/平静/兴奋", "confidence": 0.0-1.0, "reply_style": "如何回复的建议"}}

文本：{text}"""
    result = llm.invoke(prompt)
    return result.content

def smart_reply(text, analysis):
    """根据情感给出智能回复"""
    prompt = f"""用户说：{text}
情感分析：{analysis}
请根据用户的情感状态，用王秋月的身份给出贴心回复。30字以内。"""
    result = llm.invoke(prompt)
    return result.content

print("=" * 50)
print("💭 王秋月 · 情感分析")
print("输入 'quit' 退出")
print("=" * 50)

while True:
    text = input("\n👤 你: ")
    if text.lower() == "quit":
        break
    
    print("🔍 分析中...")
    analysis = analyze_sentiment(text)
    print(f"📊 分析: {analysis}")
    
    reply = smart_reply(text, analysis)
    print(f"🌙 王秋月: {reply}")
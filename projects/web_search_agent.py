import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
)

def search_bing(query, num=5):
    """用Bing搜索，返回标题和摘要"""
    try:
        url = f"https://www.bing.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        for item in soup.select("li.b_algo")[:num]:
            title = item.select_one("h2")
            desc = item.select_one("p")
            if title:
                results.append({
                    "title": title.get_text(strip=True),
                    "desc": desc.get_text(strip=True) if desc else "无描述"
                })
        return results
    except Exception as e:
        return [{"title": "搜索失败", "desc": str(e)}]

def ai_summarize(query, search_results):
    """让AI总结搜索结果"""
    context = "\n".join([f"- {r['title']}: {r['desc']}" for r in search_results])
    messages = [
        {"role": "system", "content": "你是一个信息总结助手。根据搜索结果，用简洁的中文回答用户问题。100字以内。"},
        {"role": "user", "content": f"用户问题：{query}\n\n搜索结果：\n{context}\n\n请总结回答："}
    ]
    result = llm.invoke(messages)
    return result.content

print("=" * 50)
print("🌐 王秋月联网搜索")
print("输入 'quit' 退出")
print("=" * 50)

while True:
    query = input("\n🔍 搜什么？: ")
    if query.lower() == "quit":
        print("再见！")
        break
    
    print("⏳ 搜索中...")
    results = search_bing(query)
    
    if results:
        print(f"\n📋 找到 {len(results)} 条结果：")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}")
        
        print("\n🤖 AI总结中...")
        summary = ai_summarize(query, results)
        print(f"\n📝 王秋月总结: {summary}")
    else:
        print("❌ 没搜到结果")
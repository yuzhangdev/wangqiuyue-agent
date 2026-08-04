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

def split_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

def simple_search(chunks, query):
    scores = []
    for chunk in chunks:
        score = 0
        for char in query:
            if char in chunk:
                score += 1
        scores.append(score)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:3]
    result = [chunks[i] for i, _ in ranked]
    if all(s == 0 for s in scores):
        return chunks[:3]
    return result

def ask_with_context(query, context_chunks):
    context = "\n\n".join(context_chunks)
    messages = [
        {"role": "system", "content": "你是一个文档助手。请根据提供的文档内容回答问题。如果文档中没有相关信息，就说'文档中没有提到'。回答简洁。"},
        {"role": "user", "content": f"文档内容：\n{context}\n\n问题：{query}"}
    ]
    result = llm.invoke(messages)
    return result.content

print("=" * 50)
print("📚 RAG 文档问答系统")
print("=" * 50)

file_path = input("\n📁 输入文档路径（TXT文件）: ").strip().strip('"')

try:
    with open(file_path, "r", encoding="utf-8") as f:
        doc_text = f.read()
    
    chunks = split_text(doc_text)
    print(f"✅ 文档加载成功！共 {len(doc_text)} 字符，切成 {len(chunks)} 块")
    
    while True:
        query = input("\n🤔 想问什么？（quit退出）: ")
        if query.lower() == "quit":
            break
        
        if len(chunks) <= 3:
            related = chunks
        else:
            related = simple_search(chunks, query)
        
        if related:
            answer = ask_with_context(query, related)
            print(f"\n📖 回答: {answer}")
        else:
            print("\n❌ 文档中没有相关内容")

except FileNotFoundError:
    print("❌ 文件不存在，请检查路径")
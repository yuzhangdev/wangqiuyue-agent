from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
)

# 1. 加载文档
file_path = input("📁 输入TXT文档路径: ").strip().strip('"')

with open(file_path, "r", encoding="utf-8") as f:
    doc_text = f.read()

print(f"✅ 加载 {len(doc_text)} 字符")

# 2. 分块（LangChain 专业分块器）
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
)
chunks = splitter.split_text(doc_text)
print(f"✅ 切成 {len(chunks)} 块")

# 3. 简易检索
def search_chunks(query, chunks, k=3):
    scores = []
    for i, chunk in enumerate(chunks):
        score = sum(1 for c in query if c in chunk)
        scores.append((i, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [chunks[i] for i, _ in scores[:k]]

# 4. 问答链
prompt = ChatPromptTemplate.from_template(
    """根据以下文档内容回答问题。如果文档中没有答案，就说"文档中未提及"。

文档：
{context}

问题：{question}

回答："""
)

qa_chain = prompt | llm | StrOutputParser()

# 5. 交互
print("\n" + "=" * 50)
print("📚 LangChain RAG 问答")
print("输入 'quit' 退出")
print("=" * 50)

while True:
    query = input("\n🤔 问题: ")
    if query.lower() == "quit":
        break
    
    related = search_chunks(query, chunks)
    context = "\n\n".join(related)
    
    answer = qa_chain.invoke({"context": context, "question": query})
    print(f"\n📖 回答: {answer}")
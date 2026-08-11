from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
)

KNOWLEDGE_FILE = "knowledge_graph.json"

def load_knowledge():
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"nodes": [], "edges": []}

def save_knowledge(data):
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_knowledge(text):
    """从文本中提取知识点和关系"""
    prompt = f"""从以下文本中提取知识点和关系，返回JSON：
{{"nodes": ["知识点1", "知识点2"], "edges": [{{"from": "知识点1", "to": "知识点2", "relation": "关系"}}]}}
只返回JSON。

文本：{text}"""
    result = llm.invoke(prompt)
    try:
        return json.loads(result.content)
    except:
        return {"nodes": [], "edges": []}

def query_knowledge(question):
    """基于知识图谱回答问题"""
    kg = load_knowledge()
    kg_str = json.dumps(kg, ensure_ascii=False)
    
    prompt = f"""根据以下知识图谱回答问题：
知识图谱：{kg_str}
问题：{question}
如果知识图谱中没有相关信息，就说"我还没学到这个"。
回答简洁，50字以内。"""
    result = llm.invoke(prompt)
    return result.content

print("=" * 50)
print("🧠 王秋月 · 知识图谱")
print("输入 '学' 教王秋月新知识")
print("输入 '问' 提问")
print("输入 '查看' 查看知识图谱")
print("输入 'quit' 退出")
print("=" * 50)

while True:
    cmd = input("\n📝 操作: ").strip()
    
    if cmd.lower() == "quit":
        break
    
    if cmd == "查看":
        kg = load_knowledge()
        print(f"\n📊 节点({len(kg['nodes'])}个): {kg['nodes']}")
        print(f"🔗 关系({len(kg['edges'])}个):")
        for e in kg['edges']:
            print(f"  {e['from']} --{e['relation']}--> {e['to']}")
        continue
    
    if cmd == "学":
        text = input("📖 教王秋月: ")
        new_knowledge = extract_knowledge(text)
        kg = load_knowledge()
        for node in new_knowledge["nodes"]:
            if node not in kg["nodes"]:
                kg["nodes"].append(node)
        for edge in new_knowledge["edges"]:
            if edge not in kg["edges"]:
                kg["edges"].append(edge)
        save_knowledge(kg)
        print(f"✅ 学到了 {len(new_knowledge['nodes'])} 个知识点")
        continue
    
    if cmd == "问":
        question = input("🤔 问: ")
        answer = query_knowledge(question)
        print(f"🌙 王秋月: {answer}")
        continue
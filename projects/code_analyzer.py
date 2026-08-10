import os
import requests
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

def read_python_files(folder):
    """读取所有Python文件"""
    code_files = {}
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                    code_files[f] = {
                        "path": path,
                        "lines": len(fp.readlines()),
                        "size": os.path.getsize(path)
                    }
    return code_files

def analyze_with_ai(files_info, question):
    """让AI分析代码库"""
    summary = f"项目共有 {len(files_info)} 个Python文件。\n"
    for name, info in list(files_info.items())[:20]:
        summary += f"- {name}: {info['lines']}行\n"
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你是代码分析专家。根据项目文件信息回答用户问题。"},
        {"role": "user", "content": f"项目信息：\n{summary}\n\n问题：{question}"}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

print("=" * 50)
print("🔍 王秋月 · 代码分析器")
print("=" * 50)

folder = input("\n📁 项目路径（直接回车=当前项目）: ").strip()
if not folder:
    folder = "."

print("⏳ 扫描代码...")
files = read_python_files(folder)

total_lines = sum(f["lines"] for f in files.values())
print(f"\n📊 统计：")
print(f"  Python文件: {len(files)}个")
print(f"  总代码行数: {total_lines}行")

print("\n📋 文件列表：")
for name, info in sorted(files.items(), key=lambda x: x[1]["lines"], reverse=True)[:10]:
    print(f"  {name}: {info['lines']}行")

question = input("\n🤔 问什么？（如：这个项目主要功能是什么？）: ")
print("\n🤖 分析中...")
answer = analyze_with_ai(files, question)
print(f"\n📝 分析结果:\n{answer}")
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

def ask_one(question):
    """单次提问"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "回复极度简洁，15字以内。"},
        {"role": "user", "content": question}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def batch_ask(questions, max_workers=5):
    """批量并发提问"""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ask_one, q): q for q in questions}
        for future in futures:
            q = futures[future]
            try:
                results[q] = future.result()
            except Exception as e:
                results[q] = f"失败: {e}"
    return results

print("=" * 50)
print("📋 王秋月 · 批量任务处理器")
print("=" * 50)

# 任务列表
tasks = [
    "深圳今天天气",
    "Python是什么",
    "1加1等于几",
    "中国的首都是哪里",
    "推荐一本编程书",
    "什么是机器学习",
    "如何学好编程",
    "今天星期几",
    "什么是API",
    "什么是Agent",
]

print(f"\n📋 共 {len(tasks)} 个任务\n")

# 顺序执行
print("🐢 顺序执行...")
start = time.time()
for task in tasks:
    reply = ask_one(task)
    print(f"  Q: {task[:20]} → {reply}")
seq_time = time.time() - start
print(f"  耗时: {seq_time:.2f}秒\n")

# 批量并发
print("🚀 批量并发执行...")
start = time.time()
results = batch_ask(tasks, max_workers=5)
for q, reply in results.items():
    print(f"  Q: {q[:20]} → {reply}")
con_time = time.time() - start
print(f"  耗时: {con_time:.2f}秒\n")

print(f"📊 对比：顺序 {seq_time:.1f}s vs 并发 {con_time:.1f}s")
if con_time < seq_time:
    print(f"⚡ 并发提速 {(seq_time/con_time):.1f}倍！")
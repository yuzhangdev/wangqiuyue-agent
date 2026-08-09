import asyncio
import aiohttp
import time
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

async def call_deepseek(session, message):
    """异步调用DeepSeek"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "回复极度简洁，10字以内。"},
            {"role": "user", "content": message}
        ]
    }
    async with session.post(url, json=data, headers=headers) as resp:
        result = await resp.json()
        return result["choices"][0]["message"]["content"]

async def main():
    questions = [
        "1+1等于几",
        "中国的首都是哪里",
        "天空为什么是蓝色的",
        "Python是什么",
        "今天星期几"
    ]
    
    print("=" * 50)
    print("⚡ 异步并发测试：同时问5个问题")
    print("=" * 50)
    
    # 方式1：顺序执行
    print("\n🐢 顺序执行...")
    start = time.time()
    async with aiohttp.ClientSession() as session:
        for q in questions:
            reply = await call_deepseek(session, q)
            print(f"  Q: {q} → A: {reply}")
    seq_time = time.time() - start
    print(f"  耗时: {seq_time:.2f}秒")
    
    # 方式2：并发执行
    print("\n🚀 并发执行...")
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [call_deepseek(session, q) for q in questions]
        replies = await asyncio.gather(*tasks)
        for q, r in zip(questions, replies):
            print(f"  Q: {q} → A: {r}")
    con_time = time.time() - start
    print(f"  耗时: {con_time:.2f}秒")
    
    # 对比
    print(f"\n📊 对比：顺序 {seq_time:.1f}s vs 并发 {con_time:.1f}s")
    if con_time < seq_time:
        print(f"⚡ 并发快了 {(seq_time/con_time):.1f}倍！")
    else:
        print("网络波动，差别不大")

# 先装aiohttp
import subprocess
try:
    import aiohttp
except ImportError:
    print("📦 正在安装 aiohttp...")
    subprocess.run(["pip", "install", "--user", "aiohttp", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "--trusted-host", "pypi.tuna.tsinghua.edu.cn"])

asyncio.run(main())
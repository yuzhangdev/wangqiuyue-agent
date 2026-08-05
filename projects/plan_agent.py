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

def make_plan(task):
    """让AI制定执行计划"""
    messages = [
        {"role": "system", "content": "你是一个任务规划师。收到任务后，把它拆成3-5个步骤，每步简洁明了。格式：1. xxx 2. xxx"},
        {"role": "user", "content": f"任务：{task}\n请制定执行计划："}
    ]
    result = llm.invoke(messages)
    return result.content

def execute_step(step, previous_results=""):
    """执行单个步骤"""
    context = f"之前的执行结果：\n{previous_results}" if previous_results else ""
    messages = [
        {"role": "system", "content": "你是一个执行助手。根据任务步骤和已有信息，执行当前步骤并输出结果。回答简洁，50字以内。"},
        {"role": "user", "content": f"{context}\n当前步骤：{step}\n请执行并输出结果："}
    ]
    result = llm.invoke(messages)
    return result.content

def summarize(plan, results):
    """总结所有步骤"""
    messages = [
        {"role": "system", "content": "你是总结助手。根据计划和执行结果，给用户一个完整总结。"},
        {"role": "user", "content": f"计划：\n{plan}\n\n执行结果：\n{results}\n\n请给出总结："}
    ]
    result = llm.invoke(messages)
    return result.content

print("=" * 50)
print("🧠 自主规划Agent")
print("=" * 50)

task = input("\n📋 输入任务: ")

# 第一步：制定计划
print("\n📝 制定计划中...")
plan = make_plan(task)
print(f"计划:\n{plan}")

# 第二步：逐步执行
steps = [s.strip() for s in plan.split("\n") if s.strip() and s[0].isdigit()]
results = []
for i, step in enumerate(steps, 1):
    print(f"\n⚡ 执行第{i}步...")
    prev = "\n".join(results)
    result = execute_step(step, prev)
    results.append(f"步骤{i}: {result}")
    print(f"结果: {result}")

# 第三步：总结
print("\n📊 总结中...")
final = summarize(plan, "\n".join(results))
print(f"\n🎯 最终结果:\n{final}")
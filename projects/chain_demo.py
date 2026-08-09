from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.7,
)

# ========== 定义三个链 ==========

# 链1：翻译成英文
translate_prompt = ChatPromptTemplate.from_template(
    "把以下中文翻译成英文：{text}"
)
translate_chain = translate_prompt | llm | StrOutputParser()

# 链2：润色英文
polish_prompt = ChatPromptTemplate.from_template(
    "润色以下英文，让它更正式、更地道：{text}"
)
polish_chain = polish_prompt | llm | StrOutputParser()

# 链3：总结
summarize_prompt = ChatPromptTemplate.from_template(
    "用一句话总结以下英文内容的核心意思（中文）：{text}"
)
summarize_chain = summarize_prompt | llm | StrOutputParser()

# ========== 组装流水线 ==========
full_chain = translate_chain | polish_chain | summarize_chain

print("=" * 50)
print("🔗 LangChain 流水线演示")
print("中文 → 翻译 → 润色 → 总结")
print("=" * 50)

user_text = input("\n📝 输入一段中文: ")

print("\n⚙️ 流水线处理中...\n")

# 步骤1：翻译
print("1️⃣ 翻译中...")
english = translate_chain.invoke({"text": user_text})
print(f"英文: {english}")

# 步骤2：润色
print("\n2️⃣ 润色中...")
polished = polish_chain.invoke({"text": english})
print(f"润色后: {polished}")

# 步骤3：总结
print("\n3️⃣ 总结中...")
summary = summarize_chain.invoke({"text": polished})
print(f"总结: {summary}")

# 一步到位
print("\n🚀 一步到位（链式调用）:")
result = full_chain.invoke({"text": user_text})
print(f"最终结果: {result}")
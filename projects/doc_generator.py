from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
)

TEMPLATES = {
    "1": ("API接口文档", "为以下功能生成Markdown格式的API接口文档，包含接口路径、请求方法、参数、返回示例：{topic}"),
    "2": ("项目README", "为以下项目生成Markdown格式的README文档，包含简介、功能、技术栈、快速开始：{topic}"),
    "3": ("会议纪要", "根据以下内容生成Markdown格式的会议纪要，包含时间、参会人、议题、决议、待办：{topic}"),
    "4": ("技术方案", "为以下需求生成Markdown格式的技术方案文档：{topic}"),
}

def generate_doc(doc_type, topic):
    template = TEMPLATES[doc_type][1]
    prompt = template.format(topic=topic)
    result = llm.invoke(prompt)
    return result.content

print("=" * 50)
print("📄 王秋月 · 文档生成器")
print("=" * 50)

print("\n文档类型：")
for key, (name, _) in TEMPLATES.items():
    print(f"  {key}. {name}")

doc_type = input("\n选类型: ").strip()
if doc_type not in TEMPLATES:
    doc_type = "1"

topic = input(f"📝 {TEMPLATES[doc_type][0]} - 输入主题: ")

print(f"\n⏳ 生成中...\n")
doc = generate_doc(doc_type, topic)
print(doc)

# 保存
filename = f"{TEMPLATES[doc_type][0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(doc)
print(f"\n✅ 已保存到 {filename}")
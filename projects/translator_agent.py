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

LANGUAGES = {
    "1": ("中文→英文", "把以下中文翻译成英文：{text}"),
    "2": ("英文→中文", "把以下英文翻译成中文：{text}"),
    "3": ("中文→日文", "把以下中文翻译成日文：{text}"),
    "4": ("中文→韩文", "把以下中文翻译成韩文：{text}"),
    "5": ("中文→法文", "把以下中文翻译成法文：{text}"),
    "6": ("自动检测→中文", "把以下内容翻译成中文：{text}"),
}

def translate(text, mode):
    prompt_template = LANGUAGES[mode][1]
    prompt = prompt_template.format(text=text)
    result = llm.invoke(prompt)
    return result.content

print("=" * 50)
print("🌍 王秋月 · 多语言翻译")
print("=" * 50)

print("\n翻译模式：")
for key, (name, _) in LANGUAGES.items():
    print(f"  {key}. {name}")

mode = input("\n选模式: ").strip()
if mode not in LANGUAGES:
    mode = "1"

text = input("📝 输入文本: ")
print(f"\n🔄 {LANGUAGES[mode][0]}...\n")
result = translate(text, mode)
print(f"✅ 结果:\n{result}")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def send_email(to_email, subject, body, from_email, password):
    """发送邮件"""
    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # QQ邮箱
        if "qq.com" in from_email:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 163邮箱
        elif "163.com" in from_email:
            server = smtplib.SMTP_SSL("smtp.163.com", 465)
        else:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return "✅ 邮件发送成功！"
    except Exception as e:
        return f"❌ 发送失败: {str(e)}"

def ai_compose_email(task):
    """让AI写邮件内容"""
    messages = [
        {"role": "system", "content": "你是邮件助手。根据用户要求写正式邮件。输出格式：主题：xxx\n正文：xxx"},
        {"role": "user", "content": task}
    ]
    result = llm.invoke(messages)
    content = result.content
    # 解析主题和正文
    lines = content.split("\n")
    subject = ""
    body_lines = []
    for line in lines:
        if line.startswith("主题：") or line.startswith("主题:"):
            subject = line.replace("主题：", "").replace("主题:", "").strip()
        else:
            body_lines.append(line)
    body = "\n".join(body_lines).strip()
    return subject, body

print("=" * 50)
print("📧 王秋月邮件助手")
print("=" * 50)

# 配置邮箱（演示用，实际使用时从.env读取）
print("\n⚠️ 使用QQ邮箱需要开启SMTP服务并获取授权码")
print("设置方法：QQ邮箱 → 设置 → 账户 → POP3/SMTP服务 → 开启 → 获取授权码\n")

from_email = input("你的邮箱: ").strip()
password = input("邮箱授权码（不是登录密码）: ").strip()
to_email = input("收件人邮箱: ").strip()
task = input("邮件内容（如：写一封面试感谢信）: ").strip()

print("\n🤖 AI写邮件中...")
subject, body = ai_compose_email(task)
print(f"\n📋 预览：")
print(f"收件人: {to_email}")
print(f"主题: {subject}")
print(f"正文:\n{body}")

confirm = input("\n发送？(y/n): ").strip().lower()
if confirm == "y":
    result = send_email(to_email, subject, body, from_email, password)
    print(result)
else:
    print("已取消")
import schedule
import time
import pyttsx3
import threading
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")

engine = pyttsx3.init()
engine.setProperty('rate', 180)

reminders = []

def speak(text):
    print(f"🔔 {text}")
    engine.say(text)
    engine.runAndWait()

def add_reminder(time_str, message):
    """添加提醒"""
    def job():
        speak(f"⏰ 提醒：{message}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 已提醒: {message}")
    
    schedule.every().day.at(time_str).do(job)
    reminders.append((time_str, message))
    return f"✅ 已添加提醒：每天 {time_str} - {message}"

def list_reminders():
    if not reminders:
        return "暂无提醒"
    return "\n".join([f"{i+1}. {t} - {m}" for i, (t, m) in enumerate(reminders)])

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 后台线程运行调度器
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

print("=" * 50)
print("⏰ 王秋月 · 定时提醒")
print("命令: 添加提醒 HH:MM 内容 | 查看提醒 | quit")
print("示例: 添加提醒 16:00 该喝水了")
print("=" * 50)

while True:
    cmd = input("\n⏰ 命令: ")
    
    if cmd.lower() == "quit":
        speak("好的，提醒服务关闭")
        break
    
    if cmd.startswith("添加提醒"):
        parts = cmd.replace("添加提醒 ", "").split(" ", 1)
        if len(parts) >= 2:
            time_str, message = parts[0], parts[1]
            print(add_reminder(time_str, message))
        else:
            print("格式：添加提醒 HH:MM 内容")
    
    elif cmd == "查看提醒":
        print(list_reminders())
    
    elif cmd == "测试":
        speak("测试提醒，王秋月正在运行中")
import pyautogui
import requests
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 安全设置：移动到左上角停止
pyautogui.FAILSAFE = True

def call_deepseek(user_input):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": """你是一个电脑控制助手。根据用户指令，只输出命令，不要多说话。
命令格式：
- 打开软件：[OPEN:软件名]
- 输入文字：[TYPE:文字内容]
- 按快捷键：[HOTKEY:键1+键2]
- 截屏：[SCREENSHOT]
- 移动鼠标：[MOVE:x,y]
- 点击：[CLICK]
- 获取鼠标位置：[POSITION]
- 聊天模式：[CHAT:回复内容]"""},
        {"role": "user", "content": user_input}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def execute_command(cmd):
    """执行电脑命令"""
    try:
        if cmd.startswith("[CHAT:"):
            return cmd[6:-1]
        
        elif cmd.startswith("[OPEN:"):
            app = cmd[6:-1]
            os.system(f"start {app}")
            return f"✅ 已打开 {app}"
        
        elif cmd.startswith("[TYPE:"):
            text = cmd[6:-1]
            pyautogui.write(text, interval=0.1)
            return f"✅ 已输入: {text}"
        
        elif cmd.startswith("[HOTKEY:"):
            keys = cmd[8:-1].split("+")
            pyautogui.hotkey(*keys)
            return f"✅ 已按快捷键: {'+'.join(keys)}"
        
        elif cmd == "[SCREENSHOT]":
            pyautogui.screenshot("screenshot.png")
            return "✅ 截图已保存"
        
        elif cmd.startswith("[MOVE:"):
            coords = cmd[6:-1].split(",")
            x, y = int(coords[0]), int(coords[1])
            pyautogui.moveTo(x, y, duration=0.5)
            return f"✅ 鼠标已移动到 ({x}, {y})"
        
        elif cmd == "[CLICK]":
            pyautogui.click()
            return "✅ 已点击"
        
        elif cmd == "[POSITION]":
            x, y = pyautogui.position()
            return f"🖱️ 当前位置: ({x}, {y})"
        
        return cmd
    except Exception as e:
        return f"❌ 执行失败: {e}"

print("=" * 50)
print("🖥️ 王秋月 · 电脑控制模式")
print("命令: 打开软件 | 输入文字 | 截屏 | 快捷键")
print("输入 'quit' 退出")
print("⚠️ 鼠标移到左上角可紧急停止")
print("=" * 50)

while True:
    user_input = input("\n💻 命令: ")
    if user_input.lower() == "quit":
        break
    
    ai_cmd = call_deepseek(user_input)
    print(f"🤖 执行: {ai_cmd}")
    result = execute_command(ai_cmd)
    print(f"结果: {result}")
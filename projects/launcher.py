import os
import sys
import subprocess
import socket

def check_port(port):
    """检查端口是否被占用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def launch():
    print("=" * 50)
    print("🚀 王秋月 · 一键启动器")
    print("=" * 50)
    print("\n选择启动模式：")
    print("1. 终极版（网页对话+工具+画像）")
    print("2. 数据大屏")
    print("3. RESTful API")
    print("4. 语音对话")
    print("5. 代码分析器")
    print("6. 全部启动")
    print("0. 退出")
    
    choice = input("\n选: ").strip()
    
    python = sys.executable
    
    apps = {
        "1": ("终极版", f"streamlit run wangqiuyue_ultimate.py --server.port 8501"),
        "2": ("数据大屏", f"streamlit run dashboard_agent.py --server.port 8502"),
        "3": ("API服务", f"api_agent.py"),
        "4": ("语音对话", f"simple_hotkey.py"),
        "5": ("代码分析器", f"code_analyzer.py"),
    }
    
    if choice == "0":
        print("👋 退出")
        return
    
    if choice == "6":
        print("\n⚠️ 将启动多个窗口...")
        for key, (name, cmd) in apps.items():
            print(f"🚀 启动 {name}...")
            subprocess.Popen(f"start \"{name}\" python -m {cmd}", shell=True)
        print("\n✅ 全部启动完成！")
        return
    
    if choice in apps:
        name, cmd = apps[choice]
        print(f"\n🚀 启动 {name}...")
        if "streamlit" in cmd:
            os.system(f"python -m {cmd}")
        else:
            os.system(f"python {cmd}")
    else:
        print("无效选择")

if __name__ == "__main__":
    launch()
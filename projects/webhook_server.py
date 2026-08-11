from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

app = Flask(__name__)

def chat_ai(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，回复简洁，50字以内。"},
        {"role": "user", "content": text}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

@app.route("/webhook", methods=["POST"])
def webhook():
    """接收外部消息的Webhook接口"""
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "缺少message参数"}), 400
    
    user_message = data["message"]
    sender = data.get("sender", "未知")
    
    print(f"📩 收到 {sender} 的消息: {user_message}")
    
    reply = chat_ai(user_message)
    
    print(f"📤 回复: {reply}")
    
    return jsonify({
        "sender": sender,
        "message": user_message,
        "reply": reply,
        "timestamp": __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/")
def home():
    return """
    <h1>🌙 王秋月 Webhook 服务</h1>
    <p>接收消息端点：POST /webhook</p>
    <p>格式：{"message": "你的消息", "sender": "发送者名称"}</p>
    <hr>
    <h3>📱 接入方式：</h3>
    <ul>
        <li>企业微信/钉钉机器人</li>
        <li>微信公众号</li>
        <li>其他系统回调</li>
    </ul>
    """

if __name__ == "__main__":
    print("=" * 50)
    print("🌙 王秋月 Webhook 服务")
    print("接收端点: http://localhost:5000/webhook")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
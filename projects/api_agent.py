from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

app = Flask(__name__)

def call_deepseek(user_message):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "你叫王秋月，友好简洁，50字以内。"},
        {"role": "user", "content": user_message}
    ]
    response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

@app.route("/")
def home():
    return """
    <h1>🌙 王秋月 API</h1>
    <p>使用方法：POST /chat</p>
    <p>参数：{"message": "你的问题"}</p>
    <p>示例：curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message":"你好"}'</p>
    """

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "请提供message参数"}), 400
    
    user_message = data["message"]
    reply = call_deepseek(user_message)
    
    return jsonify({
        "user": user_message,
        "reply": reply,
        "model": "deepseek-chat"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "agent": "王秋月"})

if __name__ == "__main__":
    print("=" * 50)
    print("🌙 王秋月 API 服务启动")
    print("地址: http://localhost:5000")
    print("测试: curl -X POST http://localhost:5000/chat -H \"Content-Type: application/json\" -d '{\"message\":\"你好\"}'")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
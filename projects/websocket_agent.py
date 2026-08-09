from flask import Flask, render_template_string
from flask_sock import Sock
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(r"C:\Users\张\Desktop\agent_study\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

app = Flask(__name__)
sock = Sock(app)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🌙 王秋月 WebSocket</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        #chat { border: 1px solid #ddd; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; border-radius: 10px; }
        .user { color: #667eea; }
        .ai { color: #764ba2; }
        input { width: 80%; padding: 10px; border-radius: 10px; border: 1px solid #ddd; }
        button { padding: 10px 20px; border-radius: 10px; background: #667eea; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h2>🌙 王秋月 WebSocket 实时聊天</h2>
    <div id="chat"></div>
    <input id="msg" placeholder="输入消息..." onkeypress="if(event.key==='Enter') send()">
    <button onclick="send()">发送</button>

    <script>
        var ws = new WebSocket("ws://" + location.host + "/ws");
        ws.onmessage = function(e) {
            var data = JSON.parse(e.data);
            var chat = document.getElementById("chat");
            chat.innerHTML += '<p class="user">👤 ' + data.user + '</p>';
            chat.innerHTML += '<p class="ai">🌙 ' + data.reply + '</p>';
            chat.scrollTop = chat.scrollHeight;
        };
        function send() {
            var input = document.getElementById("msg");
            var msg = input.value;
            if (msg) {
                ws.send(msg);
                input.value = "";
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@sock.route("/ws")
def chat_ws(ws):
    while True:
        user_msg = ws.receive()
        if user_msg is None:
            break
        
        # 调用DeepSeek
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        messages = [
            {"role": "system", "content": "你叫王秋月，友好简洁，50字以内。"},
            {"role": "user", "content": user_msg}
        ]
        response = requests.post(url, json={"model": "deepseek-chat", "messages": messages}, headers=headers)
        reply = response.json()["choices"][0]["message"]["content"]
        
        ws.send(json.dumps({"user": user_msg, "reply": reply}))

if __name__ == "__main__":
    print("=" * 50)
    print("🌙 王秋月 WebSocket 服务")
    print("浏览器打开: http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
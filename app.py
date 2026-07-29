from flask import Flask, render_template_string, request, jsonify
from google import genai

app = Flask(__name__)

# کلیلی زیرەکی دەستکردەکەت لێرە دابنە
client = genai.Client(api_key="لێرە_کلیلی_Gemini_API_کەت_دابنە")

# دیزاینی وێبسایتەکە (HTML & CSS & JavaScript) لەهەمان فایلدا
html_template = """
<!DOCTYPE html>
<html lang="ckb" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>یاریدەدەری کۆدی پایتۆن</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            width: 100%;
            max-width: 650px;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            height: 85vh;
        }
        h2 { text-align: center; color: #2c3e50; margin-top: 0; }
        .chat-box {
            flex: 1;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            overflow-y: auto;
            margin-bottom: 15px;
            background: #fafafa;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 8px;
            max-width: 85%;
            word-wrap: break-word;
            line-height: 1.5;
        }
        .user-msg { 
            background: #3498db; 
            color: white; 
            margin-left: auto; 
            text-align: right; 
        }
        .ai-msg { 
            background: #e2e8f0; 
            color: #2d3748; 
            margin-right: auto; 
            text-align: left; 
            direction: ltr; 
            font-family: Consolas, monospace; 
            white-space: pre-wrap; 
            font-size: 14px;
        }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 15px;
            outline: none;
        }
        input[type="text"]:focus { border-color: #3498db; }
        button {
            padding: 12px 24px;
            background: #2ecc71;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 15px;
            transition: background 0.2s;
        }
        button:hover { background: #27ae60; }
    </style>
</head>
<body>

    <div class="chat-container">
        <h2>یاریدەدەری کۆدی پایتۆن</h2>
        <div class="chat-box" id="chatBox">
            <div class="message ai-msg" style="direction: rtl; font-family: Arial;">سڵاو! هەر کۆدێکی پایتۆنت دەوێت لێرە داوای بکە تا بە زیرەکی دەستکرد بۆت دروست بکەم.</div>
        </div>
        <div class="input-group">
            <input type="text" id="userInput" placeholder="بۆ نموونە: کۆدێکی پایتۆن بۆ حسابکردنی تەمەن بنووسە..." onkeydown="checkEnter(event)">
            <button onclick="sendRequest()">ناردن</button>
        </div>
    </div>

    <script>
        async function sendRequest() {
            const inputField = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const promptText = inputField.value.trim();

            if (!promptText) return;

            chatBox.innerHTML += `<div class="message user-msg">${escapeHtml(promptText)}</div>`;
            inputField.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/generate-code', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: promptText })
                });
                
                const data = await response.json();
                
                if (data.code) {
                    chatBox.innerHTML += `<div class="message ai-msg">${escapeHtml(data.code)}</div>`;
                } else {
                    chatBox.innerHTML += `<div class="message ai-msg" style="direction: rtl; color: #e74c3c;">هەڵە: ${escapeHtml(data.error || 'نەتوانرا وەڵام وەربگیرێت')}</div>`;
                }
                chatBox.scrollTop = chatBox.scrollHeight;

            } catch (error) {
                chatBox.innerHTML += `<div class="message ai-msg" style="direction: rtl; color: #e74c3c;">هەڵەیەک ڕوویدا لە پەیوەندیکردن بە سێرڤەرەکە.</div>`;
            }
        }

        function checkEnter(event) {
            if (event.key === 'Enter') {
                sendRequest();
            }
        }

        function escapeHtml(text) {
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }
    </script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')

        # داواکردنی کۆد لە زیرەکی دەستکردی گووگڵ
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"You are a professional Python programmer. Write clean and working Python code for this request: {user_prompt}. Provide only the code or clear explanations."
        )

        return jsonify({'code': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL_NAME = "google/gemini-2.5-flash"

SYSTEM_PROMPT = (
    "Você é um especialista em Segurança da Informação e Hacking Ético. "
    "Sua função é responder dúvidas sobre vulnerabilidades, boas práticas de defesa cibernética, "
    "criptografia e segurança de sistemas de forma técnica, porém didática. "
    "Se o usuário fizer perguntas fora do escopo de TI ou segurança, lembre-o educadamente de sua especialidade."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "Mensagem inválida"}), 400
        
    user_message = data["message"]
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        
        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data["choices"][0]["message"]["content"]
            return jsonify({"response": ai_response})
        else:
            return jsonify({"error": f"Erro na API: {response.status_code}"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("A variável de ambiente GEMINI_API_KEY não está definida.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/perguntar", methods=["GET"])
def perguntar():
    # Agora o prompt completo vem da Alexa
    prompt_completo = request.args.get("texto", "")

    if not prompt_completo:
        return jsonify({"erro": "Prompt ausente."}), 400

    try:
        response = model.generate_content(prompt_completo)
        resposta = response.text
        if not resposta:
            return jsonify({"erro": "Resposta vazia do modelo."}), 500
        return jsonify({"resposta": resposta.strip()})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

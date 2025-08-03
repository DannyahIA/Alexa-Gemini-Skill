from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir chamadas de qualquer origem (ou restrinja depois)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

@app.route("/perguntar", methods=["GET"])
def perguntar():
    pergunta = request.args.get("texto", "")

    if not pergunta:
        return jsonify({"erro": "Pergunta ausente."}), 400

    prompt = f"""
Você é uma assistente virtual brasileira chamada 'Assistente Inteligente'.
Responda de forma amigável, natural e concisa (2 a 3 frases), pois a resposta será falada por uma assistente de voz.
Pergunta: {pergunta}
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"resposta": response.text.strip()})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

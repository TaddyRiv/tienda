from flask import Blueprint, request, jsonify
import openai
import os

ai_routes = Blueprint('ai_routes', __name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@ai_routes.route('/interpretar-comando', methods=['POST', 'OPTIONS'])
def interpretar_comando():
    if request.method == "OPTIONS":
        # ✅ RESPONDE correctamente al preflight
        response = jsonify({"message": "OK"})
        response.status_code = 200
        return response

    data = request.json
    frase = data.get("frase", "")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asistente que interpreta frases de usuario para determinar qué producto desea agregar al carrito. Devuelve solo el nombre del producto."},
                {"role": "user", "content": f'Frase: "{frase}". ¿Qué producto quiere agregar?'}
            ]
        )
        producto = completion.choices[0].message["content"].strip()
        return jsonify({"producto": producto})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

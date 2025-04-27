from flask import Blueprint, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.database.db import db_session
from src.models.Models import Product

load_dotenv()

recom_bp = Blueprint("recom_bp", __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@recom_bp.route("/recomendar-productos", methods=["POST"])
def recomendar_productos():
    data = request.get_json()
    producto_id = data.get("producto_id")

    if not producto_id:
        return jsonify({"error": "Falta el producto_id"}), 400

    producto_base = db_session.query(Product).get(producto_id)
    if not producto_base:
        return jsonify({"error": "Producto no encontrado"}), 404

    productos = db_session.query(Product).filter(Product.id != producto_id).all()
    productos_lista = [
        f"{p.name}: {p.description or 'sin descripción'} ({p.price} Bs)"
        for p in productos
    ]
    prompt_lista = "\n".join(productos_lista)

    prompt = f"""
Actúas como un recomendador de productos en una tienda. Un cliente ha añadido este producto a su carrito: "{producto_base.name}".
Basándote en el siguiente listado de productos disponibles en tienda, sugiere 3 productos complementarios que podríamos ofrecer al cliente.

Productos disponibles:
{prompt_lista}

Devuélveme exclusivamente los nombres exactos de los 3 productos recomendados, separados por comas.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un sistema de recomendación experto en productos complementarios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=120
        )

        texto_respuesta = response.choices[0].message.content.strip()
        print("🧠 IA respondió:", texto_respuesta)  # 👀 para debug

        nombres_array = [n.strip() for n in texto_respuesta.split(",") if n.strip()]

        productos_recomendados = db_session.query(Product).filter(Product.name.in_(nombres_array)).all()

        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "stock": p.stock,
                "imagen": p.imagen
            }
            for p in productos_recomendados
        ])

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

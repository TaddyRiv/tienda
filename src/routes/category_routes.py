from flask import Blueprint, request, jsonify
from src.database.db import db_session
from src.models.Models import Category

category_bp = Blueprint("category_bp",__name__)

#listar categorias
@category_bp.route("/categories", methods=["GET"])
def get_categories():
    categorias = db_session.query(Category).all()
    return jsonify([
        {"id": c.id, "nombre": c.nombre, "descripcion": c.descripcion}
        for c in categorias
    ])

# Crear nueva categoría
@category_bp.route("/categories", methods=["POST"])
def create_category():
    data = request.json
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    if db_session.query(Category).filter_by(nombre=nombre).first():
        return jsonify({"error": "La categoría ya existe"}), 409

    categoria = Category(nombre=nombre, descripcion=descripcion)
    db_session.add(categoria)
    db_session.commit()

    return jsonify({"message": "Categoría creada", "id": categoria.id}), 201

# Editar categoría
@category_bp.route("/categories/<int:id>", methods=["PUT"])
def update_category(id):
    categoria = db_session.query(Category).get(id)
    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404

    data = request.json
    categoria.nombre = data.get("nombre", categoria.nombre)
    categoria.descripcion = data.get("descripcion", categoria.descripcion)

    db_session.commit()
    return jsonify({"message": "Categoría actualizada"}), 200

# Eliminar categoría
@category_bp.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):
    categoria = db_session.query(Category).get(id)
    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404

    db_session.delete(categoria)
    db_session.commit()
    return jsonify({"message": "Categoría eliminada"}), 200
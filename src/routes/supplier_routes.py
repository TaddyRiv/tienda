from flask import Blueprint, request, jsonify
from src.database.db import db_session
from src.models.Models import Supplier

supplier_bp = Blueprint("supplier_bp", __name__)

# Obtener todos los proveedores
@supplier_bp.route("/suppliers", methods=["GET"])
def get_suppliers():
    proveedores = db_session.query(Supplier).all()
    return jsonify([
        {
            "id": p.id,
            "nombre": p.nombre,
            "telephone": p.telephone,
            "direccion": p.direccion
        }
        for p in proveedores
    ])

# Crear proveedor
@supplier_bp.route("/suppliers", methods=["POST"])
def create_supplier():
    data = request.json
    nombre = data.get("nombre")
    telefono = data.get("telephone")
    direccion = data.get("direccion")

    if not all([nombre, telefono, direccion]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    proveedor = Supplier(nombre=nombre, telephone=telefono, direccion=direccion)
    db_session.add(proveedor)
    db_session.commit()

    return jsonify({"message": "Proveedor creado", "id": proveedor.id}), 201

# Actualizar proveedor
@supplier_bp.route("/suppliers/<int:id>", methods=["PUT"])
def update_supplier(id):
    proveedor = db_session.query(Supplier).get(id)
    if not proveedor:
        return jsonify({"error": "Proveedor no encontrado"}), 404

    data = request.json
    proveedor.nombre = data.get("nombre", proveedor.nombre)
    proveedor.telephone = data.get("telephone", proveedor.telephone)
    proveedor.direccion = data.get("direccion", proveedor.direccion)

    db_session.commit()
    return jsonify({"message": "Proveedor actualizado"}), 200

# Eliminar proveedor
@supplier_bp.route("/suppliers/<int:id>", methods=["DELETE"])
def delete_supplier(id):
    proveedor = db_session.query(Supplier).get(id)
    if not proveedor:
        return jsonify({"error": "Proveedor no encontrado"}), 404

    db_session.delete(proveedor)
    db_session.commit()
    return jsonify({"message": "Proveedor eliminado"}), 200

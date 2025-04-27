from flask import Blueprint, request, jsonify
from datetime import datetime
from src.database.db import db_session
from src.models.Models import Order, Sucursal

order_bp = Blueprint("order_bp", __name__)

@order_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    estado = data.get("estado", "pendiente")
    fecha = data.get("fecha") or datetime.now().strftime("%Y-%m-%d")
    monto = data.get("monto", 0.0)
    sucursal_id = data.get("sucursal_id")

    if not sucursal_id:
        return jsonify({"error": "La sucursal es obligatoria"}), 400

    sucursal = db_session.query(Sucursal).get(sucursal_id)
    if not sucursal:
        return jsonify({"error": "Sucursal no válida"}), 404

    orden = Order(
        estado=estado,
        fecha=fecha,
        monto=0.0,
        sucursal_id=sucursal_id
    )

    db_session.add(orden)
    db_session.commit()

    return jsonify({
        "message": "Orden creada",
        "id": orden.id,
        "estado": orden.estado,
        "fecha": orden.fecha
    }), 201


@order_bp.route("/orders", methods=["GET"])
def get_orders():
    ordenes = db_session.query(Order).all()
    return jsonify([
        {
            "id": o.id,
            "estado": o.estado,
            "fecha": o.fecha,
            "monto": o.monto,
            "sucursal_id": o.sucursal_id
        }
        for o in ordenes
    ])
#actualizar
@order_bp.route("/orders/<int:id>", methods=["PUT"])
def actualizar_estado_orden(id):
    orden = db_session.query(Order).get(id)
    if not orden:
        return jsonify({"error": "Orden no encontrada"}), 404

    data = request.json
    nuevo_estado = data.get("estado", "pendiente")
    orden.estado = nuevo_estado

    db_session.commit()
    return jsonify({"message": "Estado actualizado"}), 200

#modifica el stock
@order_bp.route("/api/orders/complete", methods=["POST"])
def complete_order():
    data = request.json
    carrito = data.get("carrito")  # Lista de productos con cantidad
    for item in carrito:
        product_id = item.get("product_id")
        quantity = item.get("cantidad")

        # Verificar stock
        product = db_session.query(product).get(product_id)
        if product.stock < quantity:
            return jsonify({"error": f"Producto {product.nombre} no tiene suficiente stock."}), 400
        
        # Descontar stock
        product.stock -= quantity
        db_session.commit()

    return jsonify({"message": "Compra realizada con éxito"}), 200



from flask import Blueprint, request, jsonify
from src.database.db import db_session
from src.models.Models import Order, Product, OrderDetail

order_detail_bp = Blueprint("order_detail_bp", __name__)

# Agregar un detalle a una orden
@order_detail_bp.route("/order-details", methods=["POST"])
def add_order_detail():
    data = request.json
    cantidad = data.get("cantidad")
    monto = data.get("monto")
    order_id = data.get("order_id")
    product_id = data.get("product_id")

    if not all([cantidad, monto, order_id, product_id]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    orden = db_session.query(Order).get(order_id)
    producto = db_session.query(Product).get(product_id)

    if not orden:
        return jsonify({"error": "Orden no encontrada"}), 404
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Crear detalle
    detalle = OrderDetail(
        cantidad=cantidad,
        monto=monto,
        order_id=order_id,
        product_id=product_id
    )

    db_session.add(detalle)

    # Sumar monto al total de la orden
    orden.monto += monto

    db_session.commit()

    return jsonify({"message": "Detalle agregado a la orden", "id": detalle.id}), 201

# Listar todos los detalles de orden
@order_detail_bp.route("/order-details", methods=["GET"])
def get_order_details():
    detalles = db_session.query(OrderDetail).all()
    return jsonify([
        {
            "id": d.id,
            "cantidad": d.cantidad,
            "monto": d.monto,
            "order_id": d.order_id,
            "product_id": d.product_id
        }
        for d in detalles
    ])

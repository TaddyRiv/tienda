from flask import Blueprint, request, jsonify
from datetime import datetime
from src.database.db import db_session
from src.models.Models import PurchaseNote, Product, Supplier, PaymentPay

purchase_bp = Blueprint("purchase_bp", __name__)

# Crear nota de compra
@purchase_bp.route("/purchase-notes", methods=["POST"])
def create_purchase_note():
    data = request.json
    cantidad = data.get("cantidad")
    fecha = data.get("fecha") or datetime.now().strftime("%Y-%m-%d")
    monto = data.get("monto")
    product_id = data.get("product_id")
    supplier_id = data.get("supplier_id")
    payment_pay_id = data.get("payment_pay_id")

    if not all([cantidad, monto, product_id, supplier_id, payment_pay_id]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # Validar relaciones
    producto = db_session.query(Product).get(product_id)
    proveedor = db_session.query(Supplier).get(supplier_id)
    metodo_pago = db_session.query(PaymentPay).get(payment_pay_id)

    if not producto:
        return jsonify({"error": "Producto no válido"}), 404
    if not proveedor:
        return jsonify({"error": "Proveedor no válido"}), 404
    if not metodo_pago:
        return jsonify({"error": "Método de pago no válido"}), 404

    # Crear nota de compra
    nota = PurchaseNote(
        cantidad=cantidad,
        fecha=fecha,
        monto=monto,
        product_id=product_id,
        supplier_id=supplier_id,
        payment_pay_id=payment_pay_id
    )

    db_session.add(nota)

    # Aumentar el stock del producto
    producto.stock += cantidad

    db_session.commit()

    return jsonify({"message": "Nota de compra registrada", "id": nota.id}), 201

# Obtener todas las notas de compra
@purchase_bp.route("/purchase-notes", methods=["GET"])
def get_purchase_notes():
    notas = db_session.query(PurchaseNote).all()
    return jsonify([
        {
            "id": n.id,
            "cantidad": n.cantidad,
            "fecha": n.fecha,
            "monto": n.monto,
            "product_id": n.product_id,
            "supplier_id": n.supplier_id,
            "payment_pay_id": n.payment_pay_id
        }
        for n in notas
    ])

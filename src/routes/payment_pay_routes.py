from flask import Blueprint, request, jsonify
from src.database.db import db_session
from src.models.Models import PaymentPay
from src.models.Models import SalesOrder
import stripe
import os
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payment_bp = Blueprint("payment_bp", __name__)

# Obtener todos los métodos de pago
@payment_bp.route("/payment-pays", methods=["GET"])
def get_payments():
    pagos = db_session.query(PaymentPay).all()
    return jsonify([
        {"id": p.id, "nombre": p.nombre}
        for p in pagos
    ])

# Crear un nuevo método de pago
@payment_bp.route("/payment-pays", methods=["POST"])
def create_payment():
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "El nombre del método de pago es obligatorio"}), 400

    if db_session.query(PaymentPay).filter_by(nombre=nombre).first():
        return jsonify({"error": "Este método de pago ya existe"}), 409

    metodo = PaymentPay(nombre=nombre)
    db_session.add(metodo)
    db_session.commit()

    return jsonify({"message": "Método de pago registrado", "id": metodo.id}), 201

# Eliminar método de pago (opcional, si no está en uso)
@payment_bp.route("/payment-pays/<int:id>", methods=["DELETE"])
def delete_payment(id):
    metodo = db_session.query(PaymentPay).get(id)
    if not metodo:
        return jsonify({"error": "Método de pago no encontrado"}), 404

    db_session.delete(metodo)
    db_session.commit()
    return jsonify({"message": "Método de pago eliminado"}), 200

@payment_bp.route('/sales-orders/<int:order_id>/add-payment', methods=['POST'])
def add_payment_to_order(order_id):
    try:
        db_session.rollback()  # Limpia estado previo si hubo error

        data = request.json
        payment_id = data.get("payment_id")

        if not isinstance(payment_id, int):
            return jsonify({"error": "payment_id debe ser un número"}), 400

        orden = db_session.query(SalesOrder).get(order_id)
        if not orden:
            return jsonify({"error": "Orden de venta no encontrada"}), 404

        metodo = db_session.query(PaymentPay).get(payment_id)
        if not metodo:
            return jsonify({"error": "Método de pago inválido"}), 404

        orden.payment_id = payment_id
        db_session.commit()

        return jsonify({"message": "Método de pago asignado correctamente"}), 200

    except Exception as e:
        db_session.rollback()
        print("❌ Error asignando método de pago:", e)
        return jsonify({"error": "Error interno del servidor"}), 500


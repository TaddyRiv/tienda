import stripe
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payment_intent_bp = Blueprint("payment_intent_bp", __name__)

@payment_intent_bp.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data.get("amount")
        
        if not amount:
            return jsonify({"error": "Amount requerido"}), 400

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            automatic_payment_methods={"enabled": True}
        )

        return jsonify({"clientSecret": intent.client_secret})
    except Exception as e:
        print("❌ Error en Stripe:", str(e))
        return jsonify({"error": str(e)}), 500

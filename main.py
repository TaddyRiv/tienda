import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
# Importar todas las rutas
from src.routes.user_routes import user_bp
from src.routes.AuthRoutes import auth_bp 
from src.routes.category_routes import category_bp
from src.routes.product_routes import product_bp
from src.routes.payment_pay_routes import payment_bp
from src.routes.supplier_routes import supplier_bp
from src.routes.purchase_note_routes import purchase_bp
from src.routes.order_routes import order_bp
from src.routes.order_detail_routes import order_detail_bp
from src.routes.sales_order_routes import sales_order_bp
from src.routes.recomendacion_routes import recom_bp
from src.routes.payment_intent_routes import payment_intent_bp
import stripe
stripe_key = os.getenv("STRIPE_SECRET_KEY")
if not stripe_key:
    raise ValueError("🚨 No se encontró STRIPE_SECRET_KEY en el entorno")
stripe.api_key = stripe_key


# === Crear app Flask ===
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": ["http://localhost:5173"]}})

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# === Registro de Blueprints ===
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(category_bp, url_prefix="/api")
app.register_blueprint(product_bp, url_prefix="/api")
app.register_blueprint(payment_bp, url_prefix="/api")
app.register_blueprint(supplier_bp, url_prefix="/api")
app.register_blueprint(purchase_bp, url_prefix="/api")
app.register_blueprint(order_bp, url_prefix="/api")
app.register_blueprint(order_detail_bp, url_prefix="/api")
app.register_blueprint(sales_order_bp, url_prefix="/api")
app.register_blueprint(recom_bp, url_prefix="/api")
app.register_blueprint(payment_intent_bp, url_prefix="/api")

@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

# === Ruta de prueba ===
@app.route("/")
def hola():
    return "<h1>¡Hola otra vez desde TiendaERP!</h1>"

# === Mostrar rutas registradas ===
print("📌 Rutas registradas:")
for rule in app.url_map.iter_rules():
    print(f"{rule.methods} → {rule.rule}")

# === Ejecutar App ===
if __name__ == "__main__":
    app.run(debug=True)

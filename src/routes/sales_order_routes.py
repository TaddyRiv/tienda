from flask import Blueprint, request, jsonify
from datetime import datetime
from src.database.db import db_session
from src.models.Models import SalesOrder, User, PaymentPay, Product, Order, OrderDetail

sales_order_bp = Blueprint("sales_order_bp", __name__)

# Crear orden de venta
@sales_order_bp.route("/sales-orders", methods=["POST"])
def create_sales_order():
    try:
        data = request.json
        total = data.get("total")
        user_id = data.get("user_id")
        tipo_entrega = data.get("tipo_entrega", "retiro")
        direccion_entrega = data.get("direccion_entrega", None)
        estado_entrega = data.get("estado_entrega", "alistando")
        fecha = data.get("fecha") or datetime.now().strftime("%Y-%m-%d")

        user = db_session.query(User).get(user_id)
        if not user:
            return jsonify({"error": "Usuario no válido"}), 404

        venta = SalesOrder(
            total=total,
            user_id=user_id,
            fecha=fecha,
            tipo_entrega=tipo_entrega,
            direccion_entrega=direccion_entrega,
            estado_entrega=estado_entrega
        )
        db_session.add(venta)
        db_session.commit()

        return jsonify({
            "message": "Venta registrada",
            "id": venta.id,
            "fecha": venta.fecha
        }), 201

    except Exception as e:
        print("❌ Error en create_sales_order:", e)
        return jsonify({"error": "Error interno al crear venta"}), 500


# Ver todas las órdenes de venta
@sales_order_bp.route("/sales-orders", methods=["GET"])
def get_sales_orders():
    ventas = db_session.query(SalesOrder).all()
    return jsonify([{
            "id": o.id,
            "fecha": o.fecha,
            "total": o.total,
            "user_id": o.user_id,
            "tipo_entrega": o.tipo_entrega,
            "direccion_entrega": o.direccion_entrega,
            "estado_entrega": o.estado_entrega
        } for o in ventas])


# Asociar método de pago
@sales_order_bp.route("/sales-orders/<int:id>/add-payment", methods=["POST"])
def add_payment_to_sale(id):
    data = request.json
    payment_id = data.get("payment_pay_id")

    if not payment_id:
        return jsonify({"error": "Falta el ID del método de pago"}), 400

    venta = db_session.query(SalesOrder).get(id)
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404  # Verifica que la venta exista
    metodo_pago = db_session.query(PaymentPay).get(payment_id)

    if not metodo_pago:
        return jsonify({"error": "Método de pago no válido"}), 404

    metodo_pago.sales_order_id = venta.id
    db_session.commit()

    return jsonify({"message": "Método de pago vinculado"}), 200

# Actualizar estado del pedido
@sales_order_bp.route("/sales-orders/<int:id>", methods=["PUT"])
def actualizar_estado_venta(id):
    venta = db_session.query(SalesOrder).get(id)
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404

    data = request.json
    nuevo_estado = data.get("estado_entrega")
    if nuevo_estado not in ["alistando pedido", "en camino", "ya llego"]:
        return jsonify({"error": "Estado no válido"}), 400

    venta.estado_entrega = nuevo_estado
    db_session.commit()

    return jsonify({"message": "Estado actualizado"}), 200

# Verificar stock de producto
@sales_order_bp.route("/products/<int:id>/check-stock", methods=["GET"])
def check_stock(id):
    product = db_session.query(Product).get(id)  # Asegúrate de consultar la clase Product
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({
        "stock_disponible": product.stock
    })

# Reducir stock cuando se agrega al carrito
@sales_order_bp.route("/products/<int:id>/reduce-stock", methods=["POST"])
def reduce_stock(id):
    product = db_session.query(Product).get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    # Aquí verificamos que haya stock suficiente
    if product.stock <= 0:
        return jsonify({"error": "No hay suficiente stock"}), 400

    # Reducimos el stock
    product.stock -= 1
    db_session.commit()

    return jsonify({"message": "Stock actualizado", "stock_disponible": product.stock}), 200

# Confirmación de compra y actualización de stock
@sales_order_bp.route("/sales-orders/<int:id>/finalizar-compra", methods=["POST"])
def finalizar_compra(id):
    venta = db_session.query(SalesOrder).get(id)
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404
    
    try:
        # Reducir stock de los productos involucrados
        for detalle in venta.detalles:  # 'detalles' es la relación entre OrderDetails y productos
            producto = db_session.query(Product).get(detalle.product_id)
            
            if producto:
                if producto.stock >= detalle.cantidad:  # Verificar si hay suficiente stock
                    producto.stock -= detalle.cantidad  # Reducir el stock
                    db_session.commit()
                else:
                    return jsonify({"error": f"No hay suficiente stock para {producto.name}"}), 400
        
        # Aquí podrías agregar más lógica si es necesario (como marcar la venta como finalizada o enviada)

        return jsonify({"message": "Compra finalizada y stock actualizado"}), 200

    except Exception as e:
        print(f"Error al finalizar compra: {e}")
        return jsonify({"error": "Error interno al actualizar stock"}), 500


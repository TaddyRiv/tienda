# src/routes/admin_order.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from src.database.db import db_session
from src.models.Models import Order, OrderDetail, Product, SalesOrder, User, Sucursal

admin_order_bp = Blueprint("admin_order_bp", __name__)

@admin_order_bp.route("/admin/crear-orden-completa", methods=["POST"])
def crear_orden_completa():
    try:
        data = request.json

        cliente_id = data.get("cliente_id")
        productos = data.get("productos")  # [{ id: , cantidad: }]
        tipo_envio = data.get("tipo_envio", "retiro")
        direccion = data.get("direccion", None)
        metodo_pago_id = data.get("payment_pay_id", None)
        sucursal_id = data.get("sucursal_id", 1)  # puedes poner default si quieres
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        if not cliente_id or not productos:
            return jsonify({"error": "Faltan datos esenciales."}), 400

        # 1. Crear una Orden
        nueva_orden = Order(
            estado="pendiente",
            fecha=fecha_actual,
            monto=0.0,
            sucursal_id=sucursal_id
        )
        db_session.add(nueva_orden)
        db_session.commit()

        monto_total = 0.0

        # 2. Agregar los productos a la orden (OrderDetail)
        for item in productos:
            producto = db_session.query(Product).get(item["id"])
            if not producto:
                return jsonify({"error": f"Producto con id {item['id']} no encontrado"}), 404

            cantidad = item["cantidad"]
            monto = producto.price * cantidad
            monto_total += monto

            detalle = OrderDetail(
                cantidad=cantidad,
                monto=monto,
                order_id=nueva_orden.id,
                product_id=producto.id
            )
            db_session.add(detalle)

        # 3. Actualizar monto total de la orden
        nueva_orden.monto = monto_total
        db_session.commit()

        # 4. Crear la Nota de Venta (SalesOrder)
        nueva_venta = SalesOrder(
            total=monto_total,
            user_id=cliente_id,
            fecha=fecha_actual,
            tipo_entrega=tipo_envio,
            direccion_entrega=direccion,
            estado_entrega="alistando pedido"
        )
        db_session.add(nueva_venta)
        db_session.commit()

        # 5. Asociar método de pago (si se envió)
        if metodo_pago_id:
            from src.models.Models import PaymentPay  # Asegúrate que esté importado
            metodo_pago = db_session.query(PaymentPay).get(metodo_pago_id)
            if metodo_pago:
                metodo_pago.sales_order_id = nueva_venta.id
                db_session.commit()

        return jsonify({
            "message": "Orden y venta creadas correctamente",
            "order_id": nueva_orden.id,
            "sales_order_id": nueva_venta.id
        }), 201

    except Exception as e:
        print(f"Error en crear_orden_completa: {e}")
        db_session.rollback()
        return jsonify({"error": "Error interno al crear orden completa"}), 500

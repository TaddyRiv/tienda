from flask import Blueprint, request, jsonify
from src.database.db import db_session
from src.models.Models import Product, Category

product_bp = Blueprint("producto_bp", __name__)

# 🔍 Obtener todos los productos
@product_bp.route("/products", methods=["GET"])
def get_products():
    productos = db_session.query(Product).all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "category_id": p.category_id,
            "imagen": p.imagen  # ✅ Se incluye el campo imagen
        }
        for p in productos
    ])

# ➕ Crear producto
@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock", 0)
    category_id = data.get("category_id")
    imagen = data.get("imagen")  # ✅ campo imagen

    if not all([name, price, category_id]):
        return jsonify({"error": "Nombre, precio y categoría son obligatorios"}), 400

    if db_session.query(Category).get(category_id) is None:
        return jsonify({"error": "Categoría no válida"}), 404

    producto = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
        imagen=imagen  # ✅ se guarda
    )

    db_session.add(producto)
    db_session.commit()
    return jsonify({"message": "Producto creado", "id": producto.id}), 201

# ✏️ Actualizar producto
@product_bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    producto = db_session.query(Product).get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.json
    producto.name = data.get("name", producto.name)
    producto.description = data.get("description", producto.description)
    producto.price = data.get("price", producto.price)
    producto.stock = data.get("stock", producto.stock)
    producto.imagen = data.get("imagen", producto.imagen)  # ✅ actualizar imagen
    categoria = data.get("category_id", producto.category_id)

    if db_session.query(Category).get(categoria) is None:
        return jsonify({"error": "Categoría no válida"}), 404

    producto.category_id = categoria
    db_session.commit()
    return jsonify({"message": "Producto actualizado"}), 200

# 🗑️ Eliminar producto
@product_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    producto = db_session.query(Product).get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    db_session.delete(producto)
    db_session.commit()
    return jsonify({"message": "Producto eliminado"}), 200

# Verificar si hay stock suficiente
@product_bp.route("/products/<int:id>/check-stock", methods=["GET"])
def check_stock(id):
    product = db_session.query(Product).get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    stock_disponible = product.stock
    return jsonify({"stock_disponible": stock_disponible}), 200

# Reducir stock cuando el producto es agregado al carrito
@product_bp.route("/products/<int:id>/reduce-stock", methods=["POST"])
def reduce_stock(id):
    product = db_session.query(Product).get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    # Verificar que haya stock suficiente
    if product.stock <= 0:
        return jsonify({"error": "No hay suficiente stock"}), 400

    # Reducir el stock
    product.stock -= 1
    db_session.commit()

    return jsonify({"message": "Stock actualizado", "stock_disponible": product.stock}), 200

#  Endpoint SEGURO para reducir stock según la cantidad comprada
@product_bp.route("/products/<int:id>/update-stock", methods=["PUT"])
def update_stock(id):
    product = db_session.query(Product).get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.json
    cantidad = data.get("cantidad")

    if not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({"error": "Cantidad inválida"}), 400

    if product.stock < cantidad:
        return jsonify({"error": "Stock insuficiente"}), 400

    product.stock -= cantidad
    db_session.commit()

    return jsonify({"message": "Stock actualizado", "stock": product.stock}), 200


    # 🔍 Buscar varios productos por nombre (para recomendaciones IA)
@product_bp.route("/products/by-name/<string:nombre>", methods=["GET"])
def get_products_by_name(nombre):
    productos = db_session.query(Product).filter(
        Product.name.ilike(f"%{nombre}%")
    ).all()

    if not productos:
        return jsonify({"error": "No se encontraron productos similares"}), 404

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "imagen": p.imagen
        }
        for p in productos
    ])

#  Nuevo endpoint para lista simple de productos
@product_bp.route("/products/list", methods=["GET"])
def get_products_list():
    productos = db_session.query(Product).all()

    lista_productos = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in productos
    ]

    return jsonify(lista_productos), 200

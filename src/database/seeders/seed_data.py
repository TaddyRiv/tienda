from faker import Faker
import random
from werkzeug.security import generate_password_hash

fake = Faker()

# Generar datos de ejemplo
users = []
for _ in range(10):
    users.append({
        "username": fake.user_name(),
        "telephone": fake.phone_number(),
        "correo": fake.unique.email(),
        "password": generate_password_hash("123456"),
        "rol_id": random.choice([1, 3]),
        "sucursal_id": random.choice([1, 2])
    })

categories = []
for i in range(5):
    categories.append({
        "nombre": fake.word().capitalize(),
        "descripcion": fake.sentence(),
        "parent_id": None if i % 2 == 0 else random.randint(1, i)
    })

products = []
for _ in range(20):
    products.append({
        "name": fake.word().capitalize(),
        "description": fake.sentence(),
        "price": round(random.uniform(10, 200), 2),
        "stock": random.randint(5, 100),
        "imagen": fake.image_url(),
        "category_id": random.randint(1, 5)
    })

sucursales = [
    {"nombre": "Sucursal Central", "direccion": "Av. Principal #123"},
    {"nombre": "Sucursal Norte", "direccion": "Calle 10 #456"}
]

orders = []
for i in range(10):
    orders.append({
        "estado": "pendiente",
        "fecha": fake.date(),
        "monto": round(random.uniform(100, 500), 2),
        "sucursal_id": random.randint(1, 2)
    })

sales_orders = []
for i in range(10):
    sales_orders.append({
        "fecha": fake.date(),
        "total": round(random.uniform(100, 500), 2),
        "estado_entrega": "alistando",
        "tipo_entrega": "tienda",
        "direccion_entrega": None,
        "user_id": random.randint(1, 10),
        "payment_id": random.randint(1, 3)
    })

order_details = []
for i in range(20):
    order_details.append({
        "cantidad": random.randint(1, 5),
        "monto": round(random.uniform(10, 100), 2),
        "order_id": random.randint(1, 10),
        "product_id": random.randint(1, 20)
    })

import pandas as pd
import os
from pathlib import Path
import json

output_path = Path("/mnt/data/seed_data.py")

seed_code = f"""
from src.database.db import db_session
from src.models.Models import User, Product, Category, Order, SalesOrder, OrderDetail, Sucursal
from werkzeug.security import generate_password_hash

# Crear sucursales
sucursales = {sucursales}
for data in sucursales:
    db_session.add(Sucursal(**data))

# Crear categorías
categorias = {categories}
for data in categorias:
    db_session.add(Category(**data))

# Crear productos
productos = {products}
for data in productos:
    db_session.add(Product(**data))

# Crear usuarios
usuarios = {users}
for data in usuarios:
    db_session.add(User(**data))

# Crear órdenes
ordenes = {orders}
for data in ordenes:
    db_session.add(Order(**data))

# Crear ventas
ventas = {sales_orders}
for data in ventas:
    db_session.add(SalesOrder(**data))

# Crear detalles de orden
detalles = {order_details}
for data in detalles:
    db_session.add(OrderDetail(**data))

db_session.commit()
print("✅ Datos insertados correctamente.")
"""

with open(output_path, "w") as f:
    f.write(seed_code)

output_path.name

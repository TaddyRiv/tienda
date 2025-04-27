from src.database.db import db_session
from src.models.Models import User, Product, Category, Order, OrderDetail, SalesOrder
from werkzeug.security import generate_password_hash
from datetime import datetime

# ✅ Verificación para evitar duplicados
def safe_add(instance, model, unique_field, value):
    exists = db_session.query(model).filter(getattr(model, unique_field) == value).first()
    if not exists:
        db_session.add(instance)
        db_session.commit()

# Crear categorías
cat1 = Category(nombre="Electrónica", descripcion="Dispositivos y gadgets")
cat2 = Category(nombre="Hogar", descripcion="Artículos para el hogar")
safe_add(cat1, Category, "nombre", cat1.nombre)
safe_add(cat2, Category, "nombre", cat2.nombre)

# Crear productos
productos = [
    Product(name="Laptop Lenovo", description="15 pulgadas, 8GB RAM", price=4500, stock=10, category_id=cat1.id),
    Product(name="Mouse inalámbrico", description="USB, ergonómico", price=120, stock=50, category_id=cat1.id),
    Product(name="Aspiradora Robot", description="Automática", price=900, stock=15, category_id=cat2.id),
    Product(name="Cafetera", description="12 tazas, programable", price=300, stock=20, category_id=cat2.id),
]
for p in productos:
    safe_add(p, Product, "name", p.name)

# Crear usuario (cliente)
usuario = User(username="juanito", correo="juan@example.com", telephone="78945612", rol_id=3)
usuario.password = "123456"
safe_add(usuario, User, "username", usuario.username)

# Crear orden y detalles
orden = Order(estado="pendiente", fecha=str(datetime.now().date()), monto=5400, sucursal_id=1)
db_session.add(orden)
db_session.commit()

detalles = [
    OrderDetail(order_id=orden.id, product_id=productos[0].id, cantidad=1, monto=4500),
    OrderDetail(order_id=orden.id, product_id=productos[1].id, cantidad=1, monto=900),
]
db_session.bulk_save_objects(detalles)
db_session.commit()

# Crear orden de venta
venta = SalesOrder(
    fecha=str(datetime.now().date()),
    total=5400,
    user_id=usuario.id,
    tipo_entrega="tienda",
    estado_entrega="alistando"
)
db_session.add(venta)
db_session.commit()

print("✅ Datos insertados correctamente.")

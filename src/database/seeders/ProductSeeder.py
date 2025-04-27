from src.database.db import SessionLocal
from src.models.Models import Product

def run():
    db = SessionLocal()

    if db.query(Product).first():
        print("Productos ya insertados.")
        db.close()
        return

    productos = [
        Product(name="Laptop HP", description="i5 8GB RAM", price=1200, stock=5),
        Product(name="Mouse Logitech", description="Ergonómico", price=30, stock=20)
    ]

    db.add_all(productos)
    db.commit()
    db.close()
    print("Productos insertados correctamente.")

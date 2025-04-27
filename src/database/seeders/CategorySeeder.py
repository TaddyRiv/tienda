from src.database.db import SessionLocal
from src.models.Models import Category

def run():
    db = SessionLocal()

    if db.query(Category).first():
        print("Categorías ya insertadas.")
        db.close()
        return

    # Categoría principal
    tecnologia = Category(nombre="Tecnología", descripcion="Todo lo relacionado con tecnología")

    # Subcategoría (recursiva)
    laptops = Category(nombre="Laptops", descripcion="Portátiles y notebooks", parent=tecnologia)

    db.add_all([tecnologia, laptops])
    db.commit()
    db.close()
    print("Categorías insertadas correctamente.")

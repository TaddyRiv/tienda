from src.database.db import SessionLocal
from src.models.Models import Sucursal

def run():
    db = SessionLocal()
    if db.query(Sucursal).first():
        print("Sucursal ya insertada.")
        db.close()
        return

    sucursales = [
        Sucursal(nombre="Sucursal Central", direccion="Plaza 14 Septiembre"),
        Sucursal(nombre="Sucursal Sur", direccion="Plan 3000, Av. cheguevara"),
        Sucursal(nombre="Sucursal Norte", direccion="Las brisas")
    ]

    db.add_all(sucursales)
    db.commit()
    db.close()
    print("Sucursales insertadas correctamente.")

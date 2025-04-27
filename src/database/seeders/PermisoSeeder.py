from src.database.db import SessionLocal
from src.models.Models import Permiso

def run():
    db = SessionLocal()

    if db.query(Permiso).first():
        print("Permisos ya insertados.")
        db.close()
        return

    permisos = [
        Permiso(nombre="crear"),
        Permiso(nombre="editar"),
        Permiso(nombre="eliminar"),
        Permiso(nombre="ver")
    ]

    db.add_all(permisos)
    db.commit()
    db.close()
    print("Permisos insertados correctamente.")

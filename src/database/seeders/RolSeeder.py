from src.database.db import SessionLocal
from src.models.Models import Rol

def run():
    db = SessionLocal()
    if db.query(Rol).first():
        print("Roles ya insertados.")
        db.close()
        return

    roles = [
        Rol(nombre="admin"),
        Rol(nombre="empleado"),
        Rol(nombre="cliente")
    ]
    db.add_all(roles)
    db.commit()
    db.close()
    print("Roles insertados correctamente.")

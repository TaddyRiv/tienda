from src.database.db import SessionLocal
from src.models.Models import Rol, Permiso, RolPermisos

def run():
    db = SessionLocal()
    if db.query(RolPermisos).first():
        print("Relaciones rol-permiso ya insertadas.")
        db.close()
        return

    admin = db.query(Rol).filter_by(nombre="admin").first()
    empleado = db.query(Rol).filter_by(nombre="empleado").first()

    permisos = db.query(Permiso).all()

    relaciones = []

    # Admin tiene todos los permisos
    for permiso in permisos:
        relaciones.append(RolPermisos(rol_id=admin.id, permiso_id=permiso.id))

    # Empleado solo puede ver y editar
    for permiso in permisos:
        if permiso.nombre in ["ver", "editar"]:
            relaciones.append(RolPermisos(rol_id=empleado.id, permiso_id=permiso.id))

    db.add_all(relaciones)
    db.commit()
    db.close()
    print("Permisos asignados a roles correctamente.")

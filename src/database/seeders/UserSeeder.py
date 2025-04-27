from src.database.db import SessionLocal
from src.models.Models import User, Rol, Sucursal

def run():
    db = SessionLocal()

    print("🚀 Ejecutando UserSeeder...")

    sucursal = db.query(Sucursal).filter_by(nombre="Sucursal Central").first()
    if not sucursal:
        sucursal = Sucursal(nombre="Sucursal Central", direccion="Av. Principal 123")
        db.add(sucursal)
        db.commit()
        db.refresh(sucursal)

    admin_rol = db.query(Rol).filter_by(nombre="admin").first()
    if not admin_rol:
        print("❌ Rol 'admin' no encontrado. Seeder interrumpido.")
        db.close()
        return

    user = User(
        username="admin",
        telephone="77777777",
        correo="admin@gmail.com",
        password="123456",  # ✅ Usa el setter para hashear automáticamente
        rol_id=admin_rol.id,
        sucursal_id=sucursal.id
    )

    db.add(user)
    db.commit()
    db.close()

    print("✅ Usuario admin insertado correctamente.")

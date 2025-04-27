from src.database.db import Base, engine
from src.database.seeders import RolSeeder, UserSeeder, SucursalSeeder, PermisoSeeder

def run_all():
    print("📦 Creando las tablas si no existen...")
    Base.metadata.create_all(bind=engine)

    print("🚀 Ejecutando seeders...")
    RolSeeder.run()
    PermisoSeeder.run()
    SucursalSeeder.run()
    UserSeeder.run()

if __name__ == "__main__":
    run_all()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Puedes cambiar esta URL según la base que usarás
DATABASE_URL = "postgresql://postgres:tuputamadre@localhost:5432/tiendaerp"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

db_session = SessionLocal()
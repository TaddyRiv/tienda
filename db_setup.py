from src.database.db import engine
from src.models import Models  # Asegúrate que Models importa todas tus clases

Models.Base.metadata.create_all(bind=engine)

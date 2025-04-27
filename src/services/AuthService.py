import jwt
from datetime import datetime, timedelta
from flask_bcrypt import check_password_hash
from src.database.db import db_session
from src.models.Models import User

SECRET_KEY = "clave-secreta-tiendarp"  # Puedes mover esto a un .env luego

def authenticate_user(username, password):
    user = db_session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # Generar token JWT
        token = jwt.encode({
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=4)
        }, SECRET_KEY, algorithm="HS256")
        return token, user
    return None, None

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = db_session.query(User).get(payload["id"])
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

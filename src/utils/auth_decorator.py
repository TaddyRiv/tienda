from functools import wraps
from flask import request, jsonify
from src.services.AuthService import verify_token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token no proporcionado"}), 401

        token = auth_header.split(" ")[1]
        user = verify_token(token)
        if not user:
            return jsonify({"error": "Token inválido o expirado"}), 401

        request.user = user
        return f(*args, **kwargs)
    return decorated

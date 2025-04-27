import traceback
from flask import Blueprint, request, jsonify
from src.database.db import db_session
from src.models.Models import User, Rol
import jwt, datetime
from werkzeug.security import check_password_hash


auth_bp = Blueprint("auth_bp", __name__)
SECRET_KEY = "supersecreto"

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400

        user = db_session.query(User).filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Credenciales inválidas"}), 401

        token = jwt.encode({
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, "supersecreto", algorithm="HS256")

        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "rol_id": user.rol_id,
                "sucursal_id": user.sucursal_id
            }
        }), 200

    except Exception as e:
        db_session.rollback()
        print("🔴 Error en login:", str(e))
        traceback.print_exc()  # 👈 Esto muestra el error real
        return jsonify({"error": "Error interno en el servidor"}), 500
    
    #register
    
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    correo = data.get("correo")
    telephone = data.get("telephone")

    if not all([username, password, correo, telephone]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if db_session.query(User).filter_by(username=username).first():
        return jsonify({"error": "El nombre de usuario ya existe"}), 409

    if db_session.query(User).filter_by(correo=correo).first():
        return jsonify({"error": "El correo ya está en uso"}), 409

    # Asignar rol cliente (ID 3 o buscar por nombre)
    cliente_rol = db_session.query(Rol).filter_by(nombre="cliente").first()
    if not cliente_rol:
        return jsonify({"error": "Rol 'cliente' no encontrado"}), 500

    nuevo_user = User(
        username=username,
        password=password,  # Se hashea automáticamente
        correo=correo,
        telephone=telephone,
        rol_id=cliente_rol.id,
        sucursal_id=None  # Por ahora los clientes no necesitan sucursal
    )

    db_session.add(nuevo_user)
    db_session.commit()

    return jsonify({"message": "Registro exitoso", "id": nuevo_user.id}), 201
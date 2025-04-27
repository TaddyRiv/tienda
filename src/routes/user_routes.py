from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from src.database.db import db_session
from src.models.Models import User, Rol, Sucursal
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("user_bp", __name__)

# 🧾 Obtener todos los usuarios
@user_bp.route("/users", methods=["GET"])
def get_users():
    usuarios = db_session.query(User).all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "correo": u.correo,
            "telephone": u.telephone,
            "rol_id": u.rol_id,
            "sucursal_id": u.sucursal_id
        }
        for u in usuarios
    ])

# ➕ Crear nuevo usuario
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    correo = data.get("correo")
    password = data.get("password")
    telephone = data.get("telephone")
    rol_id = data.get("rol_id") or 3  # Suponiendo 3 = cliente por defecto
    sucursal_id = data.get("sucursal_id")  # Opcional para clientes

    if not all([username, correo, password, telephone]):
        return jsonify({"error": "Todos los campos obligatorios deben estar presentes"}), 400

    if db_session.query(User).filter_by(username=username).first():
        return jsonify({"error": "El nombre de usuario ya existe"}), 409

    if db_session.query(User).filter_by(correo=correo).first():
        return jsonify({"error": "El correo ya está en uso"}), 409

    user = User(
        username=username,
        correo=correo,
        telephone=telephone,
        password=password,  # Se hashea automáticamente si el modelo lo tiene configurado así
        rol_id=rol_id,
        sucursal_id=sucursal_id
    )

    db_session.add(user)
    db_session.commit()

    return jsonify({"message": "Usuario registrado con éxito", "id": user.id}), 201

# ✏️ Actualizar usuario
@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = db_session.query(User).get(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.json
    user.username = data.get("username", user.username)
    user.correo = data.get("correo", user.correo)
    user.telephone = data.get("telephone", user.telephone)

    db_session.commit()
    return jsonify({"message": "Usuario actualizado correctamente"}), 200

# 🗑️ Eliminar usuario
@user_bp.route("/users/<int:id>", methods=["DELETE", "OPTIONS"])
def delete_user(id):
    if request.method == "OPTIONS":
        # 🔁 Responder manualmente al preflight
        return jsonify({"message": "Preflight ok"}), 200

    print(f"🔴 Recibido DELETE para usuario {id}")
    user = db_session.query(User).get(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db_session.delete(user)
    db_session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200

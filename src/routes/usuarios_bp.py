from flask import Blueprint, request, jsonify, g
from functools import wraps
from src.crud.usuarios_crud import usuarios_crud
from src.utils.auth import auth_function, verify_token #tenle un ojo a esta parte. Verify esta dentro de auth pero no la detecta sin especificar

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return jsonify({"error": "Token faltante"}), 401
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Formato de header Authorization inválido"}), 401
        token = parts[1]
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401
        # pasamos payload como primer argumento de la función protegida
        g.user_payload = payload
        g.user_id = payload.get("sub")
        return f(*args, **kwargs)
    return decorated

@usuarios_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    clave = data.get("clave")
    if not email or not clave:
        return jsonify({"error": "Email y clave son obligatorios"}), 400

    token = auth_function().login(email, clave)
    token = auth_function().login(data["email"], data["clave"])

    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@usuarios_bp.route("/crear", methods=["POST"])
def crear_usuario():
    data = request.get_json() or {}
    campos = ["nombres", "apellidos", "edad", "telefono", "email", "clave", "ciudad", "pais"]
    valores = [data.get(c) for c in campos]
    crud = usuarios_crud()
    new_id = crud.create_user(*valores)
    
    if new_id:
        return jsonify({"id": new_id}), 201
    return jsonify({"error": "No se pudo crear usuario"}), 400

@usuarios_bp.route("/listar", methods=["GET"])
@token_required
def listar_usuarios():
    crud = usuarios_crud()
    usuarios = crud.read_users()
    return jsonify(usuarios), 200


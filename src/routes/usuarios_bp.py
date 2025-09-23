from flask import Blueprint, request, jsonify
from functools import wraps
from src.functions.CRUD import CRUD_function
from src.functions.auth import auth_function, verify_token #tenle un ojo a esta parte. Verify esta dentro de auth pero no la detecta sin especificar

usuarios_bp = Blueprint("usuarios", __name__)

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
        return f(payload, *args, **kwargs)
    return decorated

@usuarios_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()  # recibe { "email": "...", "clave": "..." }

    if not data or not data.get("email") or not data.get("clave"):
        return jsonify({"error": "Email y clave son obligatorios"}), 400

    token = auth_function().login(data["email"], data["clave"])

    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@usuarios_bp.route("/crear", methods=["POST"])
def crear_usuario():
    data = request.get_json()
    crud = CRUD_function()
    campos = ["nombres", "apellidos", "edad", "telefono", "email", "clave", "ciudad", "pais"]
    valores = [data.get(c) for c in campos]
    new_id = crud.create_user(*valores)
    
    if new_id:
        return jsonify({"id": new_id}), 201
    return jsonify({"error": "No se pudo crear usuario"}), 400

@usuarios_bp.route("/listar", methods=["GET"])
@token_required
def listar_usuarios():
    crud = CRUD_function()
    usuarios = crud.read_users()
    return jsonify(usuarios), 200


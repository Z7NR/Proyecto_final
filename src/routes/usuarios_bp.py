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

"""@usuarios_bp.route("/actualizar", methods=["UPDATE"])    
def update():
    data = request.get_json()

"""
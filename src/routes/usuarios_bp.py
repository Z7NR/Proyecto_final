from flask import Blueprint, request, jsonify, g
from functools import wraps
from src.crud.usuarios_crud import user_crud
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
    crud = user_crud()
    new_id = crud.create_user(*valores)
    
    if new_id:
        return jsonify({"id": new_id}), 201
    return jsonify({"error": "No se pudo crear usuario"}), 400

@usuarios_bp.route("/listar", methods=["GET"])
@token_required
def listar_usuarios():
    crud = user_crud()
    usuarios = crud.read_user()
    return jsonify(usuarios), 200

@usuarios_bp.route("/<int:id>", methods=["GET"])
@token_required
def filtrar_usuario_id(id):
    crud =user_crud()
    id_user = crud.read_id_user(id)
    if id_user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    try:
        import sqlite3
        if isinstance(id_user, sqlite3.Row): 
            id_user = dict(id_user)
    except Exception:
        pass

    return jsonify(id_user), 200

@usuarios_bp.route("/perfil", methods=["GET"])
@token_required
def obtener_perfil():
    user_id = getattr(g, "user_id", None)
    if user_id is None:
        return jsonify({"error": "Token válido pero user_id faltante"}), 401

    crud = user_crud()
    usuario = crud.read_id_user(int(user_id))
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
        import sqlite3
        if isinstance(usuario, sqlite3.Row):
            usuario = dict(usuario)
    except Exception:
        pass

    return jsonify(usuario), 200

@usuarios_bp.route("/email", methods=["GET"])
@token_required
def obtener_user_email():
    email = getattr(g, "email_id", None)
    if email is None:
        return jsonify({"error": "Token válido pero user_id faltante"}), 401

    crud = user_crud()
    usuario = crud.read_by_email(email)
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
        import sqlite3
        if isinstance(usuario, sqlite3.Row):
            usuario = dict(usuario)
    except Exception:
        pass

    usuario.pop("clave_hash", None)
    usuario.pop("clave", None)

    return jsonify(usuario), 200

@usuarios_bp.route("/ciudad/<ciudad>", methods=["GET"])
@token_required
def filtrar_por_ciudad(ciudad):
    crud = user_crud()
    usuarios = crud.read_by_city(ciudad)

    if not usuarios:
        return jsonify({"mensaje": "No hay usuarios en esa ciudad"}), 404

    return jsonify([dict(u) for u in usuarios]), 200

@usuarios_bp.route("/pais/<pais>", methods=["GET"])
@token_required
def filtrar_por_pais(pais):
    crud = user_crud()
    usuarios = crud.read_by_country(pais)
    
    if not usuarios:
        return jsonify({"mensaje": "No hay usuarios en ese país"}), 404

    return jsonify([dict(u) for u in usuarios]), 200

@usuarios_bp.route("/edad", methods=["GET"])
@token_required
def filtrar_por_edad():
    min_age = request.args.get("min")
    max_age = request.args.get("max")

    if not min_age or not max_age:
        return jsonify({"error": "Debe incluir parámetros min y max"}), 400

    try:
        min_age = int(min_age)
        max_age = int(max_age)
    except ValueError:
        return jsonify({"error": "min y max deben ser números enteros"}), 400

    crud = user_crud()
    usuarios = crud.read_by_age_range(min_age, max_age)

    if not usuarios:
        return jsonify({"mensaje": "No se encontraron usuarios en ese rango"}), 404

    return jsonify([dict(u) for u in usuarios]), 200

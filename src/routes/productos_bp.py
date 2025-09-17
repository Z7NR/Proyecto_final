from flask import Blueprint, request, jsonify
from src.functions.CRUD import CRUD_function

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/crear", methods=["POST"])
def crear_producto():
    data = request.get_json()
    db = CRUD_function()
    db.create_product(data["nombre"], data["descripcion"], data["categoria"], data["stock"])
    return jsonify({"mensaje": "Producto creado con éxito"}), 201

@productos_bp.route("/listar", methods=["GET"])
def listar_productos():
    db = CRUD_function()
    productos = db.read.products()
    return jsonify(productos), 200

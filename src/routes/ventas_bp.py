from flask import Blueprint, jsonify, request
from src.functions.CRUD import CRUD_function

ventas_bp = Blueprint("ventas", __name__)

@ventas_bp.route("/crear", methods=["POST"])
def crear_venta():
    data = request.get_json()
    db = CRUD_function()
    db.create_sale(data["id_usuario"], data["id_producto"], data["cantidad"])
    return jsonify({"mensaje": "Venta registrada con éxito"}), 201

@ventas_bp.route("/listar", methods=["GET"])
def listar_ventas():
    db = CRUD_function()
    ventas = db.read_sales()
    return jsonify(ventas), 200
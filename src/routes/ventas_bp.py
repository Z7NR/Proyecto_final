from flask import Blueprint, jsonify, request
from src.crud.usuarios_crud import ventas_crud
from src.routes.usuarios_bp import token_required

ventas_bp = Blueprint("ventas", __name__, url_prefix="/api/ventas")

@ventas_bp.route("/crear", methods=["POST"])
@token_required
def crear_venta():
    data = request.get_json() or {}
    if not data.get("id_usuario") or not data.get("id_producto"):
        return jsonify({"error":"id_usuario e id_producto son requeridos"}), 400
    
    cantidad_raw = data.get("cantidad", 1)
    try:
        cantidad= int(cantidad_raw)
        if cantidad <=0:
            return jsonify({"error":"cantidad debe ser entero positivo"}, 400)
    except Exception:
        return jsonify ({"error": "cantidad tiene formato inválido"}), 400
    
    id_usuario = data.get("id_usuario")
    id_producto = data.get("id_producto")

    db = ventas_crud()
    try:
        res = db.create_sale(id_usuario, id_producto, cantidad)
        if res is None:
            return jsonify({"error":"Error internos al crear venta"}), 500
        if isinstance(res, dict) and res.get("error"):
            return jsonify(res), 400
    #db.create_sale(data["id_usuario"], data["id_producto"], data["cantidad"])
    #return jsonify({"mensaje": "Venta registrada con éxito"}), 201
        return jsonify(res), 201
    except Exception as e:
        print(f"Error en crear_venta: {e}")
        return jsonify({"error": "Error interno"}), 500
@ventas_bp.route("/listar", methods=["GET"])

def listar_ventas():
    db = ventas_crud()
    ventas = db.read_sales()
    return jsonify(ventas), 200
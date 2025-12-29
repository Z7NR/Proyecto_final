from flask import Blueprint, request, jsonify, send_file
from src.crud.ventas_crud import ventas_crud
from src.routes.usuarios_bp import token_required
from openpyxl import Workbook
from src.crud.ventas_crud import ventas_crud
import tempfile

ventas_bp = Blueprint("ventas", __name__, url_prefix="/api/ventas")

from flask import request, jsonify, g 

@ventas_bp.route("", methods=["POST"])
@token_required
def registrar_venta():
    data = request.get_json() or {}
    required = ["id_producto", "cantidad"]
    
    if not all(k in data for k in required):
        return jsonify({"error": "Datos incompletos"}), 400

    id_usuario = int(g.user_id) 

    crud = ventas_crud()
    result = crud.create_venta(
        id_usuario,
        data["id_producto"],
        data["cantidad"]
    )

    if isinstance(result, dict):
        print(f"DEBUG FAIL: {result}") 
        return jsonify(result), 400

    return jsonify({"id": result}), 201

@ventas_bp.route("/listar", methods=["GET"])
@token_required
def listar_ventas():
    return jsonify(ventas_crud().read_all()), 200

@ventas_bp.route("/<int:id>", methods=["GET"])
@token_required
def venta_por_id(id):
    venta = ventas_crud().read_by_id(id)
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify(venta), 200

@ventas_bp.route("/usuario/<int:id>", methods=["GET"])
@token_required
def ventas_por_usuario(id):
    ventas = ventas_crud().read_by_usuario(id)
    if not ventas:
        return jsonify({"mensaje": "No hay ventas para este usuario"}), 404
    return jsonify(ventas), 200

@ventas_bp.route("/producto/<int:id>", methods=["GET"])
@token_required
def ventas_por_producto(id):
    ventas = ventas_crud().read_by_producto(id)
    if not ventas:
        return jsonify({"mensaje": "No hay ventas para este producto"}), 404
    return jsonify(ventas), 200

@ventas_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def eliminar_venta(id):
    ok = ventas_crud().delete_venta(id)
    if not ok:
        return jsonify({"error": "No se pudo eliminar la venta"}), 400
    return jsonify({"deleted": True}), 200

@ventas_bp.route("/reporte_mensual", methods=["GET"])
@token_required
def reporte_mensual():
    mes = request.args.get("mes")
    if not mes:
        return jsonify({"error": "Debe indicar mes YYYY-MM"}), 400

    crud = ventas_crud()
    ventas = crud.read_all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Ventas"

    ws.append(["ID", "Usuario", "Producto", "Cantidad", "Total", "Fecha"])

    for v in ventas:
        if v["registro"].startswith(mes):
            ws.append([
                v["id"],
                v["id_usuario"],
                v["id_producto"],
                v["cantidad"],
                v["total_venta"],
                v["registro"]
            ])

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    wb.save(tmp.name)

    return send_file(
        tmp.name,
        as_attachment=True,
        download_name=f"reporte_ventas_{mes}.xlsx"
    )
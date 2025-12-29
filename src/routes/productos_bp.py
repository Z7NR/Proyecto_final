from flask import Blueprint, request, jsonify, make_response
from io import StringIO
import csv, json, re
from src.crud.productos_crud import product_crud
from src.routes.usuarios_bp import token_required   
from src.scrapers.generic_scraper import GenericScraper

productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')

@productos_bp.route('/', methods=['POST'], strict_slashes=False)
@productos_bp.route('/crear', methods=['POST'], strict_slashes=False)
@token_required
def crear_producto():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    precio_raw = data.get('precio', 0.0)
    stock_raw = data.get('stock', 0)
    
    if not nombre:
        return jsonify({'error': 'nombre es requerido'}), 400
    
    try:
        if isinstance(precio_raw, str):
            precio_sanit = re.sub(r'[^0-9\.,-]', '', precio_raw).replace(',', '.')
            precio = float(precio_sanit) if precio_sanit not in ('', '-', '.') else 0.0
        else:
            precio = float(precio_raw)
        if precio < 0:
            return jsonify({'error': 'precio no puede ser negativo'}), 400
    except Exception:
        return jsonify({'error': 'precio tiene formato inválido'}), 400

    try:
        if isinstance(stock_raw, str):
            stock = int(re.sub(r'[^0-9-]', '', stock_raw) or 0)
        else:
            stock = int(stock_raw)
        if stock < 0:
            return jsonify({'error': 'stock no puede ser negativo'}), 400
    except Exception:
        return jsonify({'error': 'stock tiene formato inválido'}), 400

    crud = product_crud()
    try:
        new_id = crud.create_product(
            nombre,
            data.get('descripcion', ''),
            precio,
            data.get('categoria', ''),
            stock
        )
        
        if new_id is not None:
            return jsonify({'id': new_id, 'message': 'Producto creado'}), 201
        
        return jsonify({'error': 'No se pudo crear producto en la base de datos'}), 400

    except Exception as e:
        print(f"Error al crear producto: {e}")
        return jsonify({'error': str(e)}), 500

@productos_bp.route("", methods=['GET'])
def listar_productos():
    crud = product_crud()

    nombre = request.args.get("nombre")
    categoria = request.args.get("categoria")

    if nombre:
        productos = crud.read_by_name(nombre)
    elif categoria:
        productos = crud.read_by_category(categoria)
    else:
        productos = crud.read_product()

    return jsonify(productos), 200

@productos_bp.route('/<int:product_id>', methods=['GET'])
def obtener_producto(product_id):
    crud = product_crud()
    prod = crud.get_product_by_id(product_id)
    if prod:
        return jsonify(prod), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/<int:product_id>', methods=['PUT', 'PATCH'])
@token_required
def actualizar_producto(product_id):
    data = request.get_json() or {}
    fields = {}

    for key in ['nombre', 'descripcion', 'precio', 'categoria', 'stock']:
        if key in data:
            fields[key] = data[key]

    if not fields:
        return jsonify({'error': 'Nada para actualizar'}), 400

    crud = product_crud()
    ok = crud.update_product(product_id, fields)

    if ok:
        return jsonify({'updated': True}), 200
    return jsonify({'error': 'No se pudo actualizar'}), 400

@productos_bp.route('/<int:product_id>', methods=['DELETE'])
@token_required
def eliminar_producto(product_id):
    crud = product_crud()
    ok = crud.delete_product(product_id)
    if ok:
        return jsonify({'deleted': True}), 200
    return jsonify({'error': 'No se pudo eliminar'}), 400

@productos_bp.route('/export', methods=['GET'])
def exportar_productos():
    fmt = request.args.get('format', 'csv').lower()

    crud = product_crud()
    productos = crud.read_product()

    if fmt == 'json':
        resp = make_response(json.dumps(productos, ensure_ascii=False))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Content-Disposition'] = 'attachment; filename=productos.json'
        return resp
    
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['id','nombre','descripcion','precio','categoria','stock','registro'])
    for p in productos:
        writer.writerow([
            p['id'], p['nombre'], p['descripcion'], p['precio'],
            p['categoria'], p['stock'], p['registro']
        ])
    resp = make_response(si.getvalue())
    resp.headers['Content-Type'] = 'text/csv'
    resp.headers['Content-Disposition'] = 'attachment; filename=productos.csv'
    return resp

@productos_bp.route('/import', methods=['POST'])
@token_required
def importar_producto():
    data = request.get_json() or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "url requerida"}), 400

    try:
        scraper = GenericScraper()
        producto = scraper.scrape(url)

        crud = product_crud()
        new_id = crud.create_product(
            producto["nombre"],
            producto["descripcion"],
            producto["precio"],
            producto["categoria"],
            producto["stock"]
        )

        return jsonify({
            "id": new_id,
            "nombre": producto["nombre"],
            "precio": producto["precio"]
        }), 201

    except Exception as e:
        return jsonify({"error": "No se pudo importar el producto"}), 500

    
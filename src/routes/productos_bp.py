from flask import Blueprint, request, jsonify, make_response
from io import StringIO
import csv, json, requests, re
from bs4 import BeautifulSoup
from src.crud.productos_crud import product_crud
from src.routes.usuarios_bp import token_required

productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')

@productos_bp.route('/', methods=['POST'])
@productos_bp.route('/crear', methods=['POST'])
@token_required
def crear_producto():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    precio_raw = data.get('precio', 0.0) #hacer aqui una validacion por si usan "," o "."
    stock_raw = data.get('stock', 0)
    
    if not nombre:
        return jsonify({'error': 'nombre es requerido'}), 400
    
    try:
        # Acepta int/float o strings con coma/punto
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
        if new_id:
            return jsonify({'id': new_id}), 201
        return jsonify({'error': 'No se pudo crear producto'}), 400
    except Exception as e:
        try:
            import sqlite3
            if isinstance(e, sqlite3.IntegrityError):
                return jsonify({'error': 'Conflicto en la base de datos (posible duplicado)'}), 409
        except Exception:
            pass
        print(f"Error al crear producto: {e}")
        return jsonify({'error': 'Error interno'}), 500

@productos_bp.route('/', methods=['GET'])
def listar_productos():
    q = request.args.get('q')
    crud = product_crud()
    if q:
        productos = crud.search_products(q)
    else:
        productos = crud.read_products()
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
    for key in ['nombre','descripcion','precio','categoria','stock']:
        if key in data:
            fields[key] = data.get(key)
    if not fields:
        return jsonify({'error': 'Nada para actualizar'}), 400
    crud = product_crud()
    ok = crud.update_product(product_id, **fields)
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
    productos = crud.read_products()
    if fmt == 'json':
        content = json.dumps(productos, ensure_ascii=False)
        resp = make_response(content)
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        resp.headers['Content-Disposition'] = 'attachment; filename=productos.json'
        return resp
    # CSV
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['id','nombre','descripcion','precio','categoria','stock','registro'])
    for p in productos:
        writer.writerow([p.get('id'), p.get('nombre'), p.get('descripcion'), p.get('precio'), p.get('categoria'), p.get('stock'), p.get('registro')])
    output = make_response(si.getvalue())
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    output.headers['Content-Disposition'] = 'attachment; filename=productos.csv'
    return output

@productos_bp.route('/importar', methods=['POST'])
@token_required
def importar_producto_por_url():
    data = request.get_json() or {}
    url = data.get('url')
    if not url:
        return jsonify({'error': 'url requerida'}), 400
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible)'}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return jsonify({'error': 'No se pudo obtener la página'}), 400
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('h1') or soup.find('title')
        nombre = title.get_text(strip=True) if title else None
        price = None
        selectors = ['.price', '.product-price', '[itemprop=price]', '.precio', '.Precio']
        for sel in selectors:
            el = soup.select_one(sel)
            if el and el.get_text(strip=True):
                price = el.get_text(strip=True)
                break
        precio_val = None
        if price:
            num = re.sub(r'[^0-9\\.,]', '', price)
            num = num.replace(',', '.')
            try:
                precio_val = float(num)
            except Exception:
                precio_val = None
        descripcion = None
        desc_el = soup.find('meta', {'name':'description'}) or soup.find('div', {'class':'description'}) or soup.find('p')
        if desc_el and desc_el.get('content'):
            descripcion = desc_el.get('content')
        elif desc_el:
            descripcion = desc_el.get_text(strip=True)
        if not nombre:
            return jsonify({'error': 'No se pudo extraer nombre'}), 400
        crud = product_crud()
        new_id = crud.create_product(nombre, descripcion or '', precio_val or 0.0, 'importado', 0)
        return jsonify({'id': new_id, 'nombre': nombre, 'precio': precio_val}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
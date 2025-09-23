from flask import Flask, jsonify

from src.routes.usuarios_bp import usuarios_bp
from src.routes.productos_bp import productos_bp
from src.routes.ventas_bp import ventas_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        'JSON_SORT_KEYS': False
    })

# Registrar Blueprints con prefijos
    app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
    app.register_blueprint(productos_bp, url_prefix="/api/productos")
    app.register_blueprint(ventas_bp, url_prefix="/api/ventas")

    @app.route('/health', methods=['GET'])
    def health():
            return jsonify({'status':'ok'})
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask
from src.routes.usuarios_bp import usuarios_bp
from src.routes.productos_bp import productos_bp
from src.routes.ventas_bp import ventas_bp

app = Flask(__name__)

# Registrar Blueprints con prefijos
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
app.register_blueprint(productos_bp, url_prefix="/api/productos")
app.register_blueprint(ventas_bp, url_prefix="/api/ventas")

if __name__ == "__main__":
    app.run(debug=True)
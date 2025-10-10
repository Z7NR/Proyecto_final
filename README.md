# Proyecto_final - API E-commerce (Flask + SQLite)

## Requisitos
- Python 3.10+
- pip install -r requirements.txt

## Configuración
1. Copia `.env.example` a `.env` y configura `SECRET_KEY`, `DATABASE` si necesario.
2. Crear tablas: 
   ```bash
   python -c "from src.data.data_base import DBAdvanceManager; DBAdvanceManager().create_tables()"
   ```

## Ejecutar servidor
```bash
export FLASK_APP=src.app:create_app
flask run
# o
python -m src.app
```

## Tests
```bash
pip install -r requirements.txt
pytest -q
```

## Endpoints principales
- `POST /api/usuarios/crear` — crear usuario
- `POST /api/usuarios/login` — obtener token
- `POST /api/productos/crear` — crear producto (Bearer token)
- `GET /api/productos/listar` — listar productos
- `POST /api/ventas/crear` — crear venta (Bearer token)
- `GET /api/ventas/listar` — listar ventas
- `GET /health` — estado del servidor

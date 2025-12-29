# Proyecto_final - API E-commerce (Flask + SQLite)

API REST desarrollada en Flask que implementa un sistema básico de
e-commerce con gestión de usuarios, productos y ventas.
Incluye autenticación JWT, control de stock y scraping de productos
desde sitios externos usando BeautifulSoup.

## Tecnologías utilizadas
- Python 3.10+
- Flask
- SQLite
- JWT (autenticación)
- BeautifulSoup (web scraping)
- openpyxl (reportes de ventas)
- pytest (tests)

## Requisitos
- Python 3.10+
- pip install -r requirements.txt

## Configuración
1. Copia `.env.example` a `.env` y configura `SECRET_KEY` y `DATABASE` si es necesario.
2. Crear tablas:
   ```bash
   python -c "from src.data.data_base import DBAdvanceManager; DBAdvanceManager().create_tables()"

## Ejecutar servidor

export FLASK_APP=src.app:create_app
flask run
# o
python -m src.app

### Reporte mensual de ventas

GET /api/ventas/reporte_mensual?mes=YYYY-MM

Genera un archivo Excel con las ventas del mes indicado.

Ejemplo:
GET /api/ventas/reporte_mensual?mes=2025-10

Notas:
- El parámetro `mes` debe enviarse en formato `YYYY-MM`
- El archivo se descarga automáticamente en formato `.xlsx`

## Tests

pip install -r requirements.txt
pytest -q

## Endpoints principales

POST /api/usuarios/crear — crear usuario

POST /api/usuarios/login — obtener token

POST /api/productos/crear — crear producto (Bearer token)

POST /api/productos/importar — importar producto vía scraping

POST /api/ventas/crear — crear venta (Bearer token)

GET /health — estado del servidor

## Notas

El scraping se realiza mediante BeautifulSoup sin uso de navegador.

La disponibilidad de datos depende de la estructura HTML del sitio origen.
import pytest
from src.app import create_app
from src.data.data_base import DBAdvanceManager

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

import os

@pytest.fixture(autouse=True)
def setup_db():
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    db = DBAdvanceManager()
    db.create_tables()
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture
def auth_token(client):
    client.post("/api/usuarios/crear", json={
        "nombres": "Test",
        "apellidos": "User",
        "edad": 30,
        "telefono": "123456789",
        "email": "test@test.com",
        "clave": "1234",
        "ciudad": "Ciudad",
        "pais": "Pais"
    })

    resp = client.post("/api/usuarios/login", json={
        "email": "test@test.com",
        "clave": "1234"
    })

    data = resp.get_json()
    assert resp.status_code == 200
    assert "access_token" in data

    return data["access_token"]
def get_token(client):
    client.post("/api/usuarios/crear", json={
        "nombres": "Admin",
        "apellidos": "Test",
        "edad": 40,
        "telefono": "555555",
        "email": "admin@test.com",
        "clave": "admin",
        "ciudad": "MX",
        "pais": "Mexico"
    })

    resp = client.post("/api/usuarios/login", json={
        "email": "admin@test.com",
        "clave": "admin"
    })

    return resp.get_json()["token"]

def test_crear_producto(client, auth_token):
    resp = client.post(
        "/api/productos/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "nombre": "Producto Test",
            "precio": 10,
            "categoria": "Test",
            "stock": 5
        }
    )
    assert resp.status_code == 201

def test_listar_productos(client):
    resp = client.get("/api/productos")
    assert resp.status_code == 200
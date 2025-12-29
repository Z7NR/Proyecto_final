def test_registro_usuario(client):
    resp = client.post("/api/usuarios/crear", json={
        "nombres": "Juan",
        "apellidos": "Perez",
        "edad": 30,
        "telefono": "123456789",
        "email": "juan@test.com",
        "clave": "1234",
        "ciudad": "Bogota",
        "pais": "Colombia"
    })

    assert resp.status_code == 201


def test_login_usuario(client):
    client.post("/api/usuarios/crear", json={
        "nombres": "Ana",
        "apellidos": "Lopez",
        "edad": 25,
        "telefono": "987654321",
        "email": "ana@test.com",
        "clave": "abcd",
        "ciudad": "Lima",
        "pais": "Peru"
    })

    resp = client.post("/api/usuarios/login", json={
        "email": "ana@test.com",
        "clave": "abcd"
    })

    data = resp.get_json()
    assert resp.status_code == 200
    assert "access_token" in data
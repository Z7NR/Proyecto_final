def test_crear_venta(client, auth_token):
    resp_prod = client.post(
        "/api/productos",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "nombre": "Producto Test",
            "descripcion": "Producto de prueba",
            "precio": 100,
            "stock": 10
        }
    )
    
    assert resp_prod.status_code == 201, f"Fallo crear producto: {resp_prod.data.decode()}"
    
    data_prod = resp_prod.get_json()
    producto_id = data_prod.get("id")

    resp_venta = client.post(
        "/api/ventas",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "id_producto": producto_id,
            "cantidad": 2
        }
    )
    
    assert resp_venta.status_code == 201, f"Fallo crear venta: {resp_venta.data.decode()}"

def test_reporte_mensual(client, auth_token):
    resp = client.get(
        "/api/ventas/reporte_mensual?mes=2025-10",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert resp.status_code == 200
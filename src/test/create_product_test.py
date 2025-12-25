from src.crud.productos_crud import product_crud

def main():
    pc = product_crud()
    new_id = pc.create_product(
        nombre="Producto de prueba",
        descripcion="Producto creado para test manual",
        precio=15.99,
        categoria="Test",
        stock=10
    )
    if new_id:
        print(f"✅ Producto creado con éxito (id={new_id})")
    else:
        print("❌ Error: no se pudo crear el producto")

if __name__ == "__main__":
    main()
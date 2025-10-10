import pytest
from src.data.data_base import DBAdvanceManager
from src.crud.productos_crud import product_crud
from src.crud.ventas_crud import sales_crud
from src.crud.usuarios_crud import user_crud

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    DBAdvanceManager().create_user_tables()
    yield

def test_create_sale_reduces_stock():
    ucrud = user_crud()
    pc = product_crud()
    vc = sales_crud()

    # Crear usuario y producto
    uid = ucrud.create_user("Sale","User",25,"000","sale_user@example.com","pass","ciudad","pais")
    pid = pc.create_product("ProdTest","desc", 10.0, "cat", 5)
    assert isinstance(pid, int)

    # Crear venta de cantidad 3
    res = vc.create_sale(uid, pid, 3)
    assert isinstance(res, dict)
    assert res.get("total") == pytest.approx(30.0)

    prod = pc.get_product_by_id(pid)
    assert prod["stock"] == 2

def fails_insufficient_stock():
    ucrud = user_crud()
    pc = product_crud()
    vc = sales_crud()

    uid = 1
    pid = 1
    res = vc.create_sale(uid, pid, 9999)
    assert isinstance(res, dict)
    assert "error, no hay stock" in res

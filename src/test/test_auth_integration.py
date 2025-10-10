import pytest
from src.data.data_base import DBAdvanceManager
from src.crud.usuarios_crud import user_crud
from src.utils.auth import auth_function

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # crea tablas antes del módulo de tests
    DBAdvanceManager().create_user_tables()
    yield


def test_register_and_login_and_verify_token():
    crud = user_crud()
    user_id = crud.create_user("Test", "User", 30, "000000000", "test_integ@example.com", "pass1234", "Ciudad", "Pais")
    assert isinstance(user_id, int)

    token = auth_function().login("test_integ@example.com", "pass1234")
    assert token is not None

    payload = auth_function.verify_token(token)
    assert payload is not None
    assert payload.get("sub") == user_id


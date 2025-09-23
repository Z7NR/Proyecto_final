import pytest
from src.utils.security import hash_password, check_password

def test_hash_and_check_password_success():

    pwd = "MiContraseñaDePrueba123!"
    hashed = hash_password(pwd)

    assert isinstance(hashed, str)
    assert len(hashed) > 0

    assert check_password(pwd, hashed) is True

def test_check_password_failure():
    pwd = "MiContraseñaDePrueba123!"
    wrong = "OtraContra!"
    hashed = hash_password(pwd)

    assert check_password(wrong, hashed) is False

def test_invalid_inputs():

    assert check_password(None, None) is False
    assert check_password("a", None) is False
    assert check_password(None, "hash") is False
    
    with pytest.raises(ValueError):
        hash_password(None)
import pytest
from src.utils.security import hash_password, check_password

def hash_check_password():#

    pwd = "MiContraseñaDePrueba123!"
    hashed = hash_password(pwd)

    assert isinstance(hashed, str)
    assert len(hashed) > 0

    assert check_password(pwd, hashed) is True

def check_password_failure():
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

def test_same_password():
    pwd = "repite_esta"
    h1 = hash_password(pwd)
    h2 = hash_password(pwd)
    assert h1 != h2
    assert check_password(pwd, h1) is True
    assert check_password(pwd, h2) is True
import os
from dotenv import load_dotenv
import bcrypt

_BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))

def hash_password(password: str) -> str:
    if password is None:
        raise ValueError("password no puede ser None")
    if not isinstance(password, str):
        raise TypeError("password debe ser str")
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(password: str, hashed: str) -> bool:
    if password is None or hashed is None:
        return False
    if not isinstance(password, str) or not isinstance(hashed, str):
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False

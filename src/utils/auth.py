import jwt, datetime, os
from datetime import timezone
from dotenv import load_dotenv
from src.utils.security import check_password
from src.data.data_base import DBAdvanceManager

load_dotenv() #<con esto cargo las variables del .evn
SECRET_KEY = os.getenv("SECRET_KEY", "defaul_secret")

import datetime
from datetime import timezone
import jwt
import sqlite3
from src.data.data_base import DBAdvanceManager
from src.utils.security import check_password
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "cambia_esto")

class auth_function(DBAdvanceManager):
    def login(self, email: str, clave: str):

        try:
            print("DEBUG: intentando login con", email)
            self.get_connection()
            self.cursor.execute("SELECT id, clave_hash FROM usuarios WHERE email = ?", (email,))
            user = self.cursor.fetchone()
            self.close_connection()
            if not user:
                return None

            if isinstance(user, sqlite3.Row):
                user_id_db = user["id"]
                clave_hash = user["clave_hash"]
            else:
                user_id_db = user[0]
                clave_hash = user[1]

            if not check_password(clave, clave_hash):
                return None

            now_utc = datetime.datetime.now(timezone.utc)
            payload = {
                "iat": int(now_utc.timestamp()),
                "exp": int((now_utc + datetime.timedelta(hours=1)).timestamp()),
                "sub": user_id_db,
                "user_id": user_id_db
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            if isinstance(token, bytes):
                token = token.decode("utf-8")
            print("DEBUG: login generado token =", token)
            return token

        except Exception as e:
            print(f"Error en login: {e}")
            return None

    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        

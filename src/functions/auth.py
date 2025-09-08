import jwt, datetime, os
from dotenv import load_dotenv
from src.utils.security import check_password
from src.data_base import DBAdvanceManager

load_dotenv() #<con esto cargo las variables del .evn
SECRET_KEY = os.getenv("SECRET_KEY", "defaul_secret")

class auth_function(DBAdvanceManager):
    def login(self, email, clave):
        try:
            self.get_connection()
            self.cursor.execute("SELECT id, clave_hash FROM usuarios WHERE email = ?", (email,))
            user = self.cursor.fetchone() #<devuelve una tupla [0,1]
            self.close_connection()

            if user and check_password(clave, user[1]): #<verificacion con hash
                payload = {
                    "user_id": user[0],
                    "iat": datetime.datetime.itcnow(), #<cuando se creo
                    "exp": datetime.datetime.itcnow() + datetime.timedelta(hours=1) #<cuando vence
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                return token
            else:
                return None
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
        

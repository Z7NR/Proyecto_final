import sqlite3
import os
from dotenv import load_dotenv #permite conectarse al .env y usar los datos en el

class DBAdvanceManager:

    def __init__(self):
        load_dotenv() #aqui esta cargando del .env la ruta donde estara el DB 
        self.DB_PATH = os.getenv("DATABASE_URL", "ecommerce_proyectofinal.db").replace("sqlite:///", "") #debido a que sqlite no lee los slash usamos ´replace´ para quitarlos
        self.conn = None    
        self.cursor = None
    
    def get_connection(self):
        try:
            self.conn = sqlite3.connect(self.DB_PATH) #variable definida arriba. Contiene la ruta.
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            print(f"Conectado a la base de datos {self.DB_PATH}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print(f"Conexion a la base de datos {self.DB_PATH} terminada")

    def create_user_tables(self):
        try:
            self.get_connection()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    telefono TEXT UNIQUE,
                    email TEXT UNIQUE NOT NULL,
                    clave_hash TEXT NOT NULL,
                    ciudad TEXT NOT NULL,
                    pais TEXT NOT NULL,
                    registro DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """)
            
            print(f"Tabla usuarios creada con exito")  
            
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()

    def product_create_tables(self):
        try:    
            self.get_connection()
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL,
                stock INTEGER NOT NULL,
                registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            print(f"Tabla productos creada con exito")  
            
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()

    def sales_create_tables(self):
        try:    
            self.get_connection()
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                total_venta REAL NOT NULL,
                registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )
            """)
            print(f"Tabla ventas creada con exito")  
            
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()

    def exception_error(self, e):
        print(f"Error al crear la tabla: {e}")


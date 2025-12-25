import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

class DBAdvanceManager:

    def __init__(self):
        load_dotenv()
        self.DB_PATH = os.getenv("DATABASE_URL", "ecommerce.db").replace("sqlite:///", "")
        self.conn = None
        self.cursor = None

    def get_connection(self):
        try:
            if self.conn is None:
                self.conn = sqlite3.connect(self.DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
                self.conn.row_factory = sqlite3.Row
                self.cursor = self.conn.cursor()
                self.cursor.execute("PRAGMA foreign_keys = ON;")
                print(f"Conectado a la base de datos {self.DB_PATH}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
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
                );
            """)
            self.conn.commit()
            print("Tabla usuarios creada con exito")
        except sqlite3.Error as e:
            self.exception_error(e)
            raise
        finally:
            self.close_connection()

    def create_product_tables(self):
        try:
            self.get_connection()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    precio REAL NOT NULL,
                    categoria TEXT NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0,
                    registro DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
            print("Tabla productos creada con exito")
        except sqlite3.Error as e:
            self.exception_error(e)
            raise
        finally:
            self.close_connection()

    def create_sales_tables(self):
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
                );
            """)
            self.conn.commit()
            print("Tabla ventas creada con exito")
        except sqlite3.Error as e:
            self.exception_error(e)
            raise
        finally:
            self.close_connection()

    def create_tables(self):
        self.create_user_tables()
        self.create_product_tables()
        self.create_sales_tables()

    def exception_error(self, e):
        print(f"Error en DBAdvanceManager: {e}")
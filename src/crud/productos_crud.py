import sqlite3
from datetime import datetime
from src.data.data_base import DBAdvanceManager
from src.utils.security import hash_password
from src.scrapers.generic_scraper import GenericScraper

class product_crud(DBAdvanceManager):

    def create_product(self, nombre, descripcion, precio, categoria, stock, registro=None):
        try:
            self.get_connection()
            if registro is None:
                registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                INSERT INTO productos (nombre, descripcion, precio, categoria, stock, registro)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, descripcion, precio, categoria, stock, registro))
            self.conn.commit()
            new_id = self.cursor.lastrowid
            return new_id
        except sqlite3.IntegrityError as e:
            self.exception_error(e)
            return None
        except sqlite3.Error as e:
            self.exception_error(e)
            return None
        finally:
            self.close_connection()

    def read_product(self):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM productos")
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()

    def update_product(self, product_id: int, fields: dict):
        try:
            if not fields:
                return False

            columnas = ", ".join([f"{k} = ?" for k in fields.keys()])
            valores = list(fields.values())
            valores.append(product_id)

            self.get_connection()
            self.cursor.execute(
                f"UPDATE productos SET {columnas} WHERE id = ?",
                valores
            )
            self.conn.commit()

            return self.cursor.rowcount > 0

        except sqlite3.Error as e:
            self.exception_error(e)
            return False

        finally:
            self.close_connection()


    def delete_product(self, product_id: int):
        try: 
            self.get_connection()
            self.cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))
            self.conn.commit()
            print("Producto eliminado con exito")
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            self.exception_error(e)
            return False
        finally:
            self.close_connection()

    def get_product_by_id(self, product_id: int):
        try:
            self.get_connection()
            self.cursor.execute("SELECT id, nombre, descripcion, precio, categoria, stock, registro FROM productos WHERE id = ?", (product_id,))
            row = self.cursor.fetchone()
            if not row:
                return None

            if isinstance(row, sqlite3.Row):
                return {
                    "id": row["id"],
                    "nombre": row["nombre"],
                    "descripcion": row["descripcion"],
                    "precio": row["precio"],
                    "categoria": row["categoria"],
                    "stock": row["stock"],
                    "registro": row["registro"]
                }
            else:
                return {
                    "id": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "precio": row[3],
                    "categoria": row[4],
                    "stock": row[5],
                    "registro": row[6]
                }
        except sqlite3.Error as e:
            self.exception_error(e)
            return None
        finally:
            self.close_connection()

    def read_by_name(self, nombre):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()

    def read_by_category(self, categoria):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM productos WHERE categoria = ?", (categoria,))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()
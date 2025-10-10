import sqlite3
from datetime import datetime
from src.data.data_base import DBAdvanceManager
from src.utils.security import hash_password

class product_crud(DBAdvanceManager):

    def create_product(self, nombre, descripcion, precio, categoria, stock):
        registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.get_connection()
            self.cursor.execute("""
                INSERT INTO productos (nombre, descripcion, precio, categoria, stock, registro) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, descripcion, precio, categoria, stock, registro))
            self.conn.commit()
            print("Producto insertado con éxito")
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()

    def read_product(self):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM productos")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()

    def update_product(self, user_id, nuevos_datos):
        try:
            self.get_connection()
            self.cursor.execute("""
                UPDATE productos
                SET nombres = ?, descripcion = ?, precio = ?, categoria = ?, stock = ?
                WHERE id = ?
            """, (*nuevos_datos, user_id)) #pendiente despues de stock, quizas vaya una coma ahí
            self.conn.commit
            print("Producto actualizado con exito")
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()

    def delete_product(self, user_id):
        try: 
            self.get_connection()
            self.cursor.execute("DELETE FROM productos WHERE id = ?", (user_id,))
            self.conn.commit()
            print("Producto eliminado con exito")
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()


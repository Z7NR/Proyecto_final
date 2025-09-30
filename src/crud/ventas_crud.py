import sqlite3
import os
from src.data.data_base import DBAdvanceManager
from src.utils.security import hash_password

class sales_crud(DBAdvanceManager):

    
    def create_sale(self, id_usuario, id_producto, cantidad, total_venta):
        try:
            self.get_connection()
            self.cursor.execute("""
                INSERT INTO ventas (id_usuario, id_producto, cantidad, total_venta)
                VALUES (?, ?, ?, ?)
            """, (id_usuario, id_producto, cantidad, total_venta))
            self.conn.commit()
            print("Venta registrada con éxito")
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()

    def read_sales(self):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM ventas")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()

    def update_sale(self, sale_id, nuevos_datos):
        try:
            self.get_connection()
            self.cursor.execute("""
                UPDATE ventas
                SET id_usuario = ?, id_producto = ?, cantidad = ?, total_venta = ?
                WHERE id = ?
            """, (*nuevos_datos, sale_id))
            self.conn.commit()
            print("Venta actualizada con éxito")
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()

    def delete_sale(self, sale_id):
        try:
            self.get_connection()
            self.cursor.execute("DELETE FROM ventas WHERE id = ?", (sale_id,))
            self.conn.commit()
            print("Venta eliminada con éxito")
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()
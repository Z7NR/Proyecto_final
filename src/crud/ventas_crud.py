import sqlite3
from src.data.data_base import DBAdvanceManager

class ventas_crud(DBAdvanceManager):

    def create_venta(self, id_usuario, id_producto, cantidad):
        try:
            self.get_connection()

            self.cursor.execute(
                "SELECT precio, stock FROM productos WHERE id = ?",
                (id_producto,)
            )
            producto = self.cursor.fetchone()

            if not producto:
                return {"error": "Producto no existe"}

            if producto["stock"] < cantidad:
                return {"error": "Stock insuficiente"}

            total = producto["precio"] * cantidad

            self.cursor.execute("""
                INSERT INTO ventas (id_usuario, id_producto, cantidad, total_venta)
                VALUES (?, ?, ?, ?)
            """, (id_usuario, id_producto, cantidad, total))

            self.cursor.execute("""
                UPDATE productos
                SET stock = stock - ?
                WHERE id = ?
            """, (cantidad, id_producto))

            self.conn.commit()
            return self.cursor.lastrowid

        except sqlite3.Error as e:
            self.exception_error(e)
            return None
        finally:
            self.close_connection()

    def read_all(self):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM ventas")
            return [dict(r) for r in self.cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            self.close_connection()

    def read_by_id(self, venta_id):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        finally:
            self.close_connection()

    def read_by_usuario(self, user_id):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM ventas WHERE id_usuario = ?", (user_id,))
            return [dict(r) for r in self.cursor.fetchall()]
        finally:
            self.close_connection()

    def read_by_producto(self, product_id):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM ventas WHERE id_producto = ?", (product_id,))
            return [dict(r) for r in self.cursor.fetchall()]
        finally:
            self.close_connection()

    def delete_venta(self, venta_id):
        try:
            self.get_connection()

            self.cursor.execute(
                "SELECT id_producto, cantidad FROM ventas WHERE id = ?",
                (venta_id,)
            )
            venta = self.cursor.fetchone()
            if not venta:
                return False

            self.cursor.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE id = ?
            """, (venta["cantidad"], venta["id_producto"]))

            self.cursor.execute("DELETE FROM ventas WHERE id = ?", (venta_id,))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            self.close_connection()
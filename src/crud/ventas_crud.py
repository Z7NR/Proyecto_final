import sqlite3
import os
from src.data.data_base import DBAdvanceManager
from src.utils.security import hash_password
from datetime import datetime

class ventas_crud(DBAdvanceManager):

    def create_sale(self, id_usuario: int, id_producto: int, cantidad: int, total_venta: float = None): 
        try:
            self.get_connection()
            self.cursor.execute("SELECT id, precio, stock FROM productos WHERE id = ?", (id_producto,))
            prod = self.cursor.fetchone()
            if not prod:
                return {"error": "producto no encontrado"}

            # obtener precio y stock de forma uniforme (soporta sqlite3.Row o tuplas)
            precio_db, stock_actual = ( (prod["precio"], prod["stock"]) if isinstance(prod, sqlite3.Row) else (prod[1], prod[2]) )

            # validar y normalizar cantidad y precio
            try:
                cantidad = int(cantidad)
                precio_db = float(precio_db)
            except (TypeError, ValueError):
                return {"error": "cantidad o precio con formato inválido"}

            if cantidad <= 0:
                return {"error": "cantidad debe ser mayor que 0"}
            if stock_actual < cantidad:
                return {"error": "stock insuficiente"}

            # calcular total si no fue proporcionado
            if total_venta is None:
                total_venta = precio_db * cantidad
            nuevo_stock = stock_actual - cantidad
            self.cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id_producto))
            registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                INSERT INTO ventas (id_usuario, id_producto, cantidad, total_venta, registro)
                VALUES (?, ?, ?, ?, ?)
            """, (id_usuario, id_producto, cantidad, total_venta, registro))

            self.conn.commit()
            new_id = self.cursor.lastrowid

            return {"id": new_id, "total": total_venta, "cantidad": cantidad}
        except sqlite3.Error as e:
            self.exception_error(e)
            return {"error": str(e)}
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
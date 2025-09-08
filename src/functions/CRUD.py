import sqlite3
import os
from data_base import DBAdvanceManager
from src.utils.security import hash_password

class CRUD_function(DBAdvanceManager):

#CRUD de usuarios

    def create_user(self, nombres, apellidos, edad, telefono, email, clave, ciudad, pais):
        try:
            self.get_connection()
            clave_hash = hash_password(clave)
            self.cursor.execute("""
                INSERT INTO usuarios (nombres, apellidos, edad, telefono, email, clave, ciudad, pais) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombres, apellidos, edad, telefono, email, clave_hash, ciudad, pais))
            self.conn.commit()
            print("Usuario insertado con éxito")
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()

    def read_user(self):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM usuarios")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()

    def update_user(self, user_id, nuevos_datos):
        try:
            self.get_connection()
            self.cursor.execute("""
                UPDATE usuarios
                SET nombres = ?, apellidos = ?, edad = ?, telefono = ?, email = ?, clave_hash = ?, ciudad = ?, pais = ?
                WHERE id = ?
            """, (*nuevos_datos, user_id))
            self.conn.commit
            print("Usuario actualizado con exito")
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()

    def delete_user(self, user_id):
        try: 
            self.get_connection()
            self.cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            self.conn.commit()
            print("Usuario eliminado con exito")
        except sqlite3.Error as e:
            self.exception_error(e)
        finally:
            self.close_connection()
    
#CRUD de productos

    def create_product(self, nombres, descripcion, precio, categoria, stock, registro):
        try:
            self.get_connection()
            self.cursor.execute("""
                INSERT INTO productos (nombres, descripcion, precio, categoria, stock, registro) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombres, descripcion, precio, categoria, stock, registro))
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

#CRUD de ventas 

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
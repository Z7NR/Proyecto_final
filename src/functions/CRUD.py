import sqlite3
import os
from dotenv import load_dotenv #permite conectarse al .env y usar los datos en el
from data_base import DBAdvanceManager

class CRUD_function(DBAdvanceManager):
    
    def create_user(self, nombres, apellidos, edad, telefono, email, clave_hash, ciudad, pais):
        try:
            self.get_connection()
            self.cursor.execute("""
                INSERT INTO usuarios (nombres, apellidos, edad, telefono, email, clave_hash, ciudad, pais) 
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
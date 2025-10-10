import sqlite3
import os
from src.data.data_base import DBAdvanceManager
from src.utils.security import hash_password

class user_crud(DBAdvanceManager):

#CRUD de usuarios

    def create_user(self, nombres, apellidos, edad, telefono, email, clave, ciudad, pais):
        try:
            self.get_connection()
            clave_hash = hash_password(clave)
            self.cursor.execute("""
                INSERT INTO usuarios (nombres, apellidos, edad, telefono, email, clave_hash, ciudad, pais)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombres, apellidos, edad, telefono, email, clave_hash, ciudad, pais))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            # Manejar duplicado por email: devolver id existente
            msg = str(e)
            if "UNIQUE constraint failed: usuarios.email" in msg or "usuarios.email" in msg:
                try:
                    self.cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
                    row = self.cursor.fetchone()
                    if row:
                        return row[0]  # id existente
                except Exception:
                    pass
            # para otros IntegrityError dejamos que el flujo devuelva None
            self.exception_error(e)
            return None
        except sqlite3.Error as e:
            self.exception_error(e)
            return None
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
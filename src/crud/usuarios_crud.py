import sqlite3
from src.data.data_base import DBAdvanceManager
from src.utils.security import hash_password

class user_crud(DBAdvanceManager):

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
            if "usuarios.email" in str(e):
                try:
                    self.cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
                    row = self.cursor.fetchone()
                    return row["id"] if row else None
                except:
                    pass
            
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
            rows = self.cursor.fetchall()
            return [dict(r) for r in rows]
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()


    def read_id_user(self, user_id):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            self.exception_error(e)
            return None
        finally:
            self.close_connection()


    def read_by_country(self, pais):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM usuarios WHERE pais = ?", (pais,))
            rows = self.cursor.fetchall()
            return [dict(r) for r in rows]
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()


    def read_by_city(self, ciudad):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM usuarios WHERE ciudad = ?", (ciudad,))
            rows = self.cursor.fetchall()
            return [dict(r) for r in rows]
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()


    def read_by_age_range(self, min_age, max_age):
        try:
            self.get_connection()
            self.cursor.execute(
                "SELECT * FROM usuarios WHERE edad BETWEEN ? AND ?",
                (min_age, max_age)
            )
            rows = self.cursor.fetchall()
            return [dict(r) for r in rows]
        except sqlite3.Error as e:
            self.exception_error(e)
            return []
        finally:
            self.close_connection()


    def read_by_email(self, email):
        try:
            self.get_connection()
            self.cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            self.exception_error(e)
            return None
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
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            self.exception_error(e)
            return False
        finally:
            self.close_connection()


    def delete_user(self, user_id):
        try:
            self.get_connection()
            self.cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            self.exception_error(e)
            return False
        finally:
            self.close_connection()
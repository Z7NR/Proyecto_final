from src.data_base import DBAdvanceManager

class Reports(DBAdvanceManager):
    def count_sales_by_user(self, user_id):
        try:
            self.get_connection()
            self.cursor.execute("""
                    SELECT COUNT(*)
                    FROM ventas
                    WHERE id_usuario = ?            
            """, (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            self.exception_error(e)
            return 0
        finally:
            self.close_connection()

    def count_sales_all_users(self):
        try:
            self.get_connection()
            self.cursor.execute("""             
                SELECT u.id, u.nombres, u.apellidos, COUNT(v.id) as total_vestas
                FROM usuarios u
                LEFT JOIN ventas v ON u.id = v.id_usuario
                GROUP BY u.id, u.nombres, u.apellidos
                ORDER BY total_ventas DESC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            self.exception_error(e)
            return 0
        finally:
            self.close_connection()
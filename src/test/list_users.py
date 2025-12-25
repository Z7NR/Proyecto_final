import sqlite3

conn = sqlite3.connect("ecommerce.db")
cur = conn.cursor()
cur.execute("SELECT id, nombres, email FROM usuarios;")
rows = cur.fetchall()
print("USUARIOS EN DB:")
for r in rows:
    print(r)
conn.close()
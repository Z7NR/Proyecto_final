import sqlite3

conn = sqlite3.connect("ecommerce.db")
cur = conn.cursor()

print("Tablas encontradas en la base de datos:\n")
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cur.fetchall():
    print("-", row[0])

conn.close()
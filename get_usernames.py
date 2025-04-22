import sqlite3

conn = sqlite3.connect("data/beers.db")
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT username FROM beers")
users = sorted(set(row[0] for row in cursor.fetchall()))

conn.close()

print("✅ Final USERS list:")
for user in users:
    print(f'"{user}",')


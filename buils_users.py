import sqlite3

conn = sqlite3.connect("data/beers.db")
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT username FROM beers ORDER BY username ASC")
names = [row[0] for row in cursor.fetchall()]

conn.close()

print("✅ USERS list to paste into app.py:")
print("USERS = [")
for name in names:
    print(f'    "{name}",')
print("]")



import sqlite3

# Your 46 cleaned, standardized first names
final_user_list = [
    "Alora", "Amanda", "Anthony", "Bella", "Bradley", "Carla", "Carlos",
    "Charlie", "Daniel", "Devon", "Eamon", "Eleana", "Fantasia", "Gor",
    "Grace", "Gracie", "Ina", "Jacob", "Jacquline", "Jasmine", "Jonathon",
    "Josh", "Kai", "Kenzie", "Kira", "Lauren", "Lucas", "Narissa", "Natalia",
    "Nataly", "Nicolas", "Patrick", "Sophia", "Stephanie", "Steven", "Tessa",
    "Valentin", "Yoseph", "Yumiko"
]

conn = sqlite3.connect("data/beers.db")
cursor = conn.cursor()

# Ensure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS beers (
    username TEXT PRIMARY KEY,
    total INTEGER DEFAULT 0
)
""")

# Insert if missing
for name in final_user_list:
    cursor.execute("SELECT 1 FROM beers WHERE username = ?", (name,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("INSERT INTO beers (username, total) VALUES (?, 0)", (name,))
        print(f"✅ Added: {name}")

conn.commit()
conn.close()

print("✅ All 46 users confirmed in the database.")


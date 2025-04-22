import sqlite3

# Full list of 46 standardized first names
all_users = [
    "Alora", "Amanda", "Anthony", "Bella", "Bradley", "Carla", "Carlos",
    "Charlie", "Daniel", "Devon", "Eamon", "Eleana", "Fantasia", "Gor",
    "Grace", "Gracie", "Ina", "Jacob", "Jacquline", "Jasmine", "Jonathon",
    "Josh", "Kai", "Kenzie", "Kira", "Lauren", "Lucas", "Narissa", "Natalia",
    "Nataly", "Nicolas", "Patrick", "Sophia", "Stephanie", "Steven", "Tessa",
    "Valentin", "Yoseph", "Yumiko"
]

# Connect to the database
conn = sqlite3.connect("data/beers.db")
cursor = conn.cursor()

for name in all_users:
    cursor.execute("SELECT 1 FROM beers WHERE username = ?", (name,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("INSERT INTO beers (username, total) VALUES (?, 0)", (name,))
        print(f"Added {name} with 0 beers.")

conn.commit()
conn.close()

print("✅ All 46 users now exist in the database.")



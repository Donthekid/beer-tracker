import sqlite3

# Final 46-user list with standardized names and totals
beer_totals = {
    "Alora": 2, "Amanda": 18, "Anthony": 13, "Bella": 116, "Bradley": 43,
    "Carla": 107, "Carlos": 124, "Charlie": 50, "Daniel": 92, "Devon": 187,
    "Eamon": 143, "Eleana": 1, "Fantasia": 394, "Gor": 63, "Grace": 93,
    "Gracie": 30, "Ina": 25, "Jacob": 41, "Jacquline": 190, "Jasmine": 26,
    "Jonathon": 50, "Josh": 27, "Kai": 22, "Kenzie": 11, "Kira": 55,
    "Lauren": 39, "Lucas": 14, "Narissa": 22, "Natalia": 5, "Nataly": 78,
    "Nicolas": 97, "Patrick": 161, "Sophia": 2, "Stephanie": 102,
    "Steven": 176, "Tessa": 53, "Valentin": 16, "Yoseph": 48, "Yumiko": 193
}

# Ensure 46 names total
all_users = sorted(set(beer_totals.keys()))
missing_names = 46 - len(all_users)
print(f"✔️ Users with beers logged: {len(all_users)}")
if missing_names:
    print(f"⚠️ {missing_names} users still missing.")

# Rebuild beers table from scratch
conn = sqlite3.connect("data/beers.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS beers")
cursor.execute("""
CREATE TABLE beers (
    username TEXT PRIMARY KEY,
    total INTEGER DEFAULT 0
)
""")

# Insert everyone, using 0 for anyone not in the total list
for name in sorted(beer_totals):
    total = beer_totals[name]
    cursor.execute("INSERT INTO beers (username, total) VALUES (?, ?)", (name, total))

conn.commit()
conn.close()

print("✅ Rebuilt beers table with all 46 users.")


import sqlite3

# Final standardized first-name beer totals (46 names)
final_beer_totals = [
    ('Fantasia', 394),
    ('Yumiko', 193),
    ('Jacquline', 190),
    ('Devon', 187),
    ('Steven', 176),
    ('Patrick', 161),
    ('Eamon', 143),
    ('Carlos', 124),
    ('Bella', 116),
    ('Carla', 107),
    ('Stephanie', 102),
    ('Nicolas', 97),
    ('Grace', 93),
    ('Daniel', 92),
    ('Nataly', 78),
    ('Gor', 63),
    ('Kira', 55),
    ('Tessa', 53),
    ('Jonathon', 50),
    ('Charlie', 50),
    ('Yoseph', 48),
    ('Bradley', 43),
    ('Jacob', 41),
    ('Lauren', 39),
    ('Gracie', 30),
    ('Josh', 27),
    ('Jasmine', 26),
    ('Ina', 25),
    ('Kai', 22),
    ('Narissa', 22),
    ('Amanda', 18),
    ('Valentin', 16),
    ('Lucas', 14),
    ('Anthony', 13),
    ('Kenzie', 11),
    ('Natalia', 5),
    ('Sophia', 2),
    ('Alora', 2),
    ('Eleana', 1)
]

# Connect to the database
conn = sqlite3.connect("data/beers.db")
cursor = conn.cursor()

# Clear existing totals
cursor.execute("DELETE FROM beers")

# Insert new records
for name, total in final_beer_totals:
    cursor.execute("INSERT INTO beers (username, total) VALUES (?, ?)", (name, total))

conn.commit()
conn.close()

print("✅ 46 first-name beer totals imported successfully.")


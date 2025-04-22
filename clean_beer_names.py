import sqlite3

# Names that need fixing in the database
name_map = {
    "Fantasia(Zee)": "Fantasia",
    "jacqueline van luit": "Jacquline",
    "bradley": "Bradley",
    "kenzieeee☀️": "Kenzie",
    "Yumiko Bellon": "Yumiko",
    "Jonathan Mcnelis": "Jonathon"
}

conn = sqlite3.connect("data/beers.db")
cursor = conn.cursor()

for wrong, correct in name_map.items():
    # If correct name already exists, merge totals
    cursor.execute("SELECT total FROM beers WHERE username = ?", (wrong,))
    row = cursor.fetchone()
    if row:
        amount = row[0]

        cursor.execute("SELECT total FROM beers WHERE username = ?", (correct,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                "UPDATE beers SET total = total + ? WHERE username = ?",
                (amount, correct)
            )
        else:
            cursor.execute(
                "INSERT INTO beers (username, total) VALUES (?, ?)",
                (correct, amount)
            )

        # Delete the old record
        cursor.execute("DELETE FROM beers WHERE username = ?", (wrong,))

conn.commit()
conn.close()

print("✅ Name cleanup complete. All beer totals merged correctly.")


from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'data/beers.db'

USERS = [
    "Alex", "Alora", "Amanda", "Anthony", "Bella", "Bradley", "Catlin", "Carla", "Carlos",
    "Charlie", "Daniel", "Devin", "Devon", "Eamon", "Eleana", "Eunsung", "Fantasia", "Gor",
    "Grace", "Gracie", "Ina", "Jacob", "Jacquline", "Jasmine", "Jon", "Jonathon",
    "Josh", "Kai", "Kenzie", "Khoudia", "Kira", "Lauren", "Lucas", "Narissa", "Natalia",
    "Nataly", "Nicolas", "Patrick", "Sophia", "Stephanie", "Steven", "Sue",
    "Tessa", "Valentin", "Yoseph", "Yumiko"
]

def query_db(query, args=(), one=False):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv

# 📊 HOME PAGE
@app.route('/')
def index():
    # Load beer totals
    data = {}
    rows = query_db('SELECT username, total FROM beers')
    for user in USERS:
        user_data = next((r for r in rows if r['username'] == user), None)
        data[user] = {"total": user_data['total'] if user_data else 0, "dates": {}}

    # Load AOTW
    aotw = query_db('SELECT * FROM aotw ORDER BY created_at DESC LIMIT 1', one=True)
    if aotw:
        aotw_data = dict(aotw)
    else:
        aotw_data = {"name": "TBD", "image": "", "message": ""}

    return render_template('index.html', users=USERS, data=data, aotw=aotw_data)

# 🍺 LOG BEERS
@app.route('/add', methods=['POST'])
def add_beer():
    username = request.json['username']
    count = int(request.json['count'])

    existing = query_db('SELECT total FROM beers WHERE username = ?', [username], one=True)
    if existing:
        new_total = existing['total'] + count
        query_db('UPDATE beers SET total = ? WHERE username = ?', [new_total, username])
    else:
        new_total = count
        query_db('INSERT INTO beers (username, total) VALUES (?, ?)', [username, new_total])

    return jsonify(success=True, new_total=new_total)

# 🔐 ADMIN: ADJUST BEERS
@app.route('/admin/adjust', methods=['POST'])
def admin_adjust():
    username = request.json['username']
    count = int(request.json['count'])

    existing = query_db('SELECT total FROM beers WHERE username = ?', [username], one=True)
    if existing:
        new_total = max(existing['total'] + count, 0)
        query_db('UPDATE beers SET total = ? WHERE username = ?', [new_total, username])
    else:
        new_total = max(count, 0)
        query_db('INSERT INTO beers (username, total) VALUES (?, ?)', [username, new_total])

    return jsonify(success=True, new_total=new_total)

# 👑 SET AOTW
@app.route('/admin/set_aotw', methods=['POST'])
def set_aotw():
    data = request.json
    name = data.get("name")
    image = data.get("image")
    message = data.get("message")
    query_db('INSERT INTO aotw (name, image, message) VALUES (?, ?, ?)', [name, image, message])
    return jsonify(success=True)

# 🔁 GLOBAL TOAST FEED
@app.route('/toast', methods=['GET'])
def get_toasts():
    results = query_db('SELECT * FROM toasts ORDER BY id DESC LIMIT 5')
    return jsonify([dict(row) for row in reversed(results)])

@app.route('/toast', methods=['POST'])
def post_toast():
    name = request.json.get("name")
    count = int(request.json.get("count"))
    timestamp = datetime.now().isoformat()

    # Check if last toast is same user → merge
    last = query_db('SELECT * FROM toasts ORDER BY id DESC LIMIT 1', one=True)
    if last and last["name"] == name:
        new_count = last["count"] + count
        query_db('UPDATE toasts SET count = ?, timestamp = ? WHERE id = ?', [new_count, timestamp, last["id"]])
    else:
        query_db('INSERT INTO toasts (name, count, timestamp) VALUES (?, ?, ?)', [name, count, timestamp])
        # Trim to max 5
        all_toasts = query_db('SELECT id FROM toasts ORDER BY id DESC')
        if len(all_toasts) > 5:
            to_delete = [row['id'] for row in all_toasts[5:]]
            for tid in to_delete:
                query_db('DELETE FROM toasts WHERE id = ?', [tid])

    return jsonify(success=True)

# 🏁 RUN APP
if __name__ == '__main__':
    app.run(debug=True)


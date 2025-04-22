from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 🧑‍🤝‍🧑 Predefined user list
USERS = [
    "Daniel", "Eamon", "Carlos", "Gor", "Grace", "Jacob", "Josh", "Lauren",
    "Natalia", "Patrick", "Stephanie", "Sophia", "Alex", "Alora", "Amanda",
    "Anthony", "Bella", "Bradley", "Caitlin", "Carla", "Charlie", "Devin",
    "Devon", "Eleana", "Eunsung", "Fantasia", "Gracie", "Ina", "Jacquline",
    "Jasmine", "Jon", "Jonathon", "Kai", "Kenzie", "Khoudia", "Kira", "Lucas",
    "Narissa", "Nataly", "Nicolas", "Steven", "Sue", "Tessa", "Valentin"
]

# 🍺 Beer totals
class BeerLog(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    total = db.Column(db.Integer, default=0)

# 🗓️ Optional: Date-based tracking
class BeerEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date = db.Column(db.String(20))
    amount = db.Column(db.Integer)

# 🏆 Alcoholic of the Week
class AOTW(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/')
def index():
    try:
        users = BeerLog.query.all()
        user_totals = {
            user.name: {"total": int(user.total), "dates": {}} for user in users
        }

        aotw_record = AOTW.query.first()
        aotw = aotw_record.name if aotw_record else None

        return render_template('index.html', users=USERS, data=user_totals, aotw=aotw)

    except Exception as e:
        print("🔥 ERROR in / route:", str(e))
        return f"<h1>500 Error</h1><pre>{str(e)}</pre>", 500

@app.route('/add', methods=['POST'])
def add_beer():
    data = request.get_json()
    name = data['username']
    count = int(data['count'])
    today = datetime.now().strftime('%Y-%m-%d')

    log = BeerLog.query.get(name)
    if not log:
        log = BeerLog(name=name, total=0)
        db.session.add(log)

    log.total += count
    db.session.add(BeerEntry(name=name, date=today, amount=count))
    db.session.commit()

    return jsonify(success=True, new_total=log.total)

# 🔧 One-time setup: create all users
@app.route('/init')
def init_db():
    db.create_all()
    for user in USERS:
        if not BeerLog.query.get(user):
            db.session.add(BeerLog(name=user, total=0))
    db.session.commit()
    return "✅ Database initialized with users!"

# 🔧 One-time setup: create AOTW table and default entry
@app.route('/init-aotw')
def init_aotw():
    db.create_all()
    if not AOTW.query.first():
        db.session.add(AOTW(name="No one yet"))
        db.session.commit()
    return "✅ AOTW table initialized!"

# 🛠 Update AOTW via browser (e.g. /set-aotw?name=Daniel)
@app.route('/set-aotw')
def set_aotw():
    name = request.args.get("name")
    if name and name in USERS:
        record = AOTW.query.first()
        if record:
            record.name = name
        else:
            db.session.add(AOTW(name=name))
        db.session.commit()
        return f"✅ AOTW set to {name}"
    return "❌ Invalid name", 400
@app.route('/import')
def import_beer_totals():
    imported_totals = {
        "Grace": 93, "Daniel": 87, "Stephanie": 102, "Patrick": 161,
        "Eamon": 140, "Carlos": 124, "Bella": 116, "Carla": 107,
        "Nicolas": 86, "Nataly": 71, "Gor": 61, "Tessa": 53,
        "Kira": 49, "Bradley": 43, "Jacob": 41, "Lauren": 39,
        "Gracie": 30, "Fantasia": 407, "Yoseph": 46, "Yumiko": 193,
        "Jacquline": 184, "Jonathon": 50, "Kenzie": 8
    }

    for name, total in imported_totals.items():
        user = BeerLog.query.get(name)
        if user:
            user.total = total
        else:
            db.session.add(BeerLog(name=name, total=total))
    db.session.commit()

    return "✅ Imported beer totals from WhatsApp!"

if __name__ == '__main__':
    app.run(debug=True)



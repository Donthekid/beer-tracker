from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Get the database URL from Render environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User list (same as before)
USERS = [
    "Daniel", "Eamon", "Carlos", "Gor", "Grace", "Jacob", "Josh", "Lauren",
    "Natalia", "Patrick", "Stephanie", "Sophia", "Alex", "Alora", "Amanda",
    "Anthony", "Bella", "Bradley", "Caitlin", "Carla", "Charlie", "Devin",
    "Devon", "Eleana", "Eunsung", "Fantasia", "Gracie", "Ina", "Jacquline",
    "Jasmine", "Jon", "Jonathon", "Kai", "Kenzie", "Khoudia", "Kira", "Lucas",
    "Narissa", "Nataly", "Nicolas", "Steven", "Sue", "Tessa", "Valentin"
]

# 📦 Beer totals table
class BeerLog(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    total = db.Column(db.Integer, default=0)

# 🗓️ Optional: Date-based logging (expand later)
class BeerEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date = db.Column(db.String(20))
    amount = db.Column(db.Integer)

# 🔨 Create tables on startup
with app.app_context():
    db.create_all()
    for user in USERS:
        if not BeerLog.query.get(user):
            db.session.add(BeerLog(name=user, total=0))
    db.session.commit()

@app.route('/')
def index():
    try:
        users = BeerLog.query.all()
        user_totals = {
            user.name: {"total": user.total if user.total else 0, "dates": {}} for user in users
        }
    except Exception as e:
        print("🔥 ERROR loading homepage:", e)
        user_totals = {name: {"total": 0, "dates": {}} for name in USERS}
    return render_template('index.html', users=USERS, data=user_totals)

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

@app.route('/init')
def init_db():
    db.create_all()
    for user in USERS:
        if not BeerLog.query.get(user):
            db.session.add(BeerLog(name=user, total=0))
    db.session.commit()
    return "✅ Database initialized with users!"

if __name__ == '__main__':
    app.run(debug=True)



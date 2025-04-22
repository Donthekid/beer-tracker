from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

USERS = [
    "Alora", "Amanda", "Anthony", "Bella", "Bradley", "Carla", "Carlos", "Charlie", "Daniel",
    "Devon", "Eamon", "Eleana", "Fantasia", "Gor", "Grace", "Gracie", "Ina", "Jacob", "Jacquline",
    "Jasmine", "Jonathon", "Josh", "Kai", "Kenzie", "Kira", "Lauren", "Lucas", "Narissa", "Natalia",
    "Nataly", "Nicolas", "Patrick", "Sophia", "Stephanie", "Steven", "Tessa", "Valentin", "Yoseph", "Yumiko",
    "Caitlin", "Sue", "Alex", "Devin", "Eunsung"
]

class BeerLog(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    total = db.Column(db.Integer, default=0)

class BeerEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date = db.Column(db.String(20))
    amount = db.Column(db.Integer)

class AOTW(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    caption = db.Column(db.String(100))
    image = db.Column(db.String(200))

@app.route('/')
def index():
    user_totals = {}
    for user in USERS:
        record = BeerLog.query.get(user)
        total = record.total if record else 0
        user_totals[user] = {"total": total, "dates": {}}

    aotw_record = AOTW.query.first()
    aotw = aotw_record.name if aotw_record else None

    return render_template('index.html', users=USERS, data=user_totals, aotw=aotw)

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

@app.route('/import')
def import_beer_totals():
    imported_totals = {
        "Fantasia": 394, "Yumi": 190, "Jacquline": 190, "Devon": 187, "Steven": 176,
        "Patrick": 161, "Eamon": 143, "Carlos": 124, "Bella": 116, "Carla": 107,
        "Stephanie": 102, "Nicolas": 97, "Grace": 93, "Daniel": 92, "Nataly": 78,
        "Gor": 63, "Tessa": 53, "Jonathon": 50, "Charlie": 50, "Kira": 49,
        "Yoseph": 46, "Bradley": 43, "Jacob": 41, "Lauren": 39, "Gracie": 30,
        "Josh": 27, "Jasmine": 26, "Ina": 25, "Kai": 22, "Narissa": 22,
        "Amanda": 22, "Lucas": 17, "Valentin": 16, "Anthony": 13, "Kenzie": 11,
        "Natalia": 5, "Sophia": 2, "Alora": 2, "Eleana": 1
    }

    # Delete all current records first
    BeerLog.query.delete()
    db.session.commit()

    # Add ALL users with correct total or 0 fallback
    for name in USERS:
        total = imported_totals.get(name, 0)
        db.session.add(BeerLog(name=name, total=total))

    db.session.commit()
    return "✅ All users imported with 0+ beer totals"

@app.route('/init')
def init_db():
    db.create_all()
    for user in USERS:
        if not BeerLog.query.get(user):
            db.session.add(BeerLog(name=user, total=0))
    db.session.commit()
    return "✅ Database initialized!"

@app.route('/init-aotw')
def init_aotw():
    db.create_all()
    if not AOTW.query.first():
        db.session.add(AOTW(name="No one yet"))
        db.session.commit()
    return "✅ AOTW initialized!"

@app.route('/set-aotw')

def set_aotw():
    name = request.args.get("name")
    caption = request.args.get("caption", "")
    image = request.args.get("image", "")

    if not name:
        return "❌ Missing name", 400

    record = AOTW.query.first()
    if record:
        record.name = name
        record.caption = caption
        record.image = image
    else:
        db.session.add(AOTW(name=name, caption=caption, image=image))
    db.session.commit()

    return f"✅ AOTW set to {name}"

@app.route('/debug-totals')
def debug_totals():
    all_users = BeerLog.query.all()
    return "<br>".join(f"{u.name}: {u.total}" for u in all_users)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/reset-aotw-table')
def reset_aotw_table():
    try:
        db.session.execute('DROP TABLE IF EXISTS aotw CASCADE;')
        db.session.commit()
        db.create_all()
        db.session.add(AOTW(name="No one yet", caption="", image=""))
        db.session.commit()
        return "✅ AOTW table reset and initialized!"
    except Exception as e:
        return f"❌ Error: {str(e)}", 500


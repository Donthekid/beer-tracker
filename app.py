from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data/beers.json'

USERS = [
    "Daniel", "Eamon", "Carlos", "Gor", "Grace", "Jacob", "Josh", "Lauren",
    "Natalia", "Patrick", "Stephanie", "Sophia", "Alex", "Alora", "Amanda",
    "Anthony", "Bella", "Bradley", "Caitlin", "Carla", "Charlie", "Devin",
    "Devon", "Eleana", "Eunsung", "Fantasia", "Gracie", "Ina", "Jacquline",
    "Jasmine", "Jon", "Jonathon", "Kai", "Kenzie", "Khoudia", "Kira", "Lucas",
    "Narissa", "Nataly", "Nicolas", "Steven", "Sue", "Tessa", "Valentin"
]

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    data = load_data()
    for user in USERS:
        if user not in data:
            data[user] = {"total": 0, "dates": {}}
    return render_template('index.html', users=USERS, data=data)

@app.route('/add', methods=['POST'])
def add_beer():
    username = request.json['username']
    count = int(request.json['count'])
    today = datetime.now().strftime('%Y-%m-%d')
    data = load_data()

    if username not in data:
        data[username] = {"total": 0, "dates": {}}

    data[username]["total"] += count
    data[username]["dates"][today] = data[username]["dates"].get(today, 0) + count

    save_data(data)
    return jsonify(success=True, new_total=data[username]["total"])

if __name__ == '__main__':
    app.run(debug=True)



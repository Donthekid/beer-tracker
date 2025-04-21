from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Paths to your data files
DATA_FILE = 'data/beers.json'
AOTW_FILE = 'data/aotw.json'

# Your full list of users
USERS = [
    "Daniel", "Eamon", "Carlos", "Gor", "Grace", "Jacob", "Josh", "Lauren",
    "Natalia", "Patrick", "Stephanie", "Sophia", "Alex", "Alora", "Amanda",
    "Anthony", "Bella", "Bradley", "Caitlin", "Carla", "Charlie", "Devin",
    "Devon", "Eleana", "Eunsung", "Fantasia", "Gracie", "Ina", "Jacquline",
    "Jasmine", "Jon", "Jonathon", "Kai", "Kenzie", "Khoudia", "Kira", "Lucas",
    "Narissa", "Nataly", "Nicolas", "Steven", "Sue", "Tessa", "Valentin"
]

# Load beer data from JSON file
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save beer data to JSON
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Load Alcoholic of the Week data
def load_aotw():
    try:
        with open(AOTW_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"name": "TBD", "image": "", "message": ""}

# Home route
@app.route('/')
def index():
    data = load_data()
    aotw = load_aotw()

    # Ensure all users are in the dataset
    for user in USERS:
        if user not in data:
            data[user] = {"total": 0, "dates": {}}

    return render_template('index.html', users=USERS, data=data, aotw=aotw)

# Route to add beers
@app.route('/add', methods=['POST'])
def add_beer():
    username = request.json['username']
    count = int(request.json['count'])
    date = datetime.now().strftime('%Y-%m-%d')

    data = load_data()

    if username not in data:
        data[username] = {"total": 0, "dates": {}}

    data[username]["total"] += count
    data[username]["dates"][date] = data[username]["dates"].get(date, 0) + count

    save_data(data)
    return jsonify(success=True, new_total=data[username]["total"])
@app.route('/admin/adjust', methods=['POST'])
def admin_adjust():
    username = request.json['username']
    count = int(request.json['count'])

    data = load_data()

    if username not in data:
        data[username] = {"total": 0, "dates": {}}

    data[username]["total"] += count
    if data[username]["total"] < 0:
        data[username]["total"] = 0

    save_data(data)
    return jsonify(success=True, new_total=data[username]["total"])
@app.route('/admin/set_aotw', methods=['POST'])
def set_aotw():
    data = request.json
    name = data.get("name", "")
    image = data.get("image", "")
    message = data.get("message", "")

    aotw_data = {
        "name": name,
        "image": image,
        "message": message
    }

    try:
        with open(AOTW_FILE, 'w') as f:
            json.dump(aotw_data, f, indent=2)
        return jsonify(success=True)
    except:
        return jsonify(success=False), 500

# Run the app
TOAST_FILE = 'data/toast.json'

def load_toasts():
    try:
        with open(TOAST_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_toasts(toasts):
    with open(TOAST_FILE, 'w') as f:
        json.dump(toasts, f, indent=2)

@app.route('/toast', methods=['GET'])
def get_toasts():
    return jsonify(load_toasts())

@app.route('/toast', methods=['POST'])
def post_toast():
    data = request.json
    name = data.get("name")
    count = int(data.get("count"))
    timestamp = datetime.now().isoformat()

    toasts = load_toasts()

    if toasts and toasts[-1]["name"] == name:
        toasts[-1]["count"] += count
        toasts[-1]["timestamp"] = timestamp
    else:
        toasts.append({
            "name": name,
            "count": count,
            "timestamp": timestamp
        })
        if len(toasts) > 5:
            toasts.pop(0)

    save_toasts(toasts)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)


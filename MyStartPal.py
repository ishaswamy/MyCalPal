from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo

import urllib.parse

app = Flask(__name__)
# myStartPal = Blueprint(__name__, "myStartPal")


# MongoDB connection string with properly escaped username and password
username = "eij"
password = "c@lori3"
cluster_url = "cluster0.ydug9w5.mongodb.net"
uri = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@{cluster_url}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)

# Access a database
db = client['MyCalPal']

# client = MongoClient(url)
# db = client['MyCalPal']
loginInfo = db['Credentials']
foodItem = db['Food Intake']
waterItem = db['Water Intake']

#result = foodItem.insert_one({'name': 'Orange', 'meal': 'Breakfast', 'calories': 180})


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = loginInfo.find_one({"username": username, "password": password})

    if user:
        return "Login successful!"
    else:
        return "Invalid username or password."

@app.route ('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if loginInfo.find_one({"username": username}):
        return "Username already exists. Please choose another one."
    else:
        loginInfo.insert_one({'username': username, 'password': password})
        return "Account successfully created."


@app.route('/add_food', methods=['POST'])
def add_food():
    food_name = request.form.get('food-name')
    meal = request.form.get('meal')
    calories = request.form.get('calories')
    

    # Insert food intake data into the database
    
    try:
        foodItem.insert_one({'name': food_name, 'meal': meal, 'calories': calories})
        
        return jsonify({'message': "Food intake added successfully."})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/add_water', methods=['POST'])
def add_water():
    water_amount = request.form['water_amount']
    waterItem.insert_one({'water_amount': water_amount})
    return jsonify({'message': "Water intake added successfully."})

    

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import urllib.parse

app = Flask(__name__)

# MongoDB connection string with properly escaped username and password
username = "eij"
password = "c@lori3"
cluster_url = "cluster0.ydug9w5.mongodb.net"
uri = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@{cluster_url}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)

# Access the database
db = client['MyCalPal']

# Access the collections
loginInfo = db['Credentials']
foodItem = db['Food Intake']
waterItem = db['Water Intake']

@app.route('/')
def login():
    return render_template('LogIn.html')

@app.route('/signup', methods=['POST'])
def signup():
    # Get user information from the form
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    birthday = request.form['birth_month'] + '/' + request.form['birth_day'] + '/' + request.form['birth_year']
    sex = request.form['sex']
    weight = int(request.form['weight'])
    height_feet = int(request.form['height_feet'])
    height_inches = int(request.form['height_inches'])
    reason = request.form['reason']
    weight_goal = request.form['weight_goal']

    # Check if the username already exists
    if loginInfo.find_one({"username": username}):
        return "Username already exists. Please choose another one."
    else:
        # Insert user information into the database
        result = loginInfo.insert_one({
            'name': name,
            'username': username,
            'password': password,
            'birthday': birthday,
            'sex': sex,
            'weight': weight,
            'height_feet': height_feet,
            'height_inches': height_inches,
            'reason': reason,
            'weight_goal': weight_goal
        })
        # Print the result of the database insertion
        print(f"Database Insertion Result: {result.inserted_id}")
        # Redirect to Home.html upon successful account creation
        return redirect(url_for('home'))

@app.route('/Registration.html')
def register():
    return render_template('Registration.html')

@app.route('/login', methods=['POST'])
def login_process():
    username = request.form['username']
    password = request.form['password']
    user = loginInfo.find_one({"username": username, "password": password})
    if user:
        # Redirect to Home.html upon successful login
        return redirect(url_for('home'))
    else:
        return "Invalid username or password."

@app.route('/Home.html')
def home():
    # Render the Home.html template
    return render_template('Home.html')


@app.route('/LogIn.html')
def login_page():
    return render_template('LogIn.html')


@app.route('/add_food', methods=['POST'])
def add_food():
    food_name = request.form.get('food-name')
    meal = request.form.get('meal')
    calories = request.form.get('calories')

    # Insert food intake data into the database
    try:
        foodItem.insert_one({'name': food_name, 'meal': meal, 'calories': calories})
        # Retrieve all food items from the database
        all_food_items = foodItem.find({})
        # Render the Home.html template with the updated food items
        return render_template('Home.html', food_items=all_food_items)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run()

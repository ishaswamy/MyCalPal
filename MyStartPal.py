from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
import urllib.parse
import hashlib  


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
        hashed_username = hashlib.sha256(username.encode()).hexdigest()
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
            'weight_goal': weight_goal,
            'collection_name': hashed_username
        })
        
        db.create_collection(f'{hashed_username}')
                    
                   
        # Print the result of the database insertion
        print(f"Database Insertion Result: {result.inserted_id}")
        # Redirect to Home.html upon successful account creation
        return redirect(url_for('home'))

@app.route('/Registration.html')
def register():
    return render_template('Registration.html')

@app.route('/login', methods=['POST'])
def login_process():
    session.clear()
    username = request.form['username']
    password = request.form['password']
    user = loginInfo.find_one({"username": username, "password": password})
    if user:
        # Set the username in the session
        session['username'] = username
        # Redirect to Home.html upon successful login
        return redirect(url_for('home'))
    else:
        # Render the login page with an error message
        return render_template('LogIn.html', error_message="Invalid username or password.")


@app.route('/Home.html')
def home():
    # Retrieve all food items from the currently logged-in user's collection
    username = session.get('username')
    if username:
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        items = list(user_collection.find())
        # Render the Home.html template and pass the food items
        return render_template('Home.html', items=items)
    else:
        return redirect(url_for('login'))


@app.route('/LogIn.html')
def login_page():
    return render_template('LogIn.html')

@app.route('/add_water', methods=['POST'])
def add_water():
    water_amount = request.form.get('water-amount')
    meal = request.form.get('meal')
    calories = request.form.get('calories')

    # Retrieve the username from the session
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Insert food intake data into the user's collection in the database
    try:
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        user_collection.insert_one({'name': "water", 'ounces': water_amount})
        # Redirect to Home.html upon successful insertion
        return redirect(url_for('home'))
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/add_food', methods=['POST'])
def add_food():
    food_name = request.form.get('food-name')
    meal = request.form.get('meal')
    calories = request.form.get('calories')

    # Retrieve the username from the session
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Insert food intake data into the user's collection in the database
    try:
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        user_collection.insert_one({'name': food_name, 'meal': meal, 'calories': calories})
        # Redirect to Home.html upon successful insertion
        return redirect(url_for('home'))
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run()

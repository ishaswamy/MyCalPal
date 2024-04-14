
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


from datetime import datetime

@app.route('/Home.html')
def home():
    username = session.get('username')
    if username:
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Fetch food items logged on the current day
        items = list(user_collection.find({
            "name": {"$ne": "water"},
            "datetime": {"$regex": f"^{current_date}"}
        }))
        
        # Fetch water items separately
        water_items = list(user_collection.find({
            "name": "water",
            "datetime": {"$regex": f"^{current_date}"}
        }))
        
        # Calculate total calories
        total_calories = sum(item['calories'] for item in items)
        
        # Calculate total ounces consumed for water
        total_ounces = sum(int(item['ounces']) for item in water_items)
        
        # Group food items by meal
        meals = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snack': []
        }

        for item in items:
            if 'meal' in item:
                meals[item['meal']].append(item)
        
        return render_template('Home.html', meals=meals, water_items=water_items, total_calories=total_calories, total_ounces=total_ounces)
    else:
        return redirect(url_for('login'))





@app.route('/LogIn.html')
def login_page():
    return render_template('LogIn.html')

from datetime import datetime

@app.route('/add_water', methods=['POST'])
def add_water():
    water_amount = request.form.get('water-amount')
    meal = request.form.get('meal')
    
    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Retrieve the username from the session
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Insert water intake data into the user's collection in the database
    try:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        user_collection.insert_one({
            'name': "water", 
            'ounces': water_amount,
            'datetime': current_datetime  # Add complete timestamp
        })
        # Redirect to Home.html upon successful insertion
        return redirect(url_for('home'))
    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/add_food', methods=['POST'])
def add_food():
    food_name = request.form.get('food-name')
    meal = request.form.get('meal')
    calories = round(float(request.form.get('calories'))) 
    grams = request.form.get('grams')
    
    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Retrieve the username from the session
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Insert food intake data into the user's collection in the database
    try:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        user_collection.insert_one({
            'name': food_name, 
            'meal': meal, 
            'calories': round(calories), 
            'grams': grams,
            'datetime': current_datetime  # Add complete timestamp
        })
    
        # Redirect to Home.html upon successful insertion
        return redirect(url_for('home'))
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/food_items')
def get_food_items():
    try:
        # Access the "Potential Food Collection" from the "MyCalPal" database
        potential_food_collection = db['Potential Food Collection']
        
        # Fetch all documents and extract the "name" attribute
        food_items_cursor = potential_food_collection.find({}, {'name': 1})
        
        # Convert cursor to list of dictionaries
        food_list = [item['name'] for item in food_items_cursor]
        
        print(f"Fetched Food Items: {food_list}")  # Debug print
        
        # Return food items as JSON response
        return jsonify(food_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calories_per_serving', methods=['GET'])
def get_calories_per_serving():
    food_name = request.args.get('food_name')
    try:
        potential_food_collection = db['Potential Food Collection']
        food_item = potential_food_collection.find_one({"name": food_name})
        
        if not food_item:
            return jsonify({'error': 'Food item not found'}), 404
        
        calories_per_serving = food_item.get('calories_per_serving', 0)
        return jsonify({'calories_per_serving': calories_per_serving})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/food_info', methods=['GET'])
def get_food_info():
    food_name = request.args.get('food_name')
    try:
        potential_food_collection = db['Potential Food Collection']
        food_item = potential_food_collection.find_one({"name": food_name})
        
        if not food_item:
            return jsonify({'error': 'Food item not found'}), 404
        
        calories_per_serving = food_item.get('calories_per_serving', 0)
        serving_size_grams = food_item.get('serving_size_grams', 1)  # Default to 1 if serving_size_grams is not available
        
        return jsonify({
            'calories_per_serving': calories_per_serving,
            'serving_size_grams': serving_size_grams
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
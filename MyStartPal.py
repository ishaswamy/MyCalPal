from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
import urllib.parse
import hashlib  

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Create MongoDB connection
username = "eij"
password = "c@lori3"
cluster_url = "cluster0.ydug9w5.mongodb.net"
uri = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@{cluster_url}/?retryWrites=true&w=majority"
client = MongoClient(uri)

# Access database
db = client['MyCalPal']

# Access collections within database
loginInfo = db['Credentials']
potential_food_collection = db['Potential Food Collection']

# Launch LogIn Page when the application starts
@app.route('/')
def login():
    return render_template('LogIn.html')#display login page to user

#Route for user creating an account
@app.route('/signup', methods=['POST'])
def signup():
    # Receive user information from the registration form
    session.clear() #clear out anyone logged in prior (session data)
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
        hashed_username = hashlib.sha256(username.encode()).hexdigest() #hash username
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
        # Create collection corresponding with user to store intake information
        db.create_collection(f'{hashed_username}')
        # Redirect to Home.html upon successful account creation
        return redirect(url_for('home'))

# Render the signup page
@app.route('/Registration.html')
def register():
    return render_template('Registration.html')

# Update page to reflect user after they have logged in
@app.route('/login', methods=['POST'])
def login_process():
    session.clear() #clear old users out
    username = request.form['username']
    password = request.form['password']
    # Check database for user who matches entered credentials
    user = loginInfo.find_one({"username": username, "password": password})
    if user:
        # If user is found, set the username in the session
        session['username'] = username
        # Redirect to Home.html upon successful login
        return redirect(url_for('home'))
    else:
        # Render the login page with an error message displayed to user
        return render_template('LogIn.html', error_message="Invalid username or password.")

# Render tracking home page
@app.route('/Home.html')
def home():
    username = session.get('username') # find user from session
    if username:
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        # Get food items logged on the current day
        items = list(user_collection.find({
            "name": {"$ne": "water"},
            "datetime": {"$regex": f"^{current_date}"}
        }))
        
        # Get water items logged on current day
        water_items = list(user_collection.find({
            "name": "water",
            "datetime": {"$regex": f"^{current_date}"}
        }))
        
        # Calculate total calories
        total_calories = sum(item['calories'] for item in items)
        
        # Calculate total ounces consumed for water
        total_ounces = sum(int(item['ounces']) for item in water_items)
        
        # Sort food items by meal and add to corresponding list
        meals = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snack': []
        }
        for item in items:
            if 'meal' in item:
                meals[item['meal']].append(item)
        # Return home template with all the information to be displayed to user
        return render_template('Home.html', meals=meals, water_items=water_items, total_calories=total_calories, total_ounces=total_ounces)
    else:
        return redirect(url_for('login'))

# Render login page
@app.route('/LogIn.html')
def login_page():
    return render_template('LogIn.html')

# Handle water tracking
@app.route('/add_water', methods=['POST'])
def add_water():

    water_amount = request.form.get('water-amount')
    
    # Retrieve the username from the session
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Insert water intake data into the user's collection in the database
    try:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #get current time and date
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()] #find corresponding user collection
        user_collection.insert_one({ #add intake to database
            'name': "water", 
            'ounces': water_amount,
            'datetime': current_datetime 
        })
        # Redirect to Home.html upon successful insertion
        return redirect(url_for('home'))
    except Exception as e:
        return jsonify({'error': str(e)})


# Handle food tracking
@app.route('/add_food', methods=['POST'])
def add_food():
    # Get food name, meal type, calories, and portion size from form
    food_name = request.form.get('food-name')
    meal = request.form.get('meal')
    calories = round(float(request.form.get('calories'))) # round calories as integer
    grams = request.form.get('grams')

    # Retrieve the username from the session
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Insert food data into the user's collection in the database
    try:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_collection = db[hashlib.sha256(username.encode()).hexdigest()]
        user_collection.insert_one({
            'name': food_name, 
            'meal': meal, 
            'calories': round(calories), 
            'grams': grams,
            'datetime': current_datetime 
        })
        

        # Redirect to Home.html upon successful insertion
        return redirect(url_for('home'))
    except Exception as e:
        return jsonify({'error': str(e)})
    
# Show options for food items from database to user 
@app.route('/food_items')
def get_food_items():
    try:
        # Get all food documents and find the food name
        food_items_cursor = potential_food_collection.find({}, {'name': 1})
        
        # Convert cursor to list of dictionaries
        food_list = [item['name'] for item in food_items_cursor]
        
        # Return food items
        return jsonify(food_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Find calories per serving and grams per serving for the food item being logged
@app.route('/food_info', methods=['GET'])
def get_food_info():
    food_name = request.args.get('food_name')
    try:
        # Check if food item is in the collection
        potential_food_collection = db['Potential Food Collection']
        food_item = potential_food_collection.find_one({"name": food_name})
        
        if not food_item:
            return jsonify({'error': 'Food item not found'}), 404
        
        # Store and return food information
        calories_per_serving = food_item.get('calories_per_serving', 0)
        serving_size_grams = food_item.get('serving_size_grams', 1) 
        
        return jsonify({
            'calories_per_serving': calories_per_serving,
            'serving_size_grams': serving_size_grams
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
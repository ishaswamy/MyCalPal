from pymongo import MongoClient
from datetime import datetime
import urllib.parse, hashlib
from pymongo import MongoClient 

# import MyDatabasePal

# MongoDB connection string with properly escaped username and password
username = "eij"
password = "c@lori3"
cluster_url = "cluster0.ydug9w5.mongodb.net"
url = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@{cluster_url}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(url)
db = client['MyCalPal']

loginInfo = db['Credentials']

class MyCalPal:
    def __init__(self):
        self._username = ""
        self._password1 = ""
        self._password2 = ""
        self._email = ""
        self.msg = ""
        self.valid = True

    # Constructor            
    def MyCalPal(self, email, username, password1, password2):
        self._email = email
        self._username = username
        self._password1 = password1
        self._password2 = password2
       
    # getters
    def get_email(self):
        return self._email

    def get_username(self):
        return self._username
    
    def get_password1(self):
        return self._password1

    def get_password2(self):
        return self._password2    
    
    # setters
    def set_email(self, email):
        self._email = email

    def set_username(self, username):
        self._username = username
        
    def set_password1(self, password1):
        self._password1 = password1   

    def set_password1(self, password2):
        self._password2 = password2          

    def myValidPal(self, email, username, password1, password2):
        msg = ""
        valid = True 
        
        username, password1, password2 = username.strip(), password1.strip(),password2
        
        for x in username:
            if x == " ":
                msg += "User has unnecessary spaces.\n"
                valid = False

        if len(username) < 3: 
            msg += "Username is not longer than three characters.\n"
            valid = False 
            
        if username == password1:
            msg += "Username cannot be equal to password! \n"
            valid = False

        if loginInfo.find_one({'username': username}):
            msg += "Username already exists. \n"
            valid = False

        if loginInfo.find_one({'email': email}):
            msg += "Email already registered. \n"
            valid = False

        for x in password1:
            if x == " ":
                msg += "Password has unnecessary spaces.\n"
                valid = False
        
        password1 = password1.replace(" ", "")

        if password1 != password2:
            valid = False
            msg += "Passwords don't match. \n"

        if len(password1) <= 8: 
            msg += "Password must be at least 8 characters long. \n"
            valid = False
            
        special_characters = "!@#$%^&*();:<>,.//?'[]\\}{-_+=`~"
        checks = [any(char.isupper() for char in password1),
                  any(char.isdigit() for char in password1),
                  any(char in special_characters for char in password1),
                  any(char.isalpha() for char in password1)]
        
        for check, desc in zip(checks, ["uppercase letter", "digit", "special character", "alphabetical letter"]):
            if not check:
                msg += f"Password must have at least one {desc}.\n"
                valid = False

        self.msg = msg
        self.valid = valid
        return msg, valid

    def myLogPal(self, email, username, password):
        hashed_username = hashlib.sha256(username.encode()).hexdigest()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        credentials = loginInfo.find_one({'username': username})

        if credentials:
            # check the passworrd
            stored_password = credentials['password']
            if hashed_password == stored_password:
                self.msg = "Login successful."
                self.valid = True
            else:
                self.msg = "Incorrect password."
                self.valid = False
        else:
            msg = "Account not found."

        return self.msg, self.valid, hashed_username

class MyCalcPal:
    def __init__(self):
        self._hashlog = "" 
        self._food = "" 
        self._calories = 0 
        self._quantity = 1 

    # constructor function
    def MyCalcPal(self, hashlog, quantity, calories, food):
        self._quantity = quantity 
        self._calories = calories
        self._hash = hashlog
        self._food = food 

    # getters
    # gets calories and quantities
    def get_calories(self):
        return self._calories
    
    def get_quantity(self):
        return self._quantity
    
    def get_hashlog(self):
        return self._hashlog
    
    def get_food(self):
        return self._food
    
    # setters
    # sets calories and quantities
    def set_calories(self, calories):
        self._calories = calories
    
    def set_quantity(self, quantity):
        self._quantity = quantity        
    
    def set_hashlog(self, hashlog):
        self._hashlog = hashlog
    
    def set_food(self, food):
        self._food = food        
    
    def myAddPal(self, username, name, quantity, calories):
        # Get the current time
        current_time = datetime.now()
        
        userDb = db[username] # logs the user's into their personal database

        userDb.insert_one({'name': name, 
            'quantity': quantity, 'calories': calories, 
            'total_calories': (quantity * calories), 
            'time':current_time })

    def mySpamPal(self, username):
        userDb = db[username]  # logs the user into their personal database
        cursor = userDb.find()
        
        print("Calorie Chart:")
        print("{:<5} {:<20} {:<20} {:<10} {:<20}".format("No.", "Name", "Single Calories", "Quantity", "Total Calories"))
        print("-" * 75)
        
        for idx, document in enumerate(cursor, 1):
            print("{:<5} {:<20} {:<20} {:<10} {:<20}".format(idx, document['name'], document['calories'], document['quantity'], document['total_calories']))
            
        print("-" * 75)

    def myDeletePal(self, username):
        userDb = db[username]
        cursor = userDb.find()
        
        for idx, document in enumerate(cursor, 1):
            print("{:<5} {:<20} {:<20} {:<10} {:<20}".format(idx, document['name'], document['calories'], document['quantity'], document['total_calories']))
        
        print("-" * 75)

        if userDb.count_documents({}) == 0:
            print("Chart is empty.")
            return

        # Prompt user for the item to delete
        choice = input("Enter the number of the item you want to delete (or 'cancel' to abort): ").strip()
    
        if choice.lower() == 'cancel':
            print("Deletion aborted.")
            return
        
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a valid item number.")
            return
        
        # Get the selected document
        cursor.rewind() # go to beginning
        selected_document = None
        for idx, document in enumerate(cursor, 1):
            if idx == choice:
                selected_document = document
                break

        if selected_document:
            confirm = input(f"Are you sure you want to delete {selected_document['name']}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                userDb.delete_one({'_id': selected_document['_id']})
                print(f"{selected_document['name']} has been successfully deleted from your calorie chart.")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid item number. Please select a valid item.")


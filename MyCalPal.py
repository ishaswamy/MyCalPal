"""
MyCalPal - EIJ - Ethan Barthelemy, Isha Swamy, Julianne 
Development 1.1: 3.12.2024


Changelog 1.0 - 3.06.2024
- Developed start-code (menu for practice)


"""

"""
Create-Account Function:
    1. Prompt the user into making a username.
    2. Check database if username is available, if not, inform user.
    3. Input a password, password must meet the following conditions: 
        One capital, numbers, special character, and 8 characters total.
    4. If Password meets requirements, then create account and register.

Sign-In Function:
    1. User-input username & User-input password.
    2. Check if user username is registered within database.
    3. If username is not registered nor valid, return with the following: "Error: Username and Password not found."
    3. Check if password matches username, if password is not valid, return with the following: "Error: Username and Password not found."
    4. If both values values are valid, then sign the user in, and return the values.
    
Calorie Function:
    1. User inputs grams and/or calories for a certain food item. If calories aren't provided, use the grams: 
            i. protein: (x grams) * 4 calories
            ii. carbohydrages: (x grams) * 4 calories
            iii. fat: (x grams) * 9 calories
        a. Protein Cal + Carbo Cal + Fat Cal = Total Calories consumed
        b. Present the amount of calories the user has consumed.

"""
"""
Imports the database for MongoDB.

"""
import MyClassPal;

from pymongo import MongoClient

# Connect to MongoDB
#client = MongoClient("mongodb+srv://cluster0.ydug9w5.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient('mongodb://localhost:27017/')

# Access a database
db = client['MyCalPal']

# Access a collection
foodItem = db['item']

# Insert a document
result = foodItem.insert_one({'name': 'Orange', 'calories': 90})
print(result)

# Access a collection
loginInfo = db['user']






# Initiates the Program

import MyDatabasePal
import MyClassPal
    


def main():
    
    system_message = " " # prompt response meant to be run
    
    signup_or_login()
        

def signup_or_login():
    choice = int(input("Welcome to 'MyCalPal' would you like to: \n\n1.Login\n2.Create an Account\n3.Exit\n\n"))
    mcp = MyClassPal.MyCalPal()
    
    while(choice != 1) and (choice != 2) and (choice !=3): # Validity Checker for the Program
        print("Invalid input. Try Again.\n\n") 
        choice = 0 # Reset choice back to 0 to initiate the loop.
        choice = int(input("Would you like to: \n\n1.Login\n2.Create an Account\n3.Exit"))
        
    # Account Log-in Process
    if choice == 1:
        print("Log-In.\n----------\n\n")
        user = input("Input username: ")
        passw = input("Input password: ")
        login_user(user, passw)

    # Account Creation Process
    elif choice == 2:
        create_account()

    # Exits the program.
    elif choice == 3:
        print("Ending program.")

        
    
#create an account for user and add information to the system
def create_account():
    valid = False #checks if credentials are valid
    print("Creating Account.\n----------")
    while not valid: #ask for credentials until they meet requirements
        user = input("Input username: ")
        passw = input("Input password: ")
        if loginInfo.find_one({"username": user}): #check if username has already been used
            print("Username already exists. Please choose another one.")
        else:
            loginInfo.insert_one({'username': user, 'password': passw}) #add user credentials to database
            print("Account successfully created.") #display success message
            valid = True 


def login_user(username, password): #allow user to log in to the system
        user = loginInfo.find_one({"username": username, "password": password}) #check if credentials match an account in database
        if user: #if account was found, display success message
            print("Login successful!")
        else: #if credentials do not match existing account, display failure message
            print("Invalid username or password.")
    
 
        

# performs calorie calculator function
def CalcCals():
    calories = 0
    return calories  

    

if __name__ == "__main__":
    main()

# Close the connection
client.close()
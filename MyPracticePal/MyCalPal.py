# MyCalPal.py

"""
MyCalPal - EIJ - Ethan Barthelemy, Isha Swamy, Julianne 
Development 1.1: 4.09.2024

- Developed start-code (menu for practice)
"""

import MyClassPal;
from pymongo import MongoClient
import urllib.parse, hashlib, datetime
# import MyDatabasePal


# Classes
mcp = MyClassPal.MyCalPal()
mcc = MyClassPal.MyCalcPal()


# MongoDB connection string with properly escaped username and password
username = "eij"
password = "c@lori3"
cluster_url = "cluster0.ydug9w5.mongodb.net"
url = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@{cluster_url}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(url)
db = client['MyCalPal']

loginInfo = db['Credentials']

# Creates beta collection
# testing = db.create_collection('Beta')

def main():

    system_message = " " # prompt response meant to be run
    # print(ws) # checking
    
    signup_or_login()


def signup_or_login():
    while True: # Infinite loop until user chooses to exit
        try:
            choice = int(input("Welcome to 'MyCalPal' would you like to: \n1. Login\n2. Create an Account\n3. Exit\n\n"))
        except ValueError:
            print("Invalid. Please enter a number.")
            continue

        if choice == 1:
            print("\nLog-In.\n----------\n")
            email = input("Input email: ")
            username = input("Input username: ")
            password = input("Input password: ")

            message, valid, hashed_username = mcp.myLogPal(email, username, password)

            if valid:
                print(message)
                myLoggedIn(hashed_username)
                break  # Exit loop after successful login
            else:
                print(message)

        elif choice == 2:
            valid = False
            message = ""

            print("Creating Account.\n----------")
            while not valid:
                email = input("Input email: ")
                username = input("Input username: ")
                password1 = input("Input password: ")
                password2 = input("Confirm password: ")

                message, valid = mcp.myValidPal(email, username, password1, password2)

                if not valid:
                    print("Username or password not valid:\n" + message)

                else:
                    hashed_username = hashlib.sha256(username.encode()).hexdigest()
                    hashed_password = hashlib.sha256(password1.encode()).hexdigest()

                    loginInfo.insert_one({'email': email, 
                        'username': username, 
                        'password': hashed_password,
                        'collection_name': hashed_username})                

                    db.create_collection(f'{hashed_username}')
                    
                    print("Account successfully created.")
                    print("Logging in...\n")
                    break  # Exit loop after successful account creation

        elif choice == 3:
            print("Ending program.")
            break  # Exit loop and end program

def myChartPal(username):
    print("\n")
    mcc.mySpamPal(username)
    # chart_choice is mainly for the 'menu' screen for the calorie chart.
    choice = input("\nWould you like to: \n1. Add an item.\n2. Delete an item.\n3. Return to main login page.\n4.Log-Out\n")

    while True:
        if choice == '1': # Add an Item
            myCaloriePal(username)
        elif choice == '2': # Delete an Item
            mcc.myDeletePal(username)
        elif choice == '3': # Return to login / My Login
            myLoggedIn(username)
        elif choice == '4': # LogOut
            myOutPal()


def myCaloriePal(username):
    while True:
        name = input("What's the name? (Type '#' to exit): ")
        if name == "#":
            break  # Exit the loop if '#' is entered
        
        quantity = int(input("How much of this item did you consume? "))
        if quantity == "#":
            break  # Exit the loop if '#' is entered
        
        calories = int(input("How many calories does this item have? "))
        if calories == "#":
            break  # Exit the loop if '#' is entered

        # Process the input (e.g., add item to the list)
        mcc.myAddPal(username, name, quantity, calories)

    while True:
        choice = input("Would you like to: \n1.Check calorie chart.\n2.Check weekly intake.\n3.Return to main login page.\n")
        choice = choice.strip()

        while choice not in ['1' , '2', '3','4']:
            print("Wrong input or error.")
            choice = input("\nWould you like to: \n1.Check calorie chart.\n2.Check weekly intake.\n3.Return to main login page.\n4.Logout.")

        if choice == '1':
            myChartPal(username)

        if choice == '2':
            myIntakePal(username)

        if choice == '3':
            myLoggedIn(username)

        if choice == '4':
            myOutPal()

def myIntakePal(username): # Weekly Intake, Option 3
    calories = mcc.myWeekPal(username)
    
    print(f"Consumed approximately {calories} this week.")

    myLoggedIn(username)

def myOutPal(): # Log_Out
    print("Logging out...\n")
    signup_or_login()

def myLoggedIn(username):
    # userDb = db[username] # logs the user's into their personal database
    
    choice = input("Would you like to: \n1. Check your calorie chart.\n2. Add an item.\n3.Check your weekly intake.\n4. Log-Out.\n")
    choice = choice.strip()
   
    while choice not in ['1', '2', '3', '4']:
        choice = input("Would you like to: \n1. Check your calorie chart.\n2. Add an item.\n3.Check your weekly intake.\n4. Log-Out.\n")

    if choice == '1':
        myChartPal(username)
    elif choice == '2':
        myCaloriePal(username)
    elif choice == '3':
        myIntakePal(username)
    elif choice == '4':
        myOutPal()

if __name__ == "__main__":
    main()

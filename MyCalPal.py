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

# Initiates the Program

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
    if (choice == 1 ):
        print("Log-In.\n----------\n\n")
        user = input("Input username: ")
        passw = input("Input password: ")

    # Account Creation Process
    elif( choice == 2):
        valid = False
        message = ""

        print("Creating Account.\n----------")
        while (valid == False):
            user = input ("Input username: ")
            passw = input("Input password: ")
            
            message, valid = mcp.myValidPal(user, passw)
            
            if(valid == False):
                print("Username or password not valid:\n" + message)
           
            elif(valid==True):
                print("Account successfully created.")
     
    # Exits the program.
    elif(choice == 3):
        print("Ending program.")
 
        

# performs calorie calculator function
def CalcCals():
    calories = 0
    return calories  

    

if __name__ == "__main__":
    main()
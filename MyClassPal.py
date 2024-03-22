import MyDatabasePal as mydbp
import time 

class MyCalPal:
    def __init__(self):
        self._username = ""
        self._password = ""

    # Constructor            
    def MyCalPal(self, username, password):
        self._username = username
        self._password = password
       
    # getters
    def get_user(self):
        return self._username
    
    def get_passw(self):
        return self._password
    
    # setters
    def set_user(self, username):
        self._username = username
        
    def set_password(self, password):
        self._password = password        
        

        """
        checking the validity of passsword and username as valid credentials
        msg == the message provided after the program for validation has been run
        valid == a boolean variable for it the password is valid
        """
        
    def myValidPal(self, username, password):
       
        msg = ""
        valid = True 
        
        username, password = username.strip() , password.strip()  # removes end of line spaces from username password
        # print(username + " " + password)
        
        
        # username checker
        # checks if username has spaces
        for x in username:
            if x == " ":
                msg += "User has unnecessary spaces.\n"
                valid = False

        # checks if username is longer than three characters.
        if (len(username) < 3): 
            msg += "Username is not longer than three characters.\n"
            valid = False 
            
        # checks if username is equal to password
        if (username == password):
            msg += "Username cannot be equal to password! \n"
            valid = False

        # password checker
        # checks if the password has unnecessary spaces
        for x in password:
            if x == " ":
                msg += "Password has unnecessary spaces.\n"
                valid = False
        password.replace(" ","") # replaces spaces for the next line of code.

        # Checks if the password is longer than eight characters.
        if ( len(password) <= 8 ): 
            msg += "Password must be about 8 characters. \n"
            valid = False
            
        # Checks the contents of the password
        upper = 0 # counter for the number of upper case letters in the password
        digit = 0 # counter for number of digits in the password
        special = 0 # counter for number of special characters in the password
        alpha = 0 # counter for the number of alphabetical letters in the password
        
        special_characters = "!@#$%^&*();:<>,./?'[]\}{-_+=`~"
       
        for x in password:
           # print(x)
            if (x.isupper() == True):
                upper+=1
                # print("| Upper.")
            if (x.isdigit() == True):
                digit+=1
                # print(x + "| Digit")
            if (x.isalpha() == True):
                alpha+=1
                # print(x+ "| Alphabetical")
            for i in special_characters:
                if (x == i):
                    special += 1
                   # print(x+ "|Special")
                
        if upper == 0:
            msg += "Password needs at least ONE uppercase letter. \n"
            valid = False
        if digit == 0:
            msg += "Password must have at least ONE digit. \n"
            valid = False
        if special == 0:
            msg += "Password must have at least ONE special character.\n"
            valid = False
        if alpha == 0:
            msg += "Password must have at least alphabetical character.\n"
            valid = False            

        # final return statement
        # msg containing what requires are required for the password or username.
        return msg, valid

    def myLogPal(self, username, password):
        return msg, valid

class MyCalcPal():
    def __init__(self):
        self._hashlog = "" # the hash code 
        self._food = "" # what food was consumed
        self._calories = 0 # number of calories
        self._quantity = 1 # number of the food consumed

    # constructor function
    def MyCalcPal(self, hashlog, quantity, calories, food):
        self._quantity = quantity 
        self._carlories = calories
        self._hash = hashlog
        self._food = food 

    # getters
    # gets calories and quantities
    def get_calories(self):
        return self._calories
    def get_quantity(self):
        return self._quantity
    def get_hashlog(hashlog):
        return self._hashlog
    def get_food(food):
        return self._food
    
    # setters
    # sets calories and quantities
    def set_calories(self, calories):
        self._calories = calories
    def set_quantity(self, quantity):
        self._quantity = quantity        
    def set_calories(self, hashlog):
        self._hashlog = hashlog
    def set_quantity(self, food):
        self.food = food        
    
    # 
    
    def myAddPal(self, quantity, calories):
        return t_calories # represents total calories
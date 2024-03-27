import MyDatabasePal as mydbp
import time 

class MyCalPal:
    def __init__(self):
        self._username = ""
        self._password = ""
        self.msg = ""
        self.valid = True

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

    def myValidPal(self, username, password):
        msg = ""
        valid = True 
        
        username, password = username.strip(), password.strip()
        
        for x in username:
            if x == " ":
                msg += "User has unnecessary spaces.\n"
                valid = False

        if len(username) < 3: 
            msg += "Username is not longer than three characters.\n"
            valid = False 
            
        if username == password:
            msg += "Username cannot be equal to password! \n"
            valid = False

        for x in password:
            if x == " ":
                msg += "Password has unnecessary spaces.\n"
                valid = False
        password = password.replace(" ", "")

        if len(password) <= 8: 
            msg += "Password must be at least 8 characters long. \n"
            valid = False
            
        special_characters = "!@#$%^&*();:<>,.//?'[]\\}{-_+=`~"
        checks = [any(char.isupper() for char in password),
                  any(char.isdigit() for char in password),
                  any(char in special_characters for char in password),
                  any(char.isalpha() for char in password)]
        
        for check, desc in zip(checks, ["uppercase letter", "digit", "special character", "alphabetical letter"]):
            if not check:
                msg += f"Password must have at least one {desc}.\n"
                valid = False

        self.msg = msg
        self.valid = valid
        return msg, valid

    def myLogPal(self, username, password):
        return self.msg, self.valid

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
    
    # 
    def myAddPal(self, quantity, calories):
        t_calories = self._calories + calories
        return t_calories

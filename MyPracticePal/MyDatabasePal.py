# MyDatabasePal.py

import urllib.parse
from pymongo import MongoClient

# MongoDB connection string with properly escaped username and password
username = "eij"
password = "c@lori3"
cluster_url = "cluster0.ydug9w5.mongodb.net"
url = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@{cluster_url}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(url)
db = client['MyCalPal']

loginInfo = db['Credentials']

def createAccount(email, username, password):
    return loginInfo.insert_one(
        {'email': f'{email}', 'username': f'{username}', 'password':f'{hashlib.sha256(password.encode())}'})
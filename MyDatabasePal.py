"""
"""
#Imports the database for MongoDB.

"""
import MyClassPal;

from pymongo import MongoClient

# Connect to MongoDB
#client = MongoClient("mongodb+srv://cluster0.ydug9w5.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient('mongodb://localhost:27017/')

# Access a database
db = client['MyCalPal']

# Access a collection
collection = db['item']

# Insert a document
result = collection.insert_one({'name': 'Orange', 'calories': 90})
print(result)

# Close the connection
client.close()
"""
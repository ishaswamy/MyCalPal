



from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Access a database
db = client['MyCalPal']

# Access a collection
collection = db['item']

# Insert a document
result = collection.insert_one({'name': 'Cookie', 'calories': 340})

# Close the connection
client.close()


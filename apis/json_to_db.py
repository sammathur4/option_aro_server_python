

import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["OPTIONARO"]
collection = db["lastquoteoptiongreekschain_historic"]

# Load JSON data from file
with open("lastquoteoptiongreekschain_historic.json") as file:
    data = json.load(file)

# Insert JSON data into MongoDB
collection.insert_many(data)

# Close the MongoDB connection
client.close()

import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/')
db = client['OPTIONARO']
collection = db['lastquoteoptiongreekschain_realtime']

# Open and read the JSON file
with open('OPTIONARO.lastquoteoptiongreekschain_realtime.json', 'r') as file:
    json_data = json.load(file)

# Insert the JSON data into the collection
collection.insert_many(json_data)

print("JSON data inserted successfully.")

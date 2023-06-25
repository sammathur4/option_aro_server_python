import json
from pymongo import MongoClient

# Connect to MongoDB
# client = MongoClient('mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/')
client = MongoClient('mongodb://localhost:27017/')
db = client['OPTIONARO']
# collection = db['lastquoteoptiongreekschain_realtime']

new_lastquoteoptiongreekschain_historic_db = db['new_lastquoteoptiongreekschain_historic_db']

# # Open and read the JSON file
# with open('new_lastquoteoptiongreekschain_historic_db.json', 'r') as file:
#     json_data = json.load(file)
#
# # Insert the JSON data into the collection
# new_lastquoteoptiongreekschain_historic_db.insert_many(json_data)
#
# print("JSON data inserted successfully.")


# Define the projection to exclude the _id field
projection = {"_id": 0, "updated_at":0}

# Retrieve all data without the _id field
data = new_lastquoteoptiongreekschain_historic_db.find({}, projection)

# Define a list to store the documents
documents = []

# Iterate over the query results and store the documents
for document in data:
    documents.append(document)

# Write the documents to a JSON file
with open("new_lastquoteoptiongreekschain_historic_db.json", "w") as file:
    json.dump(documents, file, indent=4)
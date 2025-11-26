from pymongo import MongoClient
import sys
import json

if len(sys.argv) != 3:
    print("Please run like this format: python3 load-json.py <input_json_file> <port_number>")
    sys.exit(1)

input_json_file = sys.argv[1]

port_number = int(sys.argv[2])

# Creating connection
client = MongoClient(f"mongodb://localhost:{port_number}/" )
db = client["291db"]
# Getting database name 291db

db.articles.drop()
# Removing collection 'articles' if any

collection = db["articles"]
# Creates 'articles' collection

batches = []
batch_size = 2000 

# reading input file and adding it to batches
with open(input_json_file, "r") as f:
    for line in f:
        doc = json.loads(line)
        batches.append(doc)

        if len(batches) >= batch_size:
            collection.insert_many(batches)
            batches.clear() # Reseting batch to avoid duplicating

# Inserting left over documents
if batches:
    collection.insert_many(batches)

# Close connection
client.close()
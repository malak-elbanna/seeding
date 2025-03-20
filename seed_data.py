import json
from pymongo import MongoClient

def seed_data(cleaned_json_path, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    with open(cleaned_json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print("data has been successfully seeded to mongo")

if __name__ == "__main__":
    seed_data("D:/year 3/s2/seeding/cleaned_data.json", "tabaani", "seeding")

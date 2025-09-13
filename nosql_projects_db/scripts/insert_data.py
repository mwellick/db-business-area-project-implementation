import os
import json

from nosql_projects_db.engine.init_db import init_db

db = init_db()


def insert_collection(collection_name, filename):
    global db
    curr_dir = os.path.dirname(__file__)
    file_path = os.path.join(curr_dir, "..", "collections", filename)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    db[collection_name].insert_many(data)
    print(f"Inserted {collection_name} into MongoDB")

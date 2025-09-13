import os
import json

from nosql_projects_db.engine.init_db import init_db
from nosql_projects_db.scripts.constraints import can_order_project

db = init_db()


def filter_data(data):
    filtered_data = []
    for project in data:
        customer_name = project.get("customer")
        if can_order_project(db, customer_name):
            filtered_data.append(project)
        else:
            print(f"This customer: {customer_name} can't order a new project: "
                  f"{project.get('name')}, because he has unpaid one ")
    data = filtered_data
    return data


def insert_collection(collection_name, filename):
    global db
    curr_dir = os.path.dirname(__file__)
    file_path = os.path.join(curr_dir, "..", "collections", filename)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if collection_name == "projects":
        data = filter_data(data)
    if data:
        db[collection_name].insert_many(data)
        print(f"Inserted {collection_name} into MongoDB")

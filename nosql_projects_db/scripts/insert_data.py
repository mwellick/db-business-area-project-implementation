import os
import json

from nosql_projects_db.engine.init_db import init_db
from nosql_projects_db.scripts.constraints import can_order_project, can_report

db = init_db()


def filter_projects(data):
    """
    This  helper function helps to filter and trigger can_order_project constraint to find
    customer who has fine and didn't pay in past 90 days
    """
    filtered_data = []
    for project in data:
        customer_name = project.get("customer")
        if can_order_project(db, customer_name):
            filtered_data.append(project)
        else:
            print(f"This customer: {customer_name} can't order a new project: "
                  f"{project.get('name')}, because he has unpaid one ")

    return filtered_data


def filter_reports(data):
    """
    The same logic as in an above  helper func:
    Filters and trigger can_report constraint
    """

    filtered_data = []
    for report in data:
        executor_id = report.get("executor_id")
        date = report.get("date")
        hours = report.get("hours")
        if can_report(db, executor_id, date, hours):
            filtered_data.append(report)
        else:
            print(f"Can't report more than 10 hours per day for executor: {executor_id}")

    return filtered_data


def insert_collection(collection_name, filename):
    curr_dir = os.path.dirname(__file__)
    file_path = os.path.join(curr_dir, "..", "collections", filename)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if collection_name == "projects":
        data = filter_projects(data)

    if collection_name == "reports":
        data = filter_reports(data)

    if data:
        db[collection_name].insert_many(data)
        print(f"Inserted {collection_name} into MongoDB")

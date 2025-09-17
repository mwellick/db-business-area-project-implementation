import os
import json
from nosql_projects_db.engine.init_db import init_db
from nosql_projects_db.scripts.insert_data import insert_collection
from nosql_projects_db.scripts.calculate_salary import calculate_monthly_salary
from nosql_projects_db.reports.report_projects import project_report
from nosql_projects_db.reports.report_salaries import salaries_report
from nosql_projects_db.reports.report_project_status_monthly import project_status_report

curr_dir = os.path.dirname(__file__)
file_path = os.path.join(curr_dir, "nosql_projects_db", "collections", "reports.json")


def insert_data(db):
    insert_collection(db, "projects", "projects.json")
    insert_collection(db, "executors", "executors.json")
    insert_collection(db, "payments", "payments.json")
    print("All data inserted successfully\n")
    print("*" * 100)


def calc_monthly_salary(db, report_data, year: int, month: int):
    salaries = calculate_monthly_salary(db, year, month, report_data)
    print(json.dumps(salaries, indent=2))


def make_reports(db, reports_data):
    proj_report = project_report(db, reports_data)
    print("PROJECTS REPORT\n")
    print(json.dumps(proj_report, indent=1))
    print("-" * 100)
    sal_report = salaries_report(db, reports_data, 2025, 9)
    print("SALARIES REPORT\n")
    print(json.dumps(sal_report, indent=1))
    print("-" * 100)
    proj_status_monthly = project_status_report(db, reports_data, 1, 2025, 9)
    print("PROJECT MONTHLY STATUS  REPORT\n")
    print(json.dumps(proj_status_monthly, indent=1))
    print("-" * 100)


if __name__ == "__main__":
    db = init_db()
    insert_data(db)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    make_reports(db, data)
    # calc_monthly_salary(db, data, 2025, 9)  # Optional

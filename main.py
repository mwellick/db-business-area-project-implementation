import json
from nosql_projects_db.engine.init_db import init_db
from nosql_projects_db.scripts.insert_data import insert_collection
from nosql_projects_db.scripts.calculate_salary import calculate_monthly_salary
from nosql_projects_db.reports.report_projects import project_report
from nosql_projects_db.reports.report_salaries import salaries_report
from nosql_projects_db.reports.report_project_status_montly import project_status_report


def insert_data():
    insert_collection("projects", "projects.json")
    insert_collection("executors", "executors.json")
    insert_collection("reports", "reports.json")
    insert_collection("payments", "payments.json")
    print("All data inserted successfully\n")
    print("*" * 100)


def calc_monthly_salary(db, year: int, month: int):
    salaries = calculate_monthly_salary(init_db(), 2025, 9)
    print(json.dumps(salaries, indent=2))


def make_reports(db):
    proj_report = project_report(db)
    print("PROJECTS REPORT\n")
    print(json.dumps(proj_report, indent=2))
    print("-" * 100)
    sal_report = salaries_report(init_db(), 2025, 9)
    print("SALARIES REPORT\n")
    print(json.dumps(sal_report, indent=2))
    print("-" * 100)
    proj_status_monthly = project_status_report(init_db(), 1, 2025, 9)
    print("PROJECT MONTHLY STATUS  REPORT\n")
    print(json.dumps(proj_status_monthly, indent=2))
    print("-" * 100)


if __name__ == "__main__":
    db = init_db()
    insert_data()
    make_reports(db)
#   calc_monthly_salary(db, 2025, 9)  # Optional

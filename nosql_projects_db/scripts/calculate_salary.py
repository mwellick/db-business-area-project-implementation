from datetime import datetime


def calculate_monthly_salary(db, year, month):
    """
    This function calculates salaries only for those executors
    - which projects have been paid from customers on selected month
    """

    salaries = []
    executors = list(db.executors.find())

    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    for executor in executors:
        executor_id = executor.get("id")
        hourly_rate = executor.get("hourly_rate")
        position_coef = executor.get("position_coef")

        reports = list(
            db.reports.find(
                {
                    "executor_id": executor_id,
                    "date": {
                        "$gte": start_date.isoformat(),
                        "$lte": end_date.isoformat()
                    }
                }
            )
        )
        paid_reports = []
        for report in reports:
            project_id = report.get("project_id")
            payment = db.payments.find_one(
                {
                    "project_id": project_id,
                    "paid": True
                }
            )
            if payment:
                paid_reports.append(report)

        total_hours = sum(report.get("hours", 0) for report in paid_reports)
        primary_salary = total_hours * hourly_rate * position_coef
        overhead = round(primary_salary * 0.4, 2)
        total_salary = primary_salary + overhead

        if total_salary:
            salaries.append(
                {
                    "executor_id": executor_id,
                    "name": executor.get("name"),
                    "month": month,
                    "total_hours": total_hours,
                    "primary_salary": primary_salary,
                    "overhead": overhead,
                    "total_salary": total_salary
                }
            )

    return salaries

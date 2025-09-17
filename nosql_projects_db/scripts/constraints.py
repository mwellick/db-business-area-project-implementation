from datetime import datetime, timedelta


def can_order_project(db, customer_name):
    """
    Small explanation how it works:
    This constraint will work only and if DB already has data to compare.
    If DB is empty - all data will be inserted,because constraint still don't have data to compare yet.
    """

    three_months = (datetime.now() - timedelta(days=90)).isoformat()

    projects = db.projects.aggregate(
        [
            {"$match": {"customer": customer_name}},
            {
                "$lookup": {
                    "from": "payments",
                    "localField": "id",
                    "foreignField": "project_id",
                    "as": "payments"
                }},
            {"$unwind": "$payments"},
            {"$match": {
                "payments.paid": False,
                "payments.payment_date": {"$lte": three_months}
            }}
        ]
    )

    return len(list(projects)) == 0


def can_report(report_data, executor_id, report_date, next_report_hours):
    """
    The same logic as in an above constraint docstring
    If DS's empty - may be added any report (according to time)
    """
    total_hours = sum(
        r.get("hours", 0) for r in report_data
        if r.get("executor_id") == executor_id and r.get("date") == report_date
    )
    return total_hours + next_report_hours <= 10


def filter_reports(db, data):
    """
    Filters data and trigger can_report constraint
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

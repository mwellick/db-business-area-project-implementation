from datetime import datetime


def project_status_report(db, project_id: int, year: int, month: int):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    reports = db.reports.find(
        {
            "project_id": project_id,
            "date": {
                "$gte": start_date.isoformat(),
                "$lte": end_date.isoformat()
            }
        }
    )
    # This block is made for easily reformation  into json format &
    # better readability
    results = []

    for report in reports:
        executor = db.executors.find_one(
            {
                "id": report.get("executor_id")
            }
        )
        results.append(
            {"executor_name": executor.get("name"),
             "date": report.get("date"),
             "hours": report.get("hours"),
             "work_description": report.get("task")
             }
        )

    return results

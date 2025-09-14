from nosql_projects_db.scripts.calculate_salary import calculate_monthly_salary


def salaries_report(db, year: int, month: int):
    salaries = calculate_monthly_salary(db, year, month)
    reports = {}

    for salary in salaries:
        executor = db.executors.find_one(
            {"id": salary.get("executor_id")}
        )
        position = executor.get("position")

        if position not in reports:
            reports[position] = []

        reports[position].append(
            {
                "name": salary.get("name"),
                "total_hours": salary.get("total_hours"),
                "primary_salary": salary.get("primary_salary"),
                "overhead": salary.get("overhead"),
                "total_salary": salary.get("total_salary")
            }
        )
    # This block is made for easily reformation  into json format &
    # better readability
    results = []

    for k, v in reports.items():
        results.append(
            {
                "position": k,
                "executors": v
            }
        )

    return results

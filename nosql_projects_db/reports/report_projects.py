from collections import defaultdict


def project_report(db, reports_data):
    projects = list(db.projects.find())
    payments = list(db.payments.find())

    payments_by_projects = defaultdict(list)

    for p in payments:
        payments_by_projects[p["project_id"]].append(p)

    reports_by_project = defaultdict(list)
    for r in reports_data:
        reports_by_project[r["project_id"]].append(r)

    categories = defaultdict(list)

    for project in projects:
        project_id = project.get("id")
        category = project.get("category")

        total_hours = sum(r.get("hours") for r in reports_by_project[project_id])
        total_amount = sum(p.get("total_amount") for p in payments_by_projects[project_id])

        categories[category].append(
            {
                "name": project.get("name"),
                "total_hours": total_hours,
                "total_amount": total_amount
            }
        )

    # This block is made for easily reformation  into json format &
    # better readability
    results = []

    for category, project in categories.items():
        results.append(
            {
                "category": category,
                "projects": project
            }
        )

    return results

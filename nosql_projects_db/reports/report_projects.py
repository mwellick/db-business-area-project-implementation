def project_report(db):
    pipeline = [
        {
            "$lookup": {
                "from": "payments",
                "localField": "id",
                "foreignField": "project_id",
                "as": "payments",
            }
        },
        {
            "$lookup": {
                "from": "reports",
                "localField": "id",
                "foreignField": "project_id",
                "as": "reports"
            }
        },
        {
            "$addFields": {
                "total_hours": {
                    "$sum": "$reports.hours"
                },
                "total_amount": {
                    "$sum": "$payments.total_amount"
                }
            }
        },
        {
            "$group": {
                "_id": "$category",
                "projects": {
                    "$push": {
                        "name": "$name",
                        "total_hours": "$total_hours",
                        "total_amount": "$total_amount"
                    }
                }
            }
        }
    ]
    res_data = list(db.projects.aggregate(pipeline))
    # This block is made for easily reformation  into json format &
    # better readability
    results = []

    for data in res_data:
        results.append(
            {
                "category": data.get("_id"),
                "projects": data.get("projects")
            }
        )

    return results

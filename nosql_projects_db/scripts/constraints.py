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

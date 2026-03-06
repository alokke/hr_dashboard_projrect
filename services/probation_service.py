from services.sap_service import call_sap_service
from database import get_connection
from datetime import datetime, timedelta

def fetch_and_store_probation(emp_id):

    today = datetime.today().date()

    # 1️⃣ Check Confirmation in PA0000
    pa0000 = call_sap_service("pa0000", emp_id)

    if isinstance(pa0000, dict):
        records = pa0000.get("data", [])
    elif isinstance(pa0000, list):
        records = pa0000
    else:
        records = []

    for record in records:
        if isinstance(record, dict):
            if record.get("MASSN") in ["CONF", "03", "ZCONF"]:
                confirmation_date = record.get("BEGDA")
                return {
                    "emp_id": emp_id,
                    "probation_status": "Completed",
                    "confirmation_date": confirmation_date,
                    "source": "PA0000 Action"
                }

    # 2️⃣ Check PA0041 (Date Specifications)
    pa0041 = call_sap_service("pa0041", emp_id)

    if isinstance(pa0041, dict):
        records_41 = pa0041.get("data", [])
    elif isinstance(pa0041, list):
        records_41 = pa0041
    else:
        records_41 = []

    for record in records_41:
        if isinstance(record, dict):
            # Example: change to your probation date type
            probation_end = record.get("DAT02")

            if probation_end:
                probation_end_date = datetime.strptime(probation_end, "%Y-%m-%d").date()

                if today >= probation_end_date:
                    return {
                        "emp_id": emp_id,
                        "probation_status": "Completed",
                        "confirmation_date": probation_end,
                        "source": "PA0041 Date"
                    }
                else:
                    return {
                        "emp_id": emp_id,
                        "probation_status": "Under Probation",
                        "confirmation_date": probation_end,
                        "source": "PA0041 Date"
                    }

    # 3️⃣ Fallback → Calculate from DOJ
    pa0002 = call_sap_service("pa0002", emp_id)

    if isinstance(pa0002, dict):
        records_02 = pa0002.get("data", [])
    elif isinstance(pa0002, list):
        records_02 = pa0002
    else:
        records_02 = []

    for record in records_02:
        if isinstance(record, dict):
            doj = record.get("BEGDA")

            if doj:
                doj_date = datetime.strptime(doj, "%Y-%m-%d").date()
                probation_end = doj_date + timedelta(days=365*2)

                if today >= probation_end:
                    return {
                        "emp_id": emp_id,
                        "probation_status": "Completed",
                        "confirmation_date": probation_end,
                        "source": "Calculated (DOJ + 2 Years)"
                    }
                else:
                    return {
                        "emp_id": emp_id,
                        "probation_status": "Under Probation",
                        "confirmation_date": probation_end,
                        "source": "Calculated (DOJ + 2 Years)"
                    }

    return {
        "emp_id": emp_id,
        "probation_status": "No Data Found",
        "confirmation_date": None,
        "source": "None"
    }
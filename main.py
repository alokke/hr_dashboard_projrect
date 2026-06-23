from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from database import save_probation

app = FastAPI()
templates = Jinja2Templates(directory="templates")
BASE_URL = "http://10.48.49.107:8080/SAP-SERVICE/hr"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("probation.html", {"request": request})
@app.get("/probation/{emp_id}")
def get_probation(emp_id: str):

    try:
        response = requests.post(
            f"{BASE_URL}/pa0000",
            json={"empId": emp_id},
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        data = response.json()
        records = data.get("pa0000DetailsList", [])

        confirmation_date = None
        sap_action_type = None

        for record in records:
            if record.get("massn") in ["03", "05"]:
                confirmation_date = record.get("begda")
                sap_action_type = record.get("massn")

        if confirmation_date:
            probation_status = "Completed"
        else:
            probation_status = "Pending"

        # ✅ SAVE TO DATABASE (ADD THIS LINE)
        save_probation(emp_id, probation_status, confirmation_date, sap_action_type)

        # Return to frontend
        if confirmation_date:
            return {
                "probation_status": probation_status,
                "confirmation_date": confirmation_date
            }
        else:
            return {
                "status": probation_status
            }

    except Exception as e:
        return {"status": "Server Error"}

#Alok#
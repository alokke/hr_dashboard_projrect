import requests

BASE_URL = "http://10.48.49.107:8080/SAP-SERVICE/hr"

headers = {
    "Content-Type": "application/json"
}

def call_sap_service(infotype, emp_id):
    try:
        url = f"{BASE_URL}/{infotype}"

        response = requests.post(
            url,
            json={"empId": emp_id},
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            try:
                return response.json()
            except:
                return response.text
        else:
            return {"error": response.text}

    except Exception as e:
        return {"error": str(e)}
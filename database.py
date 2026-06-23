import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hr_dashboard"
    )
def save_probation(emp_id, probation_status, confirmation_date, sap_action_type):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO employee_probation
    (emp_id, confirmation_date, probation_status, sap_action_type)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        confirmation_date = %s,
        probation_status = %s,
        sap_action_type = %s
    """

    cursor.execute(
        query,
        (
            emp_id, confirmation_date, probation_status, sap_action_type,
            confirmation_date, probation_status, sap_action_type
        )
    )

    conn.commit()
    cursor.close()
    conn.close()
    
#Alok123#
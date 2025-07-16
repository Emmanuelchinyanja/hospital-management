import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital-management"
    )

def log_action(user, department, action):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (user, department, action) VALUES (%s, %s, %s)",
        (user, department, action)
    )
    conn.commit()
    conn.close()
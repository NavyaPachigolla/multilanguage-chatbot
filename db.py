import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="chatbot_db",
        port=3306
    )
    return conn
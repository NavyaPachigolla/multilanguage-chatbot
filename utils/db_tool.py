import mysql.connector


def get_student(name):

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="student_db",
        port=3306
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE name=%s",
        (name,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result
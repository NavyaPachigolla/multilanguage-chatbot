print("🚀 START")

import mysql.connector

print("✅ IMPORTED MYSQL")

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        port=3306,
        connection_timeout=5
    )

    print("✅ CONNECTED")

    conn.close()

    print("🔒 CLOSED")

except Exception as e:
    print("❌ ERROR:")
    print(e)

print("🏁 END")
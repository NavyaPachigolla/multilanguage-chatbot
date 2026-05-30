from db import get_connection

print("🚀 Testing DB...")

conn = get_connection()

if conn.is_connected():
    print("✅ DB CONNECTED SUCCESSFULLY!")

conn.close()

print("🔒 CLOSED")
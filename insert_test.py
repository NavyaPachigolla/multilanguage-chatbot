from db import get_connection

conn = get_connection()
cursor = conn.cursor()

query = """
INSERT INTO chat_history
(user_message, bot_response, language)
VALUES (%s, %s, %s)
"""

values = (
    "Hello",
    "Hi! How can I help you?",
    "English"
)

cursor.execute(query, values)

conn.commit()

print("✅ Data inserted!")

cursor.close()
conn.close()
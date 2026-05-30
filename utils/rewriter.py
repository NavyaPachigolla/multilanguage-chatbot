from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")


def rewrite_query(query: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Rewrite the query for better document retrieval. Keep meaning same, make it clear and search-friendly."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception:
        return query
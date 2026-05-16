from groq import Groq

import os

from dotenv import load_dotenv


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


SYSTEM_PROMPT = """
You are an intelligent multilingual AI assistant.

Answer ONLY from the provided context.

Rules:

1. Do not hallucinate.

2. If information is unavailable, say:
'The uploaded documents do not contain this information.'

3. Always include source citations.

4. Mention document name and page number.

5. Keep answers concise and accurate.

6. Support multilingual users.
"""


def generate_answer(question, retriever):

    # NEW LANGCHAIN METHOD
    docs = retriever.invoke(question)

    context = ""

    for doc in docs:
        context += doc.page_content + "\n"


    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    answer = response.choices[0].message.content

    return answer, docs
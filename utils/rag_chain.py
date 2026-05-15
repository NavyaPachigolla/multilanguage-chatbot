import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from utils.retriever import get_retriever


# Load environment variables
load_dotenv()


def get_llm():

    groq_api_key = os.getenv("GROQ_API_KEY")

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant"
    )

    return llm


def generate_answer(question):

    # Load retriever
    retriever = get_retriever()

    # Retrieve top relevant chunks
    docs = retriever.invoke(question)

    # Combine retrieved text
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Prompt
    prompt = f"""
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

Context:
{context}

Question:
{question}

Answer:
"""

    # Load LLM
    llm = get_llm()

    # Generate response
    response = llm.invoke(prompt)

    return response.content, docs
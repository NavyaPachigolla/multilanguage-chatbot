from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()


# ===============================
# SYSTEM PROMPT
# ===============================

PROMPT_TEMPLATE = """

You are an intelligent multilingual AI assistant.

Answer ONLY from the provided context.

Rules:

1. Do not hallucinate.

2. If information is unavailable, say:
'The uploaded documents do not contain this information.'

3. Always include concise answers.

4. Support multilingual users.

5. Use previous conversation if relevant.


Conversation History:
{chat_history}


Context:
{context}


Question:
{question}


Answer:

"""


# ===============================
# GENERATE ANSWER
# ===============================

def generate_answer(

    question,

    retriever,

    chat_history=""
):

    # RETRIEVE DOCUMENTS

    docs = retriever.invoke(
        question
    )
    # COMBINE CONTEXT

    context = "\n\n".join([

        doc.page_content

        for doc in docs
    ])

    # PROMPT

    prompt = PromptTemplate(

        template=PROMPT_TEMPLATE,

        input_variables=[
            "context",
            "question",
            "chat_history"
        ]
    )

    final_prompt = prompt.format(

        context=context,

        question=question,

        chat_history=chat_history
    )

    # LLM

    llm = ChatGroq(

        model="llama-3.3-70b-versatile",

        temperature=0
    )

    # GENERATE RESPONSE

    response = llm.invoke(
        final_prompt
    )

    answer = response.content

    return answer, docs
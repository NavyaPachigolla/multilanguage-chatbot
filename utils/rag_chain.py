from utils.llm_factory import GroqLLM

# ================= STRICT RAG PROMPT =================

SYSTEM_PROMPT = """
You are a STRICT RAG-based AI assistant.

RULES:
1. Answer ONLY using the provided context.
2. If answer is not in context, say:
   "The uploaded documents do not contain this information."
3. Do NOT use outside knowledge.
4. Be concise and accurate.
5. Always include source if available (file name + page).
"""


# ================= LLM INSTANCE =================

llm = GroqLLM()


# ================= MAIN FUNCTION =================

def generate_answer(question, retriever):

    try:

        # ================= RETRIEVE =================

        docs = retriever.invoke(question)

        if not docs:
            return "The uploaded documents do not contain this information.", []


        # ================= REMOVE DUPLICATES =================

        seen = set()
        unique_docs = []

        for d in docs:

            key = (
                d.metadata.get("source", "Unknown"),
                d.metadata.get("page", "Unknown")
            )

            if key not in seen:
                seen.add(key)
                unique_docs.append(d)

        docs = unique_docs


        # ================= BUILD CONTEXT =================

        context = "\n\n".join(

            f"[Source: {d.metadata.get('source','Unknown')} | "
            f"Page: {d.metadata.get('page','?')}]\n"
            f"{d.page_content}"

            for d in docs
        )


        # ================= FINAL PROMPT =================

        final_prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


        # ================= LLM MESSAGES =================

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": final_prompt
            }
        ]


        # ================= GENERATE =================

        answer = llm.generate(messages)

        return answer, docs


    except Exception as e:

        print("RAG Error:", e)

        return (
            "The uploaded documents do not contain this information.",
            []
        )
def generate_web_answer(question, web_context):

    try:

        prompt = f"""
You are a helpful AI assistant.

Answer the question using the web search results.

Keep the answer:
- Short
- Accurate
- Direct

QUESTION:
{question}

WEB RESULTS:
{web_context}

ANSWER:
"""

        messages = [
            {
                "role": "system",
                "content": "Answer using the web search results."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        answer = llm.generate(messages)

        return answer

    except Exception as e:

        print("Web Error:", e)

        return "Unable to generate web answer."
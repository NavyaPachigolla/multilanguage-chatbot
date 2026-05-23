import streamlit as st

from utils.pdf_loader import load_pdfs
from utils.embeddings import split_documents, create_vectorstore
from utils.rag_chain import generate_answer

from utils.translator import (
    detect_language,
    translate_to_english,
    translate_answer
)

from utils.rewriter import rewrite_query

from db import get_connection
def save_chat(user_msg, bot_msg, language):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO chat_history
    (user_message, bot_response, language)
    VALUES (%s, %s, %s)
    """

    values = (user_msg, bot_msg, language)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Multilingual Multi-Document AI Chatbot",
    layout="wide"
)

st.title("📚 Multilingual Multi-Document AI Chatbot")

st.markdown("""
### 🌍 Supported Languages
- English
- Telugu
- Hindi
- Tamil
- Other Indian Languages
""")


# ================= SESSION STATE =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None


# ================= SIDEBAR =================
st.sidebar.header("📂 Upload PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()


# ================= PROCESS PDFs =================
if uploaded_files and st.session_state.retriever is None:

    with st.spinner("Processing PDFs..."):

        documents = load_pdfs(uploaded_files)

        if not documents:
            st.error("❌ No text extracted from PDFs.")
            st.stop()

        chunks = split_documents(documents)

        if not chunks:
            st.error("❌ No chunks generated.")
            st.stop()

        vectorstore = create_vectorstore(chunks)

        st.session_state.retriever = vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )

        st.success("✅ PDFs processed successfully!")


# ================= CHAT SECTION =================
if st.session_state.retriever is not None:

    retriever = st.session_state.retriever

    # show history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])

    # input box
    user_question = st.chat_input("Ask questions from your documents...")

    if user_question:

        with st.chat_message("user"):
            st.write(user_question)

        with st.spinner("Thinking..."):

            try:
                # 1. Detect language
                user_language = detect_language(user_question)

                # 2. Translate to English
                english_question = translate_to_english(user_question)

                # 3. Rewrite query (IMPORTANT FOR RETRIEVAL)
                rewritten_question = rewrite_query(english_question)

                # 4. Generate answer (RAG)
                answer, docs = generate_answer(rewritten_question, retriever)

                # 5. Translate back
                if user_language == "en":
                    final_answer = answer
                else:
                    final_answer = translate_answer(answer, user_language)

                # 6. Sources
                sources = "\n\n📄 Sources:\n"
                for d in docs:
                    sources += (
                        f"\n📌 {d.metadata.get('source','Unknown')} "
                        f"- Page {d.metadata.get('page','?')}"
                    )

                final_output = final_answer + sources
                save_chat(user_question, final_output, user_language)

                # show answer
                with st.chat_message("assistant"):
                    st.write(final_output)

                # save history
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": final_output
                })

            except Exception as e:
                st.error(f"Error generating answer: {e}")


else:
    st.info("📂 Please upload PDF documents to begin.")
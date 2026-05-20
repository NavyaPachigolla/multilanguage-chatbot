import streamlit as st

from utils.pdf_loader import load_pdfs

from utils.embeddings import (
    split_documents,
    create_vectorstore,
    load_vectorstore
)

from utils.rag_chain import generate_answer

from utils.translator import (
    detect_language,
    translate_to_english,
    translate_answer
)

from utils.ragas_eval import (
    run_ragas_evaluation
)


# ================= PAGE CONFIG =================

st.set_page_config(

    page_title="Multilingual Multi-Document AI Chatbot",

    layout="wide"
)


# ================= TITLE =================

st.title(
    "📚 Multilingual Multi-Document AI Chatbot"
)

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

st.sidebar.header("📂 Upload PDF Files")

uploaded_files = st.sidebar.file_uploader(

    "Upload one or more PDFs",

    type=["pdf"],

    accept_multiple_files=True
)


# ================= CLEAR CHAT =================

if st.sidebar.button("🗑 Clear Chat"):

    st.session_state.chat_history = []

    st.rerun()


# ================= PROCESS PDFs =================

if uploaded_files and st.session_state.retriever is None:

    with st.spinner("Processing PDFs..."):

        try:

            # LOAD PDFs

            documents = load_pdfs(
                uploaded_files
            )

            if not documents:

                st.error(
                    "❌ No text extracted from PDFs."
                )

                st.stop()


            # SPLIT DOCUMENTS

            chunks = split_documents(
                documents
            )

            if not chunks:

                st.error(
                    "❌ No chunks generated."
                )

                st.stop()


            # ================= VECTORSTORE =================

            existing_vectorstore = load_vectorstore()

            if existing_vectorstore is not None:

                vectorstore = existing_vectorstore

            else:

                vectorstore = create_vectorstore(
                    chunks
                )


            # ================= RETRIEVER =================

            retriever = vectorstore.as_retriever(

                search_kwargs={"k": 3}
            )

            st.session_state.retriever = retriever

            st.success(
                "✅ PDFs processed successfully!"
            )

        except Exception as e:

            st.error(
                f"Error processing PDFs: {e}"
            )

            st.stop()


# ================= MAIN APP =================

if st.session_state.retriever is not None:

    retriever = st.session_state.retriever


    # ================= SHOW CHAT HISTORY =================

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):

            st.write(chat["question"])


        with st.chat_message("assistant"):

            st.write(chat["answer"])


    # ================= CHAT INPUT =================

    user_question = st.chat_input(

        "Ask questions from uploaded documents..."
    )


    # ================= QUESTION PROCESSING =================

    if user_question:

        # SHOW USER QUESTION

        with st.chat_message("user"):

            st.write(user_question)


        with st.spinner("Generating answer..."):

            try:

                # ================= LANGUAGE DETECTION =================

                user_language = detect_language(
                    user_question
                )


                # ================= TRANSLATE TO ENGLISH =================

                english_question = (
                    translate_to_english(
                        user_question
                    )
                )


                # ================= CREATE CHAT MEMORY =================

                history_text = ""

                for chat in st.session_state.chat_history:

                    history_text += (

                        f"User: {chat['question']}\n"

                        f"Assistant: {chat['answer']}\n\n"
                    )


                # ================= GENERATE ANSWER =================

                answer, source_docs = generate_answer(

                    english_question,

                    retriever,

                    history_text
                )


                # ================= TRANSLATE BACK =================

                if user_language == "en":

                    final_answer = answer

                else:

                    final_answer = translate_answer(

                        answer,

                        user_language
                    )


                # ================= SOURCES =================

                source_text = "\n\n📄 Sources:\n"


                for doc in source_docs:

                    source = doc.metadata.get(

                        "source",

                        "Unknown"
                    )

                    page = doc.metadata.get(

                        "page",

                        "Unknown"
                    )

                    source_text += (

                        f"\n📌 {source}"
                        f" — Page {page}"
                    )


                # ================= FINAL RESPONSE =================

                final_response = (

                    final_answer
                    +
                    source_text
                )


                # ================= SHOW ANSWER =================

                with st.chat_message("assistant"):

                    st.write(final_response)


                # ================= SAVE CHAT HISTORY =================

                st.session_state.chat_history.append({

                    "question": user_question,

                    "answer": final_response

                })


            except Exception as e:

                st.error(
                    f"Error generating answer: {e}"
                )


    # ================= RAGAS EVALUATION =================

    st.divider()

    st.subheader(
        "📊 RAGAS Evaluation"
    )

    st.write(
        "Evaluate chatbot quality using RAGAS metrics."
    )


    if st.button(
        "🚀 Run RAGAS Evaluation"
    ):

        with st.spinner(
            "Running RAGAS Evaluation..."
        ):

            try:

                ragas_df, scores = (

                    run_ragas_evaluation(
                        retriever
                    )
                )

                st.success(
                    "✅ RAGAS Evaluation Completed"
                )


                # ================= DETAILED RESULTS =================

                st.subheader(
                    "📄 Detailed Results"
                )

                st.dataframe(
                    ragas_df
                )


                # ================= AVERAGE SCORES =================

                st.subheader(
                    "📈 Average Scores"
                )

                st.write(

                    f"Faithfulness: "
                    f"{scores['Faithfulness']}%"
                )

                st.write(

                    f"Answer Relevancy: "
                    f"{scores['Answer Relevancy']}%"
                )

                st.write(

                    f"Context Precision: "
                    f"{scores['Context Precision']}%"
                )

                st.write(

                    f"Context Recall: "
                    f"{scores['Context Recall']}%"
                )

            except Exception as e:

                st.error(
                    f"RAGAS Error: {e}"
                )


else:

    st.info(
        "📂 Please upload PDF documents to begin."
    )
import streamlit as st

from utils.pdf_loader import load_pdfs

from utils.embeddings import (
    split_documents,
    create_vectorstore
)

from utils.rag_chain import generate_answer

from utils.citation import format_sources

from utils.translator import (
    detect_language,
    translate_to_english,
    translate_answer
)

from utils.ragas_eval import evaluate_rag


# Page configuration
st.set_page_config(
    page_title="Multilingual AI Chatbot",
    layout="wide"
)

# Title
st.title("📚 Multilingual Multi-Document AI Chatbot")

st.info(
    "Supports English, Telugu, Hindi, Tamil and other Indian languages."
)

# Sidebar
st.sidebar.title("Upload PDF Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF Files",
    type="pdf",
    accept_multiple_files=True
)


# Process uploaded PDFs
if uploaded_files:

    with st.spinner("Processing PDFs..."):

        try:

            # Load PDFs
            documents = load_pdfs(uploaded_files)

            if not documents:
                st.error("No text could be extracted from PDFs.")
                st.stop()

            # Split documents into chunks
            chunks = split_documents(documents)

            if not chunks:
                st.error("No chunks generated from documents.")
                st.stop()

            # Create vectorstore
            create_vectorstore(chunks)

            st.success("Documents processed successfully!")

            st.write(f"Total Pages: {len(documents)}")

            st.write(f"Total Chunks: {len(chunks)}")

        except Exception as e:

            st.error(f"Error processing PDFs: {e}")

            st.stop()

    # User Question
    question = st.text_input(
        "Ask your question"
    )

    # Generate answer
    if question:

        with st.spinner("Generating answer..."):

            try:

                # Detect language
                user_language = detect_language(question)

                # Translate question to English
                english_question = translate_to_english(question)

                # Generate answer from RAG
                answer, source_docs = generate_answer(
                    english_question
                )

                # Translate answer back
                final_answer = translate_answer(
                    answer,
                    user_language
                )

                # Format citations
                sources = format_sources(source_docs)

                # RAGAS Evaluation
                evaluation_result = evaluate_rag(
                    english_question,
                    answer,
                    source_docs
                )

                # Display Answer
                st.subheader("Answer")

                st.write(final_answer)

                # Display Sources
                st.subheader("Sources")

                for source in sources:

                    st.write(f"- {source}")

                # Display RAGAS Scores
                st.subheader("RAGAS Evaluation Scores")

                st.write(evaluation_result)

            except Exception as e:

                st.error(f"Error generating answer: {e}")

else:

    st.info("Please upload PDF documents to begin.")
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


# Page config
st.set_page_config(
    page_title="Advanced Multilingual AI Chatbot",
    layout="wide"
)

# Title
st.title("🤖 Advanced Multilingual RAG Chatbot")

st.markdown(
    """
Supports:
- English
- Telugu
- Hindi
- Tamil
- Other Indian Languages
"""
)

# Initialize chat history
if "messages" not in st.session_state:

    st.session_state.messages = []


# Sidebar
st.sidebar.title("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF Files",
    type="pdf",
    accept_multiple_files=True
)

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# Process PDFs
if uploaded_files:

    with st.spinner("Processing PDFs..."):

        try:

            documents = load_pdfs(uploaded_files)

            if not documents:
                st.error("No text extracted from PDFs.")
                st.stop()

            chunks = split_documents(documents)

            if not chunks:
                st.error("No chunks generated.")
                st.stop()

            create_vectorstore(chunks)

            st.success("Documents processed successfully!")

            st.write(f"📄 Pages Loaded: {len(documents)}")

            st.write(f"🧩 Chunks Created: {len(chunks)}")

        except Exception as e:

            st.error(f"Error processing PDFs: {e}")

            st.stop()

    # Display old chat messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Chat input
    question = st.chat_input(
        "Ask a question from uploaded documents..."
    )

    # If user asks question
    if question:

        # Show user message
        st.chat_message("user").markdown(question)

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.spinner("Generating answer..."):

            try:

                # Detect language
                user_language = detect_language(question)

                # Translate to English
                english_question = translate_to_english(question)

                # Generate answer
                answer, source_docs = generate_answer(
                    english_question
                )

                # Translate answer back
                final_answer = translate_answer(
                    answer,
                    user_language
                )

                # Format sources
                sources = format_sources(source_docs)

                # RAG evaluation
                evaluation_result = evaluate_rag(
                    english_question,
                    answer,
                    source_docs
                )

                # Create final response
                full_response = final_answer

                full_response += "\n\n### 📚 Sources\n"

                for source in sources:

                    full_response += f"- {source}\n"

                full_response += "\n### 📊 Evaluation\n"

                full_response += f"""
- Retrieved Chunks: {evaluation_result['Retrieved Chunks']}
- Context Characters: {evaluation_result['Context Characters']}
"""

                # Display assistant message
                with st.chat_message("assistant"):

                    st.markdown(full_response)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": full_response
                    }
                )

            except Exception as e:

                st.error(f"Error generating answer: {e}")

else:

    st.info("📂 Upload PDF documents to start chatting.")
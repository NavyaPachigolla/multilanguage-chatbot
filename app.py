import streamlit as st
from graph.workflow import graph
from utils.pdf_loader import load_pdfs
from utils.embeddings import split_documents, create_vectorstore

from streamlit_mic_recorder import mic_recorder
from utils.speech_to_text import transcribe
from utils.text_to_speech import generate_voice

import asyncio
from langdetect import detect
from utils.translator import (
    detect_language,
    translate_to_english,
    translate_answer
)

from utils.rewriter import rewrite_query


#from utils.db_tool import get_student


from db import get_connection
VOICE_MAP = {
    "te": "te-IN-ShrutiNeural",
    "hi": "hi-IN-SwaraNeural",
    "en": "en-IN-NeerjaNeural",
    "ta": "ta-IN-PallaviNeural",
    "kn": "kn-IN-SapnaNeural",
    "ml": "ml-IN-SobhanaNeural"
}
LANGUAGE_MAP = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta"
}

# ================= DATABASE SAVE =================

def save_chat(user_msg, bot_msg, language):

    conn = get_connection()
    cursor = conn.cursor()
    conn = get_connection()


    cursor.execute("SELECT * FROM chat_history")

    rows = cursor.fetchall()

    st.write(rows)

    cursor.close()
    conn.close()

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

### 🤖 Supported Tools

- PDF RAG Search
- MySQL Database Search
- Tavily Web Search
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



    # ================= CHAT SECTION =================

retriever = st.session_state.retriever

# Display history
# ================= CHAT HISTORY =================

for i, chat in enumerate(st.session_state.chat_history):

    col1, col2 = st.columns([10, 1])

    with col1:
        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

    with col2:

        if st.button("🗑", key=f"delete_{i}"):

            st.session_state.chat_history.pop(i)

            st.rerun()
# Language Selection
selected_lang = st.selectbox(
    "🌍 Select Input Language",
    ["English", "Telugu", "Hindi", "Tamil"]
)

# Voice Input
audio = mic_recorder(
    start_prompt="🎤 Ask by Voice",
    stop_prompt="⏹ Stop Recording",
    key="mic"
)

# Text Input
user_question = st.chat_input(
    "Ask anything... Upload PDF only if needed."
)

# Voice to Text
if audio:

    with open("temp.wav", "wb") as f:
        f.write(audio["bytes"])

    lang_code = LANGUAGE_MAP[selected_lang]

    user_question = transcribe(
        "temp.wav",
        lang_code
    )

    st.success(
        f"🎤 You said: {user_question}"
    )

if user_question:

    if user_question:

        with st.chat_message("user"):
            st.write(user_question)

        with st.spinner("Thinking..."):

            try:

                # ================= LANGUAGE DETECTION =================

                user_language = detect_language(
                    user_question
                )

                english_question = translate_to_english(
                    user_question
                )

                rewritten_question = rewrite_query(
                    english_question
                )

                # ================= LANGGRAPH =================

                result = graph.invoke({
                     "question": rewritten_question,

                     "retriever": retriever

                })

                answer = result["final_answer"]

                docs = []
                    

                # ================= TRANSLATE BACK =================

                if user_language == "en":

                    final_answer = answer

                else:

                    final_answer = translate_answer(
                        answer,
                        user_language
                    )

                # ================= SOURCES =================

                sources = ""

                if docs:

                    sources = "\n\n📄 Sources:\n"

                    for d in docs:

                        sources += (
                            f"\n📌 {d.metadata.get('source','Unknown')}"
                            f" - Page {d.metadata.get('page','?')}"
                        )

                final_output = final_answer + sources
                try:
                    lang = LANGUAGE_MAP[selected_lang]
                    voice=VOICE_MAP.get(
                        lang,
                        "en-IN-NeerjaNeural"

                    )
                    asyncio.run(
                        generate_voice(
                            final_answer,
                            "answer.mp3",
                            voice
                        )
                    )
                except Exception as e:
                    print(e)    










                

                # ================= SAVE CHAT =================

                #save_chat(
                   # user_question,
                   # final_output,
                    #user_language
                #)

                # ================= DISPLAY =================

                with st.chat_message("assistant"):
                    st.write(final_output)
                    try:
                        st.audio("answer.mp3")
                    except:
                        pass    

                st.session_state.chat_history.append({

                    "question": user_question,
                    "answer": final_output

                })

            except Exception as e:

                st.error(
                    f"Error generating answer: {e}"
                )


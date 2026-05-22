import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ================= EMBEDDING MODEL =================
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )


# ================= SPLIT DOCUMENTS =================
def split_documents(documents):

    if not documents:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    # remove empty chunks
    cleaned_chunks = [
        chunk for chunk in chunks
        if chunk.page_content and chunk.page_content.strip()
    ]

    return cleaned_chunks


# ================= CREATE VECTORSTORE =================
def create_vectorstore(chunks):

    if not chunks:
        raise ValueError("No valid chunks found from PDFs.")

    embeddings = get_embedding_model()

    vectorstore = FAISS.from_documents(chunks, embeddings)

    # save locally
    os.makedirs("vectorstore", exist_ok=True)
    vectorstore.save_local("vectorstore")

    return vectorstore


# ================= LOAD VECTORSTORE =================
def load_vectorstore():

    embeddings = get_embedding_model()

    if os.path.exists("vectorstore"):
        vectorstore = FAISS.load_local(
            "vectorstore",
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore

    return None
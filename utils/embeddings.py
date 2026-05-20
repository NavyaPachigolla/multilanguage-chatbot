import os

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)


# ===============================
# SPLIT DOCUMENTS
# ===============================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks


# ===============================
# CREATE VECTORSTORE
# ===============================

def create_vectorstore(chunks):

    embedding_model = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    vectorstore = FAISS.from_documents(

        documents=chunks,

        embedding=embedding_model
    )

    # SAVE LOCALLY

    vectorstore.save_local(
        "vectorstore"
    )

    return vectorstore


# ===============================
# LOAD VECTORSTORE
# ===============================

def load_vectorstore():

    embedding_model = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    if os.path.exists("vectorstore"):

        vectorstore = FAISS.load_local(

            "vectorstore",

            embedding_model,

            allow_dangerous_deserialization=True
        )

        return vectorstore

    return None
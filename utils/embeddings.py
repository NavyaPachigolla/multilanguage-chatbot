import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS


# Load multilingual embedding model
def get_embedding_model():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    return embeddings


# Split documents into chunks
def split_documents(documents):

    if not documents:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    # Remove empty chunks
    cleaned_chunks = []

    for chunk in chunks:

        if chunk.page_content.strip():
            cleaned_chunks.append(chunk)

    return cleaned_chunks


# Create FAISS vector store
def create_vectorstore(chunks):

    if not chunks:
        raise ValueError("No valid chunks found from uploaded PDFs.")

    embeddings = get_embedding_model()

    # Create vector DB
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Create folder if missing
    os.makedirs("vectorstore", exist_ok=True)

    # Save locally
    vectorstore.save_local("vectorstore")

    return vectorstore


# Load saved vectorstore
def load_vectorstore():

    embeddings = get_embedding_model()

    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore
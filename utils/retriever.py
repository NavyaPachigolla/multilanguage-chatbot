from utils.embeddings import load_vectorstore


def get_retriever():

    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever
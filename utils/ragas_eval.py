def evaluate_rag(question, answer, docs):

    contexts = [
        doc.page_content for doc in docs
    ]

    evaluation_result = {
        "Question": question,
        "Answer Length": len(answer),
        "Retrieved Chunks": len(contexts),
        "Context Characters": sum(len(c) for c in contexts)
    }

    return evaluation_result
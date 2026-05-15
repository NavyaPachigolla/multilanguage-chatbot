def format_sources(source_documents):

    sources = []

    for doc in source_documents:

        file_name = doc.metadata.get("source", "Unknown")

        page = doc.metadata.get("page", "N/A")

        source_text = f"{file_name} — Page {page}"

        if source_text not in sources:
            sources.append(source_text)

    return sources
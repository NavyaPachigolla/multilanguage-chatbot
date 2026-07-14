def route_query(query):

    query = query.lower()

    # ================= DATABASE =================

    db_keywords = [
        "student",
        "cgpa",
        "eligible",
        "college",
        "database",
        "placement status",
        "student details",
        "student information"
    ]

    # ================= WEB SEARCH =================

    web_keywords = [
        "ceo",
        "latest",
        "current",
        "today",
        "recent",
        "news",
        "ipl",
        "cricket",
        "match",
        "winner",
        "won",
        "score",
        "sports",
        "president",
        "prime minister",

        "cm",
        "chief minister",
        "governor",
        "minister",
        "andhra pradesh",
        "telangana",
        "india",

        "weather",
        "stock",
        "share price",
        "tcs",
        "infosys",
        "wipro",
        "google",
        "microsoft",
        "openai",
        "ai news",
        "trending",
        "live",
        "update"
    ]

    # ================= PDF SUMMARY =================

    summary_keywords = [
        "summary",
        "summarize",
        "overview",
        "pdf about",
        "document about",
        "what is this pdf about",
        "explain this document",
        "document summary"
    ]

    # ================= ROUTING =================

    if any(word in query for word in summary_keywords):
        return "summary"

    if any(word in query for word in db_keywords):
        return "database"

    if any(word in query for word in web_keywords):
        return "web"
    general_question_words = [
        "who",
        "what",
        "when",
        "where",
        "which",
        "current"
    ]
    if any(word in query for word in general_question_words):
        return "web"
    # ================= DEFAULT =================

    return "rag"
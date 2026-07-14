from typing import TypedDict, Any

class ChatState(TypedDict):

    question: str

    language: str

    english_question: str

    rewritten_question: str

    route: str

    answer: str

    final_answer: str

    retriever: Any
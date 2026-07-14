from utils.rewriter import rewrite_query
from utils.router import route_query
from utils.tavily_tool import web_search
from utils.rag_chain import (
    generate_answer,
    generate_web_answer
)
from utils.translator import (
    detect_language,
    translate_to_english,
    translate_answer
)


def rewrite_node(state):

    rewritten = rewrite_query(
        state["english_question"]
    )

    return {
        "rewritten_question": rewritten
    }


def route_node(state):

    route = route_query(
        state["rewritten_question"]
    )

    return {
        "route": route
    }


def web_node(state):

    web_context = web_search(
        state["rewritten_question"]
    )

    answer = generate_web_answer(
        state["rewritten_question"],
        web_context
    )

    return {
        "answer": answer
    }


def pdf_node(state):
    print(state)
    

    retriever = state["retriever"]

    answer, docs = generate_answer(
        state["rewritten_question"],
        retriever
    )

    return {
        "answer": answer
    }
def language_node(state):

    language = detect_language(
        state["question"]
    )

    return {
        "language": language
    }
def translate_node(state):

    english_question = translate_to_english(
        state["question"]
    )

    return {
        "english_question": english_question
    }
def translate_back_node(state):

    if state["language"] == "en":

        return {
            "final_answer": state["answer"]
        }

    final_answer = translate_answer(

        state["answer"],

        state["language"]

    )

    return {
        "final_answer": final_answer
    }
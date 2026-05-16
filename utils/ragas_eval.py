from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

from langchain_groq import ChatGroq

from ragas.llms import LangchainLLMWrapper

from langchain_huggingface import HuggingFaceEmbeddings

from ragas.embeddings import (
    LangchainEmbeddingsWrapper
)

from utils.test_dataset import test_questions

from utils.rag_chain import generate_answer


def run_ragas_evaluation(retriever):

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    # GENERATE TEST DATA

    for item in test_questions:

        question = item["question"]

        ground_truth = item["ground_truth"]

        answer, source_docs = generate_answer(

            question,

            retriever
        )

        retrieved_contexts = [

            doc.page_content

            for doc in source_docs
        ]

        questions.append(question)

        answers.append(answer)

        contexts.append(retrieved_contexts)

        ground_truths.append(ground_truth)

    # CREATE DATASET

    dataset = Dataset.from_dict({

        "question": questions,

        "answer": answers,

        "contexts": contexts,

        "ground_truth": ground_truths
    })

    # ===============================
    # GROQ EVALUATOR MODEL
    # ===============================

    groq_llm = ChatGroq(

        model="llama-3.3-70b-versatile",

        temperature=0
    )

    evaluator_llm = LangchainLLMWrapper(

        groq_llm
    )

    # ===============================
    # HUGGINGFACE EMBEDDINGS
    # ===============================

    embedding_model = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    evaluator_embeddings = (

        LangchainEmbeddingsWrapper(

            embedding_model
        )
    )

    # ===============================
    # RUN RAGAS
    # ===============================

    result = evaluate(

        dataset=dataset,

        metrics=[

            faithfulness,

            answer_relevancy,

            context_precision,

            context_recall
        ],

        llm=evaluator_llm,

        embeddings=evaluator_embeddings
    )

    # ===============================
    # CONVERT TO DATAFRAME
    # ===============================

    result_df = result.to_pandas()

    # REMOVE NaN VALUES

    result_df = result_df.fillna(0)

    # ===============================
    # AVERAGE SCORES
    # ===============================

    avg_scores = {

        "Faithfulness":
        round(

            float(
                result_df["faithfulness"].mean()
            ) * 100,

            2
        ),

        "Answer Relevancy":
        round(

            float(
                result_df["answer_relevancy"].mean()
            ) * 100,

            2
        ),

        "Context Precision":
        round(

            float(
                result_df["context_precision"].mean()
            ) * 100,

            2
        ),

        "Context Recall":
        round(

            float(
                result_df["context_recall"].mean()
            ) * 100,

            2
        )
    }

    return result_df, avg_scores
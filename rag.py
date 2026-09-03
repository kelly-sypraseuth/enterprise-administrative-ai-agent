from embedding_search import (
    get_confidence,
    get_ranked_results,
    semantic_document_search,
)

from llm import ask_llm


def format_source(result):
    title = result["title"]
    document_type = result["document_type"]
    authority = result["authority"]
    version = result["version"]
    page_number = result.get("page_number")
    chunk_number = result["chunk_number"]

    source = (
        f"{title} | "
        f"Type: {document_type} | "
        f"Authority: {authority} | "
        f"Version: {version}"
    )

    if page_number:
        source += f" | Page {page_number}"

    source += f" | Chunk {chunk_number}"

    return source


def answer_with_rag(question):
    ranked_results = get_ranked_results(
        question
    )

    if not ranked_results:
        return (
            "I could not find any "
            "reference information."
        )

    best_score = ranked_results[0]["score"]
    confidence = get_confidence(best_score)

    if confidence == "LOW":
        return (
            "I do not have enough supporting "
            "information in the reference documents "
            "to answer that question.\n\n"
            f"Confidence: {confidence} | "
            f"Best retrieval score: "
            f"{best_score:.3f}"
        )

    results = semantic_document_search(
        question,
        top_k=3
    )

    if not results:
        return (
            "I do not have enough supporting "
            "information in the reference documents "
            "to answer that question."
        )

    context_parts = []
    source_parts = []

    for result in results:
        context_parts.append(
            f"Source metadata:\n"
            f"{format_source(result)}\n"
            f"Content:\n"
            f"{result['text']}"
        )

        source_parts.append(
            format_source(result)
        )

    context = "\n\n".join(
        context_parts
    )

    answer = ask_llm(
        question,
        context
    )

    sources = "\n".join(
        f"- {source}"
        for source in source_parts
    )

    return (
        f"{answer}\n\n"
        f"Confidence: {confidence} | "
        f"Best retrieval score: "
        f"{best_score:.3f}\n\n"
        f"Sources:\n"
        f"{sources}"
    )
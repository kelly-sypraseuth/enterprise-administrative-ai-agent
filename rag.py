from embedding_search import semantic_document_search
from llm import ask_llm


def answer_with_rag(question):
    results = semantic_document_search(
        question,
        top_k=3
    )

    if not results:
        return "I could not find supporting information in the reference documents."

    context_parts = []
    source_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['document_name']}\n"
            f"Chunk: {result['chunk_number']}\n"
            f"Content: {result['text']}"
        )

        source_parts.append(
            f"{result['document_name']} "
            f"(Chunk {result['chunk_number']})"
        )

    context = "\n\n".join(context_parts)

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
        f"Sources:\n{sources}"
    )
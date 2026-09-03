from llm import client
from vector_store import get_collection


MINIMUM_SCORE = 0.35


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def convert_distance_to_similarity(
    distance
):
    return 1 - distance


def search_vector_database(
    question,
    number_of_results
):
    collection = get_collection()

    total_records = collection.count()

    if total_records == 0:
        return []

    result_count = min(
        number_of_results,
        total_records
    )

    question_embedding = get_embedding(
        question
    )

    response = collection.query(
        query_embeddings=[
            question_embedding
        ],
        n_results=result_count,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    results = []

    documents = response["documents"][0]
    metadatas = response["metadatas"][0]
    distances = response["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        score = convert_distance_to_similarity(
            distance
        )

        page_number = metadata.get(
            "page_number",
            0
        )

        if page_number == 0:
            page_number = None

        results.append(
            {
                "text": document,
                "source": metadata["source"],
                "document_name": metadata[
                    "document_name"
                ],
                "title": metadata["title"],
                "document_type": metadata[
                    "document_type"
                ],
                "authority": metadata["authority"],
                "version": metadata["version"],
                "page_number": page_number,
                "chunk_number": metadata[
                    "chunk_number"
                ],
                "score": score
            }
        )

    return results


def get_ranked_results(question):
    collection = get_collection()

    total_records = collection.count()

    if total_records == 0:
        return []

    return search_vector_database(
        question,
        total_records
    )


def semantic_document_search(
    question,
    top_k=3,
    threshold=MINIMUM_SCORE
):
    results = search_vector_database(
        question,
        top_k
    )

    relevant_results = [
        result
        for result in results
        if result["score"] >= threshold
    ]

    return relevant_results


def get_confidence(score):
    if score >= 0.55:
        return "HIGH"

    if score >= MINIMUM_SCORE:
        return "MODERATE"

    return "LOW"
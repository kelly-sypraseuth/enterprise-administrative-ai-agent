import json

import numpy as np

from llm import client


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def load_embedding_cache():
    with open(
        "data/embeddings.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def get_ranked_results(question):
    cached_chunks = load_embedding_cache()

    question_embedding = get_embedding(question)

    results = []

    for item in cached_chunks:
        score = cosine_similarity(
            question_embedding,
            item["embedding"]
        )

        results.append(
            {
                "text": item["text"],
                "source": item["source"],
                "document_name": item["document_name"],
                "chunk_number": item["chunk_number"],
                "score": score
            }
        )

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results


def semantic_document_search(question, top_k=3, threshold=0.35):
    results = get_ranked_results(question)

    relevant_results = [
        result
        for result in results
        if result["score"] >= threshold
    ]

    return relevant_results[:top_k]
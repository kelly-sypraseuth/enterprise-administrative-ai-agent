from embedding_search import get_ranked_results
from rag import answer_with_rag


question = input("Ask the RAG system a question: ")

ranked_results = get_ranked_results(question)

print("\nRETRIEVAL DEBUG:")
print("----------------")

for number, result in enumerate(ranked_results, start=1):
    print(
        f"{number}. "
        f"{result['document_name']} | "
        f"Chunk {result['chunk_number']} | "
        f"Score: {result['score']:.3f}"
    )

answer = answer_with_rag(question)

print("\nRAG response:")
print(answer)
import glob
import json
import os

from chunking import chunk_text
from llm import client


DOCUMENT_FOLDER = "documents"


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def load_all_chunks():
    all_chunks = []

    file_paths = glob.glob(
        os.path.join(DOCUMENT_FOLDER, "*.txt")
    )

    for file_path in file_paths:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            document_text = file.read()

        document_chunks = chunk_text(document_text)

        for chunk in document_chunks:
            all_chunks.append(
                {
                    "source": file_path,
                    "document_name": os.path.basename(file_path),
                    "chunk_number": chunk["chunk_number"],
                    "text": chunk["text"]
                }
            )

    return all_chunks


def build_embedding_cache():
    chunks = load_all_chunks()

    cached_data = []

    print(f"Found {len(chunks)} document chunks.")

    for index, chunk in enumerate(chunks, start=1):
        print(
            f"Creating embedding {index}/{len(chunks)} "
            f"from {chunk['document_name']} "
            f"(chunk {chunk['chunk_number']})..."
        )

        embedding = get_embedding(chunk["text"])

        cached_data.append(
            {
                "source": chunk["source"],
                "document_name": chunk["document_name"],
                "chunk_number": chunk["chunk_number"],
                "text": chunk["text"],
                "embedding": embedding
            }
        )

    with open(
        "data/embeddings.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(cached_data, file)

    print("Embedding cache created successfully.")


if __name__ == "__main__":
    build_embedding_cache()
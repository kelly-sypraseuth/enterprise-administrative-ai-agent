import glob
import json
import os

from chunking import chunk_text
from document_loader import load_document
from llm import client
from vector_store import (
    get_collection,
    reset_collection,
)


DOCUMENT_FOLDER = "documents"
METADATA_FILE = "document_metadata.json"


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def load_metadata():
    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def get_document_metadata(
    document_name,
    metadata_registry
):
    return metadata_registry.get(
        document_name,
        {
            "title": document_name,
            "document_type": "Unknown",
            "authority": "Unknown",
            "version": "Unknown"
        }
    )


def load_all_chunks():
    all_chunks = []

    metadata_registry = load_metadata()

    file_paths = glob.glob(
        os.path.join(
            DOCUMENT_FOLDER,
            "*"
        )
    )

    for file_path in file_paths:
        document = load_document(
            file_path
        )

        if not document:
            continue

        document_name = os.path.basename(
            file_path
        )

        metadata = get_document_metadata(
            document_name,
            metadata_registry
        )

        if document["type"] == "txt":
            document_chunks = chunk_text(
                document["content"]
            )

            for chunk in document_chunks:
                all_chunks.append(
                    {
                        "source": file_path,
                        "document_name": document_name,
                        "title": metadata["title"],
                        "document_type": metadata[
                            "document_type"
                        ],
                        "authority": metadata[
                            "authority"
                        ],
                        "version": metadata["version"],
                        "page_number": 0,
                        "chunk_number": chunk[
                            "chunk_number"
                        ],
                        "text": chunk["text"]
                    }
                )

        if document["type"] == "pdf":
            for page in document["content"]:
                page_chunks = chunk_text(
                    page["text"]
                )

                for chunk in page_chunks:
                    all_chunks.append(
                        {
                            "source": file_path,
                            "document_name": document_name,
                            "title": metadata["title"],
                            "document_type": metadata[
                                "document_type"
                            ],
                            "authority": metadata[
                                "authority"
                            ],
                            "version": metadata[
                                "version"
                            ],
                            "page_number": page[
                                "page_number"
                            ],
                            "chunk_number": chunk[
                                "chunk_number"
                            ],
                            "text": chunk["text"]
                        }
                    )

    return all_chunks


def build_vector_database():
    chunks = load_all_chunks()

    collection = reset_collection()

    print(
        f"Found {len(chunks)} "
        f"document chunks."
    )

    for index, chunk in enumerate(
        chunks,
        start=1
    ):
        print(
            f"Creating embedding "
            f"{index}/{len(chunks)} "
            f"from "
            f"{chunk['document_name']}..."
        )

        embedding = get_embedding(
            chunk["text"]
        )

        record_id = (
            f"{chunk['document_name']}::"
            f"{chunk['page_number']}::"
            f"{chunk['chunk_number']}"
        )

        collection.add(
            ids=[
                record_id
            ],
            documents=[
                chunk["text"]
            ],
            embeddings=[
                embedding
            ],
            metadatas=[
                {
                    "source": chunk["source"],
                    "document_name": chunk[
                        "document_name"
                    ],
                    "title": chunk["title"],
                    "document_type": chunk[
                        "document_type"
                    ],
                    "authority": chunk[
                        "authority"
                    ],
                    "version": chunk[
                        "version"
                    ],
                    "page_number": chunk[
                        "page_number"
                    ],
                    "chunk_number": chunk[
                        "chunk_number"
                    ]
                }
            ]
        )

    print(
        "Vector database created successfully."
    )

    print(
        f"Records stored: "
        f"{collection.count()}"
    )


def ensure_vector_database():
    try:
        collection = get_collection()

        if collection.count() > 0:
            print(
                f"Vector database already available "
                f"with {collection.count()} records."
            )
            return

    except Exception:
        print(
            "Vector database not found. "
            "Building from reference documents..."
        )

    build_vector_database()


if __name__ == "__main__":
    build_vector_database()
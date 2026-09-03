import json

from rag import answer_with_rag


METADATA_FILE = "document_metadata.json"


def search_knowledge(question):
    return answer_with_rag(question)


def list_available_references():
    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    references = []

    for document_name, details in metadata.items():
        references.append(
            (
                f"- {details['title']} | "
                f"Type: {details['document_type']} | "
                f"Authority: {details['authority']} | "
                f"Version: {details['version']}"
            )
        )

    return (
        "Available reference documents:\n"
        + "\n".join(references)
    )
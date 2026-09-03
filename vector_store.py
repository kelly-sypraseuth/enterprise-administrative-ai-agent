import chromadb


DATABASE_PATH = "data/chroma_db"
COLLECTION_NAME = "misso_documents"


client = chromadb.PersistentClient(
    path=DATABASE_PATH
)


def create_collection():
    return client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )


def get_collection():
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=None
    )


def reset_collection():
    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )
    except Exception:
        pass

    return create_collection()
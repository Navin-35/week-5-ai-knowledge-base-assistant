from app.vector_store import load_vector_store


def search(query: str, k: int = 3):

    db = load_vector_store()

    docs = db.similarity_search(
        query,
        k=k
    )

    return docs
from app.vector_store import load_vector_store


def search(query):

    db = load_vector_store()

    docs = db.similarity_search(

        query,

        k=3

    )

    return docs
from langchain_community.vectorstores import FAISS
from app.embeddings import embeddings


def create_vector_store(chunks):

    db = FAISS.from_documents(

        chunks,

        embeddings

    )

    db.save_local("vector_db")

    return db


def load_vector_store():

    return FAISS.load_local(

        "vector_db",

        embeddings,

        allow_dangerous_deserialization=True

    )
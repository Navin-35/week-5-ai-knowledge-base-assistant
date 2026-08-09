from rank_bm25 import BM25Okapi

from app.vector_store import load_vector_store
from app.document_loader import load_documents
from app.text_splitter import split_documents


def keyword_search(query: str, chunks, k: int = 3):
    """
    Search document chunks using BM25 keyword matching.
    """

    tokenized_documents = [
        chunk.page_content.lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_documents)

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    return [chunks[i] for i in ranked_indexes]


def semantic_search(query: str, k: int = 3):
    """
    Search the FAISS vector database using semantic similarity.
    """

    db = load_vector_store()

    return db.similarity_search(
        query,
        k=k
    )


def hybrid_search(query: str, k: int = 3):
    """
    Combine semantic and keyword search results.
    """

    documents = load_documents()

    chunks = split_documents(documents)

    semantic_results = semantic_search(
        query,
        k=k
    )

    keyword_results = keyword_search(
        query,
        chunks,
        k=k
    )

    combined = []

    seen = set()

    for doc in semantic_results + keyword_results:

        content = doc.page_content

        if content not in seen:

            combined.append(doc)

            seen.add(content)

    return combined[:k]
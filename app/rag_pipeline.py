from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.query_transformer import transform_query
from app.hybrid_search import hybrid_search
from app.reranker import rerank_documents


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)


def ask_question(question: str):

    # Step 1: Transform the user query
    improved_query = transform_query(question)

    # Step 2: Retrieve candidate documents
    candidate_docs = hybrid_search(
        improved_query,
        k=6
    )

    # Step 3: Rerank candidates
    relevant_docs = rerank_documents(
        improved_query,
        candidate_docs,
        top_k=3
    )

    # Step 4: Build context
    context = "\n\n".join(
        doc.page_content
        for doc in relevant_docs
    )

    # Step 5: Generate answer
    prompt = f"""
You are an AI Knowledge Base Assistant for DStarix.

Answer the user's question ONLY using the provided company knowledge base context.

Knowledge Base Context:

{context}

User Question:

{question}

Instructions:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not present in the context, say:
"I couldn't find this information in the company knowledge base."
4. Keep the answer concise and professional.
"""

    response = llm.invoke(prompt)

    return {
        "original_query": question,
        "improved_query": improved_query,
        "retrieved_documents": len(candidate_docs),
        "reranked_documents": len(relevant_docs),
        "answer": response.content,
    }
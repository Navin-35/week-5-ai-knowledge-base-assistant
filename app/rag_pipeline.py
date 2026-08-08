from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.query_transformer import transform_query
from app.retriever import search

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)


def ask_question(question: str):

    improved_query = transform_query(question)

    docs = search(improved_query)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an AI Knowledge Base Assistant.

Answer ONLY using the provided context.

Context:

{context}

Question:

{question}

If the answer is not present in the context, say:
"I couldn't find this information in the company knowledge base."
"""

    response = llm.invoke(prompt)

    return {
        "original_query": question,
        "improved_query": improved_query,
        "answer": response.content,
    }
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)


def transform_query(query: str) -> str:
    prompt = f"""
You are a query rewriting assistant.

Rewrite the user's question so it is better suited for searching an enterprise knowledge base.

Only return the improved search query.

User Question:
{query}
"""

    response = llm.invoke(prompt)

    return response.content.strip()
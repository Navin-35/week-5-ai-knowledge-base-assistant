from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.query_transformer import transform_query
from app.hybrid_search import hybrid_search
from app.reranker import rerank_documents
from app.guardrails import validate_input
from app.models import AnswerResponse
from app.logger import logger


# --------------------------------------------------
# Gemini LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)


# --------------------------------------------------
# Main RAG Pipeline
# --------------------------------------------------

def ask_question(question: str):

    try:

        # ------------------------------------------
        # 1. INPUT GUARDRAIL
        # ------------------------------------------

        is_valid, error_message = validate_input(question)

        if not is_valid:

            logger.warning(
                "Input rejected by guardrail"
            )

            return {
                "success": False,
                "error": error_message,
            }


        logger.info("Received valid user question")


        # ------------------------------------------
        # 2. QUERY TRANSFORMATION
        # ------------------------------------------

        improved_query = transform_query(question)

        logger.info(
            "Query transformation completed"
        )


        # ------------------------------------------
        # 3. HYBRID SEARCH
        # ------------------------------------------

        candidate_docs = hybrid_search(
            improved_query,
            k=6
        )

        logger.info(
            "Retrieved %d candidate documents",
            len(candidate_docs)
        )


        # ------------------------------------------
        # 4. RERANKING
        # ------------------------------------------

        relevant_docs = rerank_documents(
            improved_query,
            candidate_docs,
            top_k=3
        )

        logger.info(
            "Reranked documents: %d",
            len(relevant_docs)
        )


        # ------------------------------------------
        # 5. CHECK RETRIEVAL
        # ------------------------------------------

        if not relevant_docs:

            logger.warning(
                "No relevant documents found"
            )

            return {
                "success": True,
                "answer": (
                    "I couldn't find this information "
                    "in the company knowledge base."
                ),
                "sources": [],
                "confidence": "low",
                "original_query": question,
                "improved_query": improved_query,
            }


        # ------------------------------------------
        # 6. BUILD CONTEXT
        # ------------------------------------------

        context = "\n\n".join(
            doc.page_content
            for doc in relevant_docs
        )


        # ------------------------------------------
        # 7. GENERATE ANSWER WITH GEMINI
        # ------------------------------------------

        prompt = f"""
You are the DStarix AI Knowledge Base Assistant.

Your job is to answer questions ONLY using the
provided DStarix company knowledge base.

========================
KNOWLEDGE BASE CONTEXT
========================

{context}

========================
USER QUESTION
========================

{question}

========================
RULES
========================

1. Answer only using the provided context.

2. Do not use outside knowledge.

3. Do not invent or assume information.

4. If the answer cannot be found in the
   provided context, respond with:

"I couldn't find this information in the
company knowledge base."

5. Keep the answer concise and professional.

6. Mention the relevant company information
   clearly.
"""


        response = llm.invoke(prompt)

        answer = response.content.strip()


        logger.info(
            "Answer generated successfully"
        )


        # ------------------------------------------
        # 8. OUTPUT VALIDATION / STRUCTURED OUTPUT
        # ------------------------------------------

        result = AnswerResponse(
            answer=answer,
            sources=[
                "DStarix Employee Handbook"
            ],
            confidence="high",
        )


        # ------------------------------------------
        # 9. FINAL RESPONSE
        # ------------------------------------------

        return {
            "success": True,
            "answer": result.answer,
            "sources": result.sources,
            "confidence": result.confidence,
            "original_query": question,
            "improved_query": improved_query,
        }


    # ------------------------------------------
    # 10. ERROR HANDLING
    # ------------------------------------------

    except Exception as e:

        logger.exception(
            "Unexpected error while processing question"
        )

        return {
            "success": False,
            "error": "An unexpected error occurred while processing your question.",
        }
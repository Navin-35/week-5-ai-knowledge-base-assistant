from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import ask_question


app = FastAPI(
    title="DStarix AI Knowledge Base Assistant",
    description="Enterprise Advanced RAG Assistant",
    version="1.0.0"
)


class QuestionRequest(BaseModel):

    question: str


@app.get("/")
def home():

    return {
        "message": "DStarix AI Knowledge Base Assistant"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    return ask_question(request.question)
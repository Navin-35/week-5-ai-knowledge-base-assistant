# DStarix AI Knowledge Base Assistant

An enterprise-style AI Knowledge Base Assistant built with **Advanced RAG**, **FastAPI**, and **Google Gemini**. It answers questions from company documents using query transformation, hybrid retrieval, reranking, guardrails, and structured responses.

## Features

- Query transformation
- Semantic search with FAISS
- Keyword search with BM25
- Hybrid retrieval
- Cross-encoder reranking
- Input guardrails
- Grounded responses
- Structured JSON output
- Logging and error handling
- FastAPI REST API

## Tech Stack

- Python
- FastAPI
- LangChain
- Google Gemini
- FAISS
- BM25
- Sentence Transformers
- Pydantic

## Setup

```bash
git clone <repository-url>
cd week-5-ai-knowledge-base-assistant

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

## Run

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Architecture

```text
User
 ↓
Guardrails
 ↓
Query Transformation
 ↓
FAISS + BM25
 ↓
Reranking
 ↓
Gemini
 ↓
Structured Response
```

## Knowledge Base

The project currently uses a sample **DStarix Employee Handbook** as its knowledge source.

## Author

**Navin Kumar**
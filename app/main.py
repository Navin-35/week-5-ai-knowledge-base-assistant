from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Base Assistant",
    description="Enterprise GenAI Project - Week 5",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Knowledge Base Assistant"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }
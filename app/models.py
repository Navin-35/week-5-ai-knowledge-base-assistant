from pydantic import BaseModel, Field


class AnswerResponse(BaseModel):

    answer: str = Field(
        description="Answer based only on the company knowledge base."
    )

    sources: list[str] = Field(
        default_factory=list,
        description="Sources used to answer the question."
    )

    confidence: str = Field(
        description="Confidence level: high, medium, or low."
    )
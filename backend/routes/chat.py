from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.postgres_rag import PostgreSQLRAG


router = APIRouter(prefix="/chat",tags=["Chat"])

class ChatRequest(BaseModel):
    question: str


# Create RAG object
rag = PostgreSQLRAG(
    postgres_password="Documind@123",
    hf_token=None
)


@router.post("/")
def chat(request: ChatRequest):

    try:

        result = rag.answer_question(question=request.question,k=3)

        return result

    except Exception as e:

        raise HTTPException(status_code=500,detail=str(e))
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import answer_question

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query", response_model=QueryResponse)
def query_knowledge(req: QueryRequest):
    answer = answer_question(req.question)
    return {"answer":answer}
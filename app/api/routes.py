from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedding_service import embed_text
from app.services.rag_service import (query_chunks, answer_question, filter_results, group_by_source, select_best_chunks, build_context)

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query")
def query(req: QueryRequest):
    raw_results = query_chunks(embed_text(req.question))

    filtered = filter_results(raw_results)

    if not filtered:
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }
    
    grouped = group_by_source(filtered)
    selected = select_best_chunks(grouped)
    context = build_context(selected)
    
    answer = answer_question(req.question, context)

    print("Retrieved:", len(filtered))
    for c in selected:
        print(c["title"], c["distance"])

    return {
            "answer": answer,
            "sources": list({c["title"] for c in selected})
    }
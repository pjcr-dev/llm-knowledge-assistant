from fastapi import APIRouter, Form
from pydantic import BaseModel
from app.services.embedding_service import embed_text
from app.services.rag_service import (query_chunks, answer_question, filter_results, group_by_source, select_best_chunks, build_context)
from fastapi.responses import HTMLResponse

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query")
def query(question: str = Form(...)):
    raw_results = query_chunks(embed_text(question))

    filtered = filter_results(raw_results)

    if not filtered:
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }
    
    grouped = group_by_source(filtered)
    selected = select_best_chunks(grouped)
    context = build_context(selected)
    
    answer = answer_question(question, context)

    print("Retrieved:", len(filtered))
    for c in selected:
        print(c["title"], c["distance"])

    return {
            "answer": answer,
            "sources": list({c["title"] for c in selected})
    }

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <body>
        <h2>Knowledge Assistant</h2>
        <form action="/query" method="post">
          <input name="question" />
          <button type="submit">Ask</button>
        </form>
      </body>
    </html>
    """
from fastapi import APIRouter, Form
from pydantic import BaseModel
from app.services.embedding_service import embed_text
from app.services.rag_service import (query_chunks, answer_question, filter_results, group_by_source, select_best_chunks, build_context)
from fastapi.responses import HTMLResponse
from app.db.vector_store import collection
from app.services.llm_service import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query", response_class=HTMLResponse)
def query(question: str = Form(...)):

    if collection.count() == 0:
        return render_page(
            question,
            "The knowledge base is empty. Please ingest documents first.",
            []
        )

    try:
        raw_results = query_chunks(embed_text(question))
        filtered = filter_results(raw_results)

        if not filtered:
            return render_page(
                question,
                "No relevant information found for your question.",
                []
            )
        
        grouped = group_by_source(filtered)
        selected = select_best_chunks(grouped)
        context = build_context(selected)
        
        answer = answer_question(question, context)

        sources = sorted({c["title"] for c in selected})
        
        #print("Retrieved:", len(filtered))
        # for c in selected:
        #     print(c["title"], c["distance"])

        return render_page(question, answer, sources)
    
        # ALTERNATIVE:
        # return HTMLResponse(
        #     content=render_page(question, answer, sources)
        # )

    except Exception as e:
        return render_page(
            question,
            "An error occurred while processing your request",
            [],
            error=str(e)
        )
    
        # ALTERNATIVE:
        # return HTMLResponse(
        #         content=render_page(
        #             question,
        #             "An unexpected error occurred.",
        #             [],
        #             error=str(e)
        #         ),
        #         status_code=500
        #     )

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title>Knowledge Assistant</title>
      </head>
      <body style="font-family: Arial; max-width: 800px; margin: auto;">
        <h2>LLM-Powered Knowledge Assistant</h2>

        <form action="/query" method="post">
          <input 
            type="text" 
            name="question" 
            placeholder="Ask a question..."
            style="width: 100%; padding: 8px;"
            required
          />
          <br/><br/>
          <button type="submit">Ask</button>
        </form>
      </body>
    </html>
    """

@router.get("/favicon.ico")
def favicon():
    return {}

def render_page(question: str, answer: str, sources: list[str], error: str | None =  None) -> HTMLResponse:
    sources_html = ""
    if sources:
        sources_html = "<h4>Sources:</h4><ul>"
        for src in sources:
            sources_html += f"<li>{src}</li>"
        sources_html += "</ul>"

    error_html = ""
    if error:
        error_html = f"<pre style='color: red;'>{error}</pre>" 

    return f"""
    <html>
      <head>
        <title>Knowledge Assistant</title>
      </head>
      <body style="font-family: Arial; max-width: 800px; margin: auto;">
        <h2>LLM-Powered Knowledge Assistant</h2>

        <form action="/query" method="post">
          <input 
            type="text" 
            name="question" 
            value="{question}"
            style="width: 100%; padding: 8px;"
            required
          />
          <br/><br/>
          <button type="submit">Ask</button>
        </form>

        <hr/>

        <h3>Answer</h3>
        <p>{answer}</p>

        {sources_html}

        {error_html}
      </body>
    </html>
    """
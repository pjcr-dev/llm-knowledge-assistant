from fastapi import APIRouter, Form
from pydantic import BaseModel
from app.services.rag_service import answer_question
from fastapi.responses import HTMLResponse

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query", response_class=HTMLResponse)
def query(question: str = Form(...)):
    
    result = answer_question(question)

    return HTMLResponse(
        content=render_page(question, result["answer"], result["sources"])
    )

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
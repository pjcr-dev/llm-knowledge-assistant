from fastapi import FastAPI
from app.api.routes import router
from app.db.vector_store import collection
from app.core.config import settings

app = FastAPI(title="LLM Knowledge Assistant")

app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "vector_store": "ready",
        "documents_indexed": collection.count(),
        "model": settings.model_name
    }
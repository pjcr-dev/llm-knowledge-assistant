from fastapi import FastAPI
from app.api.routes import router
from app.db.vector_store import collection
from app.core.config import settings
from app.ingestion.ingest import ingest_docs
from contextlib import asynccontextmanager
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.run_ingest_on_startup:
        logger.info("Application startup: beginning document ingestion")
        ingest_docs()
        logger.info("Application startup: ingestion complete")
    yield
    logger.info("Application shutdown")

app = FastAPI(title="LLM Knowledge Assistant", lifespan=lifespan)

app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "vector_store": "ready",
        "documents_indexed": collection.count(),
        "model": settings.model_name
    }


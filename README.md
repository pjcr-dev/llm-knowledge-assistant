# LLM-Powered Knowledge Assistant

## Overview

This project is a **Retrieval-Augmented Generation (RAG)** system that allows users to query a local knowledge base using natural language. It combines:

* Document ingestion and chunking
* Vector embeddings stored in a vector database (Chroma)
* Semantic retrieval
* Large Language Model (LLM) generation grounded in retrieved context
* A simple HTML-based user interface

---

## Architecture

```
User (Browser)
   │
   ▼
FastAPI Web Server
   │
   ├── / (HTML UI)
   └── /query (Form POST)
        │
        ▼
Query Pipeline
   │
   ├── Embed user question
   ├── Retrieve top-K document chunks (Chroma)
   ├── Filter by relevance (distance threshold)
   ├── Group & de-duplicate by source
   ├── Build structured context
   │
   ▼
LLM (Answer Generation)
   │
   ▼
HTML Response (Answer + Sources)
```

---

## Project Structure

```
.
├── app/
│   ├── db/                 # Vector store setup (Chroma)
│   ├── models/             # Pydantic models
│   ├── services/           # Embedding, query, and LLM logic
│   ├── utils/              # Chunking and file loading
│   └── api/                # FastAPI routes
├── data/
│   └── docs/               # Source documents (Markdown)
├── scripts/
│   └── ingest_documents.py # Idempotent ingestion script
├── chroma_db/              # Vector database (gitignored)
├── main.py                 # FastAPI entry point
└── README.md
```

---

## Data Flow

### Ingestion Flow

1. Raw documents are placed in `data/docs/`
2. Each document is loaded from disk
3. Documents are chunked into overlapping text segments
4. Each chunk is embedded using an embedding model
5. Chunks are **upserted** into Chroma using stable IDs

---

### Query Flow

1. User submits a question via the HTML form
2. The question is embedded
3. Chroma retrieves top-K nearest chunks
4. Results are filtered by distance (relevance threshold)
5. Chunks are grouped by document source
6. A limited number of chunks per source are selected
7. A structured context is built
8. The LLM generates an answer grounded in the retrieved context
9. The answer and sources are rendered as HTML

---

## Limitations/Future Improvements

* No authentication or rate limiting
* Simple HTML UI (no frontend framework)
* No automatic document upload via UI

---

## How to Run Locally

1. Create a virtual environment
2. Install dependencies
```
   pip install -r requirements.txt
```
3. Create a `.env` file based on `.env.example`
4. Start the server
```
   uvicorn app.main:app --reload
```
5. Open http://127.0.0.1:8000


---

## What This Project Demonstrates

* End-to-end RAG system design
* Vector database usage
* Embedding-based semantic search
* Backend + UI integration
* Production-style error handling

# LLM-Powered Knowledge Assistant

## Overview

This project is a **minimal Retrieval-Augmented Generation (RAG) prototype** that demonstrates how to build an LLM-powered knowledge assistant using embeddings and a vector database. The system retrieves relevant information from stored documents and uses a Large Language Model (LLM) to generate grounded answers.

The primary goal of this repository is to showcase **practical, end-to-end LLM application development**, suitable for portfolio and interview discussions.

---

## Key Features

* LLM API integration for text generation
* Text embeddings for semantic search
* Vector database for document storage and retrieval
* Simple Retrieval-Augmented Generation (RAG) pipeline
* Modular, easy-to-extend project structure

---

## How Retrieval-Augmented Generation (RAG) Works

1. **Document Ingestion**

   * Text documents are converted into vector embeddings.
   * Embeddings are stored in a vector database.

2. **Query Processing**

   * A user question is converted into an embedding.
   * The vector database is queried to find the most relevant documents.

3. **Answer Generation**

   * Retrieved documents are injected into the LLM prompt as context.
   * The LLM generates an answer grounded in the retrieved information.

This approach reduces hallucinations and allows the model to answer questions using custom knowledge.

---

## Tech Stack

* **Python 3.10+**
* **OpenAI API** (LLM + embeddings)
* **ChromaDB** (vector database)
* **LangChain** (optional utilities)
* **python-dotenv** (environment variable management)

---

## Project Structure

```
llm-knowledge-assistant/
│
├── data/                 # Sample or ingested documents
├── scripts/
│   ├── test_llm.py       # Basic LLM API test
│   ├── embeddings_test.py# Embeddings + vector DB test
│   └── rag_minimal.py    # End-to-end RAG pipeline
├── .env                  # API keys (not committed)
├── .gitignore
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd llm-knowledge-assistant
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

* Windows:

```bash
venv\Scripts\activate
```

* macOS / Linux:

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install openai langchain chromadb python-dotenv jupyter
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

---

## Usage

### Test LLM Connectivity

```bash
python scripts/test_llm.py
```

Expected result: a short LLM-generated response printed to the terminal.

---

### Test Embeddings and Vector Search

```bash
python scripts/embeddings_test.py
```

Expected result: a document relevant to the test query is returned.

---

### Run Minimal RAG Pipeline

```bash
python scripts/rag_minimal.py
```

Expected result: an answer generated using retrieved contextual information.

---

## Example Use Case

* Internal knowledge assistant
* FAQ chatbot
* Document-based Q&A system
* Foundation for a web-based AI assistant

---

## Limitations

* Uses small sample text instead of large document ingestion
* No persistence layer for vector storage
* CLI-based interface only

These are intentional to keep the prototype minimal and focused.

---

## Future Improvements

* PDF / Markdown document ingestion
* Persistent vector database
* FastAPI backend
* Web UI (React or simple frontend)
* Authentication and usage limits

---

## Why This Project Matters

This project demonstrates:

* Practical LLM API usage
* Understanding of embeddings and semantic search
* Real-world RAG architecture
* Ability to design and implement AI systems beyond toy examples

It is suitable for **AI Engineer, Machine Learning Engineer, or Software Engineer** portfolios.

---

## License

MIT License

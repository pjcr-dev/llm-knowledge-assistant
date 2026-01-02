from app.services.embedding_service import embed_text
from app.db.vector_store import collection
from app.utils.file_loader import load_text_files
from app.utils.chunking import chunk_text
from pathlib import Path
import hashlib

DATA_DIR = Path("data/docs")

print("Ingesting documents...")

def document_id(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

existing_ids = set(collection.get()['ids'])

added = 0
updated = 0



for doc in load_text_files(DATA_DIR):
    
    doc_id = document_id(doc["id"])
    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc_id}_chunk_{i}"
        embedding = embed_text(chunk)

        collection.upsert(
            documents=[chunk],
            embeddings=[embedding],
            ids=[chunk_id],
            metadatas=[{"source": doc["source"], "chunk":i, "title": doc["id"]}]
        )

    updated+=1
    print(f"Ingested document: {doc["id"]}")

print(f"Documents ingested successfully. Updated: {updated}")
print("Document count:", collection.count())

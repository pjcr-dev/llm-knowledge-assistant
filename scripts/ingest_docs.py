from app.services.embedding_service import embed_text
from app.db.vector_store import collection
from app.utils.file_loader import load_text_files
from pathlib import Path
import hashlib

DATA_DIR = Path("data/docs")

print("Ingesting documents...")

old_documents = [
    "Leena is a sniper.",
    "Kai is Leena's brother.",
    "Leena likes Raz.",
    "Claude is Leena's commander."
]

def document_id(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

existing_ids = set(collection.get()['ids'])

added = 0
updated = 0

for doc in load_text_files(DATA_DIR):
    
    doc_id = document_id(doc["id"])
    embedding = embed_text(doc["text"])

    collection.upsert(
        documents=[doc["text"]],
        embeddings=[embedding],
        ids=[doc_id],
        metadatas=[{"source": doc["source"], "title": doc["id"]}]
    )

    updated+=1
    #print(f"Ingested document: {doc}")

print(f"Documents ingested successfully. Updated: {updated}")
print("Document count:", collection.count())

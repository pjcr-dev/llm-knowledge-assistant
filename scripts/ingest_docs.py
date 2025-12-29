from app.services.embedding_service import embed_text
from app.db.vector_store import collection
import hashlib

print("Ingesting documents...")

documents = [
    "Leena is a sniper.",
    "Kai is Leena's brother.",
    "Leena likes Raz.",
    "Claude is Leena's commander."
]

def document_id(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

existing_ids = set(collection.get()['ids'])

added = 0
skipped = 0

for doc in documents:
    
    doc_id = document_id(doc)

    if doc_id in existing_ids:
        skipped+=1
        continue

    embedding = embed_text(doc)
    collection.add(
        documents=[doc],
        embeddings=[embedding],
        ids=[doc_id]
    )

    added+=1
    #print(f"Ingested document: {doc}")

print(f"Documents ingested successfully. Added: {added}, Skipped (duplicates): {skipped}")
print("Document count:", collection.count())

from app.services.embedding_service import embed_text
from app.db.vector_store import collection

documents = [
    "Leena is a sniper.",
    "Kai is Leena's brother.",
    "Leena likes Raz.",
    "Claude is Leena's commander."
]

print("Ingesting documents...")

for i, doc in enumerate(documents):
    
    embedding = embed_text(doc)
    collection.add(
        documents=[doc],
        embeddings=[embedding],
        ids=[str(i)]
    )
    #print(f"Ingested document {i}: {doc}")

print("Documents ingested successfully.")
print("Document count:", collection.count())

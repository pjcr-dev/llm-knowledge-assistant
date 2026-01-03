import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("documents")

def add_documents(texts, embeddings):
    ids = [str(i) for i in range(len(texts))]
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )

#Now unused function, kept for reference
def query_documents(query_embedding, n_results=3):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
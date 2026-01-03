from app.services.embedding_service import embed_text
from app.services.llm_service import generate_answer
from collections import defaultdict
from app.db.vector_store import collection


def query_chunks(query_embedding, TOP_K=6):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"]
    )

MAX_DISTANCE = 1.2
def filter_results(results):
    filtered = []

    for doc, meta, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        if distance < MAX_DISTANCE:
            filtered.append({
                "text": doc, 
                "source": meta.get("source"),
                "title": meta.get("title"),
                "chunk": meta.get("chunk"),
                "distance": distance
            })

    return filtered

def group_by_source(chunks):
    grouped = defaultdict(list)

    for chunk in chunks:
        grouped[chunk["source"]].append(chunk)

    return grouped

MAX_CHUNKS_PER_DOC = 2
def select_best_chunks(grouped):
    selected = []

    for source, chunks in grouped.items():
        chunks = sorted(chunks, key=lambda x: x["distance"])
        selected.extend(chunks[:MAX_CHUNKS_PER_DOC])

    return selected

def build_context(chunks):
    context_parts = []

    for chunk in chunks:
        context_parts.append(f"[Source: {chunk['title']}]\n{chunk['text']}")

    return "\n\n".join(context_parts)


def answer_question(question: str, context) -> str:
    query_embedding = embed_text(question)
    results = query_chunks(query_embedding)

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""
    
    #print("Retrieved results: ", results)

    return generate_answer(prompt)
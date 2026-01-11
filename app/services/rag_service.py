from app.services.embedding_service import embed_text
from app.services.llm_service import generate_answer
from collections import defaultdict
from app.db.vector_store import collection
from app.core.logging import logger
from app.core.config import settings


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

        # print(f"[{meta['source']}] distance={distance:.4f}")
        # print(doc[:200])
        # print("----")
        
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


def answer_question(question: str) -> dict:

    if collection.count() == 0:

        logger.warning("Query attempted with empty knowledge base.")

        return {
            "answer": "The knowledge base is empty.",
            "sources": []
        }


    logger.info(f"Received query: {question}")
    raw_results = query_chunks(embed_text(question))
    logger.info("Retrieved %d chunks (unfiltered)", len(raw_results))

    filtered = filter_results(raw_results)

    if not filtered:

        logger.warning("No relevant documents found for query.")
        
        return {
            "answer": "I don't know based on the provided documents.",
            "sources": []
        }
        
    grouped = group_by_source(filtered)
    selected = select_best_chunks(grouped)
    context = build_context(selected)
    
    answer = generate_answer(question, context)
    sources = sorted({c["title"] for c in selected})

    if "i don't know" in answer.lower():
        logger.info("Model refused due to insufficient context.")

    elif not sources:
        logger.warning("Answer generated without sources.")

    if settings.debug:
        return {
            "answer": answer,
            "sources": sources,
            "debug": {"retrieved_chunks": raw_results}
        }

    return {
        "answer": answer,
        "sources": sources
    }
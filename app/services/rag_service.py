from app.services.embedding_service import embed_text
from app.db.vector_store import query_documents
from app.services.llm_service import generate_answer

def answer_question(question: str) -> str:
    query_embedding = embed_text(question)
    results = query_documents(query_embedding)

    context_docs = results["documents"][0]
    context = "\n".join(context_docs)

    prompt = f"""
Use the following context to answer the question.
If the answer is not contained within the context, respond with 'No relevant documents found'.
If the question is not related to the context, respond with 'No relevant documents found'.

Context:
{context}

Question:
{question}
"""
    
    print("Retrieved results: ", results)

    return generate_answer(prompt)
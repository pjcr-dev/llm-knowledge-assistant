from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb

load_dotenv()
client = OpenAI()
chroma = chromadb.Client()
collection = chroma.create_collection(name="docs")

# Embed documents ================================================

texts = [
    "Leena is a sniper.",
    "Kai is Leena's brother.",
    "Leena likes Raz.",
    "Claude is Leena's commander."
]

for i, text in enumerate(texts):
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(i)]
    )

# Embed query ===================================================

query = input("Ask a question about Leena: ")

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

# Generate answer ================================================

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

context = "\n".join(results["documents"][0])

print(results["documents"])

prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
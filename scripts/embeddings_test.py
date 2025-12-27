from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
chroma = chromadb.Client()
collection = chroma.create_collection(name="docs")

print("Starting embedding tests...")

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

query = "Who is Leena's sibling?"

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

print(results["documents"])
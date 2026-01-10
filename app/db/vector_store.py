import chromadb
from app.core.config import settings

client = chromadb.PersistentClient(path="./" + settings.chroma_persist_dir)

collection = client.get_or_create_collection("documents")
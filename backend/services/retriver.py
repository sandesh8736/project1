import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
client = chromadb.PersistentClient(path="./vector_store")

def retrieve_chunks(question, k=3):

    collection = client.get_collection(name="documents")

    # Convert question into embedding
    question_embedding = model.encode([question])[0]

    # Search ChromaDB
    results = collection.query(query_embeddings=[question_embedding.tolist()], n_results=k
    )

    return results
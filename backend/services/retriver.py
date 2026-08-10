from services.vector_store import collection
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_relevant_chunks(question, k=3):
    question_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=k,
    )

    # results["documents"] is a list-of-lists (one inner list per query) —
    # since we only sent 1 question, we want results["documents"][0]
    return results["documents"][0]
import numpy as np 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def find_top_k_chunks(question, chunks, chunk_embeddings, k=3):
    question_embedding = model.encode([question])
    Scores = cosine_similarity(question_embedding, chunk_embeddings)
    Scores = Scores[0]

    
    sorted_indices = np.argsort(Scores)[::-1]
    top_indices = sorted_indices[:k]

    top_chunks = [chunks[i] for i in top_indices]
    return top_chunks


 
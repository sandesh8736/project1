import numpy as np 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")

chunks= [
    "The refund policy allows returns within 30 days of purchase.",
    "Our office is located in downtown Kharagpur, open 9 to 5.",
    "Late payments incur a 5% penalty fee after a 10-day grace period.",
    "We offer free shipping on orders over $50.",
]

chunk_embeddings = model.encode(chunks)

question = "What happens if i pay later?"

question_embedding = model.encode([question])

arr =[]

print("CShape:" ,chunk_embeddings.shape)

print("QShape:", question_embedding.shape)

"""def find_best_chunk(question,chunks,chunk_embeddings):
    question_embedding = model.encode([question])
    scores = cosine_similarity(question_embedding, chunk_embeddings)
   # print("scores:",scores)
   # print("scores_shape :",scores.shape)
    match_index = np.argmax(scores)
    print("best matches" ,chunks[match_index])"""



def find_top_k_chunks(question, chunks, chunk_embeddings, k=3):
    question_embedding = model.encode([question])
    Scores = cosine_similarity(question_embedding, chunk_embeddings)
    Scores = Scores[0]
    print("scores_shape :",Scores.shape)
    sorted_indices = np.argsort(Scores)[::-1]
    top_3 = sorted_indices[:3]
    for i in top_3:
        print(Scores[i], "-", chunks[i])


find_top_k_chunks("What happens if I pay late?", chunks, chunk_embeddings)
find_top_k_chunks("Do you offer free delivery?", chunks, chunk_embeddings)
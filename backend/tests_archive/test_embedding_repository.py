import os

from services.database.postgres import PostgreSQL
from services.database.embedding_repository import (
    EmbeddingRepository
)
from sentence_transformers import SentenceTransformer


# -----------------------------------------
# Database
# -----------------------------------------

db = PostgreSQL(
    password=os.environ["DOCUMIND_DB_PASSWORD"]
)

repository = EmbeddingRepository(db)


# -----------------------------------------
# Embedding model
# -----------------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------------------
# Create embedding
# -----------------------------------------

text = """
Machine learning is a branch of artificial
intelligence that allows computers to learn
patterns from data.
"""

embedding = model.encode(text)

print("Embedding dimension:")
print(len(embedding))


# -----------------------------------------
# Store embedding
# -----------------------------------------

# NOTE: chunk_id=1 must already exist in the `chunks` table (FK constraint).
# Run test_document_repository.py first, or swap in a real chunk id here.
CHUNK_ID = 1

embedding_id = repository.create_embedding(
    chunk_id=CHUNK_ID,
    embedding=embedding  # repository converts numpy -> list internally
)

print("Embedding ID:", embedding_id)


# -----------------------------------------
# Read embedding
# -----------------------------------------

result = repository.get_embedding(
    chunk_id=CHUNK_ID
)

print("\nStored embedding:")
print(result)
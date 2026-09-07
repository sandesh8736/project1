from sentence_transformers import SentenceTransformer

from services.database.postgres import PostgreSQL
from services.database.embedding_repository import EmbeddingRepository


class PostgreSQLRetriever:

    def __init__(self, password):

        # Database connection
        self.db = PostgreSQL(password=password)

        # Embedding repository
        self.embedding_repository = EmbeddingRepository(self.db)

        # Same model used while storing embeddings
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # -----------------------------------------
    # Retrieve relevant chunks
    # -----------------------------------------

    def retrieve(self,question,k=3,document_id=None):

        if k <= 0:
            raise ValueError("k must be a positive integer")

        if document_id is None:
            raise ValueError("document_id is required for document-specific retrieval")

        # Convert question into embedding
 
        question_embedding = self.model.encode(question)

        # Search PostgreSQL
 
        results = (
            self.embedding_repository
            .search_similar_chunks(
                question_embedding,
                limit=k,
                document_id=document_id
            )
        )

        return results

    # -----------------------------------------
    # Return only text chunks
    # -----------------------------------------

    def retrieve_text(self,question,k=3,document_id=None):

        results = self.retrieve(question,k,document_id)

        # search_similar_chunks returns dict rows (see EmbeddingRepository),
        # so index by column name, not position.
        chunks = []

        for result in results:

            content = result["content"]

            chunks.append(
                content
            )

        return chunks
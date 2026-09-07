import logging

from services.database.postgres import PostgreSQL
from services.database.document_repository import DocumentRepository
from services.database.embedding_repository import EmbeddingRepository

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class IngestionService:

    def __init__(self, password):

        # ---------------------------------
        # Database
        # ---------------------------------

        self.db = PostgreSQL(
            password=password
        )

        # ---------------------------------
        # Repositories
        # ---------------------------------

        self.document_repository = (
            DocumentRepository(self.db)
        )

        self.embedding_repository = (
            EmbeddingRepository(self.db)
        )

        # ---------------------------------
        # Embedding model
        # ---------------------------------

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    # -----------------------------------------
    # Get or create a user (idempotent by email)
    # -----------------------------------------

    def get_or_create_user(self, name, email):
        """
        Looks up a user by email, creating one if it doesn't exist yet.
        Requires a UNIQUE constraint on users.email.
        """

        query = """
            INSERT INTO users
            (
                name,
                email
            )

            VALUES
            (
                %s,
                %s
            )

            ON CONFLICT (email)
            DO UPDATE SET name = EXCLUDED.name

            RETURNING id;
        """

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(query, (name, email))

                user_id = cursor.fetchone()[0]

            connection.commit()

        return user_id

    # -----------------------------------------
    # Process document
    # -----------------------------------------

    def ingest_document(
        self,
        user_id,
        title,
        file_path,
        file_type,
        file_size,
        pages
    ):
        """
        Runs the entire ingestion (document, pages, chunks, embeddings) inside
        a single transaction. If anything fails partway through, everything
        rolls back instead of leaving a half-written document behind.
        """

        print("\nStarting document ingestion...")

        with self.db.connect() as connection:

            try:
                # ---------------------------------
                # 1. Create document
                # ---------------------------------

                document_id = (
                    self.document_repository.create_document(
                        user_id=user_id,
                        title=title,
                        file_path=file_path,
                        file_type=file_type,
                        file_size=file_size,
                        connection=connection
                    )
                )

                print(
                    "Document created:",
                    document_id
                )

                # ---------------------------------
                # 2. Process pages
                # ---------------------------------

                total_chunks = 0

                for page in pages:

                    page_number = page["page_number"]

                    text = page.get(
                        "text",
                        ""
                    )

                    # ---------------------------------
                    # Create page
                    # ---------------------------------

                    page_id = (
                        self.document_repository.create_page(
                            document_id=document_id,
                            page_number=page_number,
                            text_content=text,
                            connection=connection
                        )
                    )

                    print(
                        f"Page {page_number} stored:",
                        page_id
                    )

                    # ---------------------------------
                    # Create chunks
                    # ---------------------------------

                    chunks = self.create_chunks(
                        text
                    )

                    for chunk in chunks:

                        chunk_id = (
                            self.document_repository.create_chunk(
                                document_id=document_id,
                                page_id=page_id,
                                chunk_type="text",
                                content=chunk,
                                chunk_index=total_chunks,
                                connection=connection
                            )
                        )

                        # ---------------------------------
                        # Generate + store embedding
                        # ---------------------------------

                        embedding = (
                            self.embedding_model.encode(
                                chunk
                            )
                        )

                        self.embedding_repository.create_embedding(
                            chunk_id=chunk_id,
                            embedding=embedding,
                            connection=connection
                        )

                        total_chunks += 1

                # Everything succeeded -> commit the whole ingestion at once
                connection.commit()

            except Exception:
                connection.rollback()
                logger.exception("Ingestion failed for document '%s' — rolled back.", title)
                raise

        print("\nDocument ingestion completed.")

        print(
            "Document ID:",
            document_id
        )

        print(
            "Total chunks:",
            total_chunks
        )

        return {
            "document_id": document_id,
            "chunks": total_chunks
        }

    # -----------------------------------------
    # Chunk text
    # -----------------------------------------

    def create_chunks(self,text,chunk_size=1000,overlap=200):

        if not text:
            return []

        if chunk_size <= overlap:
            raise ValueError("chunk_size must be greater than overlap")

        chunks = []

        start = 0

        text_length = len(text)

        while start < text_length:

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append(
                chunk
            )

            start = end - overlap

        return chunks
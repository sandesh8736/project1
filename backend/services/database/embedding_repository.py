import logging

from contextlib import contextmanager

from psycopg.rows import dict_row

from services.database.postgres import PostgreSQL

logger = logging.getLogger(__name__)


class EmbeddingRepository:

    def __init__(self, db):
        self.db = db

    # -----------------------------------------
    # Shared query execution helper
    # -----------------------------------------

    @contextmanager
    def _connection_scope(self, connection=None):
        """
        If an external `connection` is passed in, reuse it and let the
        caller manage commit/rollback/close (used when several repository
        calls need to share one transaction, e.g. during ingestion).

        Otherwise open a short-lived connection, commit, and close it here.
        """

        if connection is not None:
            yield connection, False  # False = don't commit/close, caller owns it
            return

        with self.db.connect() as own_connection:
            yield own_connection, True  # True = commit/close here

    def _execute(self, query, params, fetch_one=False, fetch_all=False, connection=None):
        """
        Runs a single query.

        connection -> reuse an existing connection/transaction instead of
                      opening a new one (pass this to share a transaction
                      across multiple repository calls)
        fetch_one  -> returns a single dict row (or None)
        fetch_all  -> returns a list of dict rows
        neither    -> returns None (use for INSERT/UPDATE with no RETURNING)
        """

        try:
            with self._connection_scope(connection) as (conn, owns_connection):

                with conn.cursor(row_factory=dict_row) as cursor:

                    cursor.execute(query, params)

                    result = None

                    if fetch_one:
                        result = cursor.fetchone()

                    elif fetch_all:
                        result = cursor.fetchall()

                if owns_connection:
                    conn.commit()

            return result

        except Exception:
            logger.exception("Query failed: %s | params=%s", query.strip().splitlines()[0], params)
            raise

    # -----------------------------------------
    # Store embedding
    # -----------------------------------------

    def create_embedding(self, chunk_id, embedding, connection=None):

        # pgvector needs a plain list/sequence of floats, not a numpy array.
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()

        query = """
            INSERT INTO embeddings
            (
                chunk_id,
                embedding
            )

            VALUES
            (
                %s,
                %s
            )

            RETURNING id;
        """

        row = self._execute(query,(chunk_id,embedding),fetch_one=True,connection=connection)

        return row["id"]

    # -----------------------------------------
    # Get embedding
    # -----------------------------------------

    def get_embedding(self, chunk_id, connection=None):

        query = """
            SELECT
                id,
                chunk_id,
                embedding,
                created_at

            FROM embeddings

            WHERE chunk_id = %s;
        """

        return self._execute(
            query,
            (chunk_id,),
            fetch_one=True,
            connection=connection
        )

    # -----------------------------------------
    # Similarity search
    # -----------------------------------------

    def search_similar_chunks(self,query_embedding,limit=5,document_id=None,connection=None):

        if hasattr(query_embedding, "tolist"):
            query_embedding = query_embedding.tolist()

        query = """
            SELECT
                chunks.id,
                chunks.document_id,
                documents.title,
                chunks.page_id,
                document_pages.page_number,
                chunks.chunk_type,
                chunks.content,
                chunks.chunk_index,
                embeddings.embedding <=> %s::vector AS distance

            FROM embeddings

            JOIN chunks
                ON chunks.id = embeddings.chunk_id

            JOIN documents
                ON documents.id = chunks.document_id

            LEFT JOIN document_pages
                ON document_pages.id = chunks.page_id

            WHERE chunks.document_id = %s 

            ORDER BY distance

            LIMIT %s;
        """

        return self._execute(query,(query_embedding,document_id,limit),
            fetch_all=True,connection=connection)

    

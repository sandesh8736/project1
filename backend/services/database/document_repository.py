import logging

from contextlib import contextmanager

from psycopg.rows import dict_row

from services.database.postgres import PostgreSQL

logger = logging.getLogger(__name__)


class DocumentRepository:

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
    # Create document
    # -----------------------------------------

    def create_document(
        self,
        user_id,
        title,
        file_path,
        file_type,
        file_size,
        connection=None
    ):

        query = """
            INSERT INTO documents
            (
                user_id,
                title,
                file_path,
                file_type,
                file_size
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )

            RETURNING id;
        """

        row = self._execute(
            query,
            (
                user_id,
                title,
                file_path,
                file_type,
                file_size
            ),
            fetch_one=True,
            connection=connection
        )

        return row["id"]

    # -----------------------------------------
    # Create page
    # -----------------------------------------

    def create_page(
        self,
        document_id,
        page_number,
        text_content,
        connection=None
    ):

        query = """
            INSERT INTO document_pages
            (
                document_id,
                page_number,
                text_content
            )

            VALUES
            (
                %s,
                %s,
                %s
            )

            RETURNING id;
        """

        row = self._execute(
            query,
            (
                document_id,
                page_number,
                text_content
            ),
            fetch_one=True,
            connection=connection
        )

        return row["id"]

    # -----------------------------------------
    # Create chunk
    # -----------------------------------------

    def create_chunk(
        self,
        document_id,
        page_id,
        chunk_type,
        content,
        chunk_index,
        connection=None
    ):

        query = """
            INSERT INTO chunks
            (
                document_id,
                page_id,
                chunk_type,
                content,
                chunk_index
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )

            RETURNING id;
        """

        row = self._execute(
            query,
            (
                document_id,
                page_id,
                chunk_type,
                content,
                chunk_index
            ),
            fetch_one=True,
            connection=connection
        )

        return row["id"]

    # -----------------------------------------
    # Get document
    # -----------------------------------------

    def get_document(self, document_id, connection=None):

        query = """
            SELECT
                id,
                user_id,
                title,
                file_path,
                file_type,
                file_size,
                uploaded_at

            FROM documents

            WHERE id = %s;
        """

        return self._execute(
            query,
            (document_id,),
            fetch_one=True,
            connection=connection
        )

    # -----------------------------------------
    # Get document pages
    # -----------------------------------------

    def get_pages(self, document_id, connection=None):

        query = """
            SELECT
                id,
                page_number,
                text_content

            FROM document_pages

            WHERE document_id = %s

            ORDER BY page_number;
        """

        return self._execute(
            query,
            (document_id,),
            fetch_all=True,
            connection=connection
        )

    # -----------------------------------------
    # Get document chunks
    # -----------------------------------------

    def get_chunks(self, document_id, connection=None):

        query = """
            SELECT
                id,
                page_id,
                chunk_type,
                content,
                chunk_index

            FROM chunks

            WHERE document_id = %s

            ORDER BY chunk_index;
        """

        return self._execute(
            query,
            (document_id,),
            fetch_all=True,
            connection=connection
        )
from services.database.postgres import PostgreSQL


class DatabaseSchema:

    def __init__(self, db):

        self.db = db

    def create_extension(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE EXTENSION IF NOT EXISTS vector;
                    """
                )

            connection.commit()

        print("pgvector extension ready.")

    def create_users_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (

                        id BIGSERIAL PRIMARY KEY,

                        name VARCHAR(255) NOT NULL,

                        email VARCHAR(255)
                            UNIQUE NOT NULL,

                        password_hash TEXT NOT NULL,

                        created_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )

            connection.commit()

        print("use    rs table ready.")

    def create_documents_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS documents (

                        id BIGSERIAL PRIMARY KEY,

                        user_id BIGINT NOT NULL,

                        title VARCHAR(500) NOT NULL,

                        file_path TEXT NOT NULL,

                        file_type VARCHAR(50),

                        file_size BIGINT,

                        uploaded_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT fk_documents_user

                            FOREIGN KEY (user_id)

                            REFERENCES users(id)

                            ON DELETE CASCADE
                    );
                    """
                )

            connection.commit()

        print("documents table ready.")

    def create_document_pages_table(self):

            with self.db.connect() as connection:

                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS document_pages (

                            id BIGSERIAL PRIMARY KEY,

                            document_id BIGINT NOT NULL,

                            page_number INTEGER NOT NULL,

                            text_content TEXT,

                            created_at TIMESTAMP
                                DEFAULT CURRENT_TIMESTAMP,

                            CONSTRAINT fk_pages_document

                                FOREIGN KEY (document_id)

                                REFERENCES documents(id)

                                ON DELETE CASCADE,

                            CONSTRAINT unique_document_page

                                UNIQUE (
                                    document_id,
                                    page_number
                                )
                        );
                        """
                    )

                connection.commit()

            print("document_pages table ready.")

    def create_chunks_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS chunks (

                        id BIGSERIAL PRIMARY KEY,

                        document_id BIGINT NOT NULL,

                        page_id BIGINT,

                        chunk_type VARCHAR(20) NOT NULL,

                        content TEXT NOT NULL,

                        chunk_index INTEGER NOT NULL,

                        created_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT fk_chunks_document

                            FOREIGN KEY (document_id)

                            REFERENCES documents(id)

                            ON DELETE CASCADE,

                        CONSTRAINT fk_chunks_page

                            FOREIGN KEY (page_id)

                            REFERENCES document_pages(id)

                            ON DELETE CASCADE,

                        CONSTRAINT valid_chunk_type

                            CHECK (
                                chunk_type IN (
                                    'text',
                                    'image',
                                    'table'
                                )
                            ),

                        CONSTRAINT unique_chunk_index

                            UNIQUE (
                                document_id,
                                chunk_index
                            )
                    );
                    """
                )

            connection.commit()

        print("chunks table ready.")

    def create_embeddings_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS embeddings (

                        id BIGSERIAL PRIMARY KEY,

                        chunk_id BIGINT
                            UNIQUE NOT NULL,

                        embedding VECTOR(384)
                            NOT NULL,

                        created_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT fk_embedding_chunk

                            FOREIGN KEY (chunk_id)

                            REFERENCES chunks(id)

                            ON DELETE CASCADE
                    );
                    """
                )

            connection.commit()

        print("embeddings table ready.")

    def create_images_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS images (

                        id BIGSERIAL PRIMARY KEY,

                        document_id BIGINT NOT NULL,

                        page_id BIGINT,

                        image_index INTEGER NOT NULL,

                        image_path TEXT,

                        image_description TEXT,

                        created_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT fk_images_document

                            FOREIGN KEY (document_id)

                            REFERENCES documents(id)

                            ON DELETE CASCADE,

                        CONSTRAINT fk_images_page

                            FOREIGN KEY (page_id)

                            REFERENCES document_pages(id)

                            ON DELETE CASCADE
                    );
                    """
                )

            connection.commit()

        print("images table ready.")

    def create_tables_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS document_tables (

                        id BIGSERIAL PRIMARY KEY,

                        document_id BIGINT NOT NULL,

                        page_id BIGINT,

                        table_index INTEGER NOT NULL,

                        content JSONB,

                        created_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT fk_tables_document

                            FOREIGN KEY (document_id)

                            REFERENCES documents(id)

                            ON DELETE CASCADE,

                        CONSTRAINT fk_tables_page

                            FOREIGN KEY (page_id)

                            REFERENCES document_pages(id)

                            ON DELETE CASCADE
                    );
                    """
                )

            connection.commit()

        print("document_tables table ready.")

    def create_query_logs_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS query_logs (

                        id BIGSERIAL PRIMARY KEY,

                        user_id BIGINT,

                        query TEXT NOT NULL,

                        response TEXT,

                        created_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT fk_query_user

                            FOREIGN KEY (user_id)

                            REFERENCES users(id)

                            ON DELETE SET NULL
                    );
                    """
                )

            connection.commit()

        print("query_logs table ready.")

    def create_settings_table(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS settings (

                        id BIGSERIAL PRIMARY KEY,

                        key VARCHAR(255)
                            UNIQUE NOT NULL,

                        value TEXT,

                        updated_at TIMESTAMP
                            DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )

            connection.commit()

        print("settings table ready.")

    def create_indexes(self):

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_documents_user_id

                    ON documents(user_id);
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_pages_document_id

                    ON document_pages(document_id);
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_chunks_document_id

                    ON chunks(document_id);
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_chunks_page_id

                    ON chunks(page_id);
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_images_document_id

                    ON images(document_id);
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_tables_document_id

                    ON document_tables(document_id);
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_query_logs_user_id

                    ON query_logs(user_id);
                    """
                )

            connection.commit()

        print("Indexes created.")

    def create_all(self):

        print("\nCreating Documind AI database schema...\n")

        self.create_extension()

        self.create_users_table()

        self.create_documents_table()

        self.create_document_pages_table()

        self.create_chunks_table()

        self.create_embeddings_table()

        self.create_images_table()

        self.create_tables_table()

        self.create_query_logs_table()

        self.create_settings_table()

        self.create_indexes()

        print(
            "\nDatabase schema created successfully."
        )
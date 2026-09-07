class PostgresVectorStore:

    def __init__(self, db):

        self.db = db

    def store_chunks(
        self,
        document_name,
        chunks,
        embeddings
    ):

        if len(chunks) != len(embeddings):

            raise ValueError(
                "Number of chunks and embeddings must be equal."
            )

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                for chunk, embedding in zip(
                    chunks,
                    embeddings
                ):

                    page_number = chunk.get(
                        "page_number"
                    )

                    chunk_type = chunk.get(
                        "type",
                        "text"
                    )

                    content = chunk.get(
                        "content",
                        ""
                    )

                    embedding_list = embedding.tolist()

                    cursor.execute(
                        """
                        INSERT INTO document_chunks
                        (
                            document_name,
                            page_number,
                            chunk_type,
                            content,
                            embedding
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                        """,
                        (
                            document_name,
                            page_number,
                            chunk_type,
                            content,
                            embedding_list
                        )
                    )

            connection.commit()

        print(
            f"{len(chunks)} chunks stored successfully."
        )

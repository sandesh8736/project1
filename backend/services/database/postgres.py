import psycopg

from pgvector.psycopg import register_vector


class PostgreSQL:

    def __init__(
        self,
        host="localhost",
        port=5432,
        database="documind_ai",
        user="postgres",
        password="Documind@123"
    ):

        self.connection_string = (
            f"host={host} "
            f"port={port} "
            f"dbname={database} "
            f"user={user} "
            f"password={password}"
        )

    def connect(self):

        connection = psycopg.connect(
            self.connection_string
        )

        register_vector(connection)

        return connection

    def test_connection(self):

        try:

            with self.connect():

                print(
                    "PostgreSQL connected successfully."
                )

        except Exception as error:

            print(
                "PostgreSQL connection failed:"
            )

            print(error)
import unittest
from unittest.mock import MagicMock

from services.database.postgres_vector_store import PostgresVectorStore


class Embedding:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return self.values


class PostgresVectorStoreTests(unittest.TestCase):
    def test_store_chunks_inserts_each_chunk_and_commits(self):
        db = MagicMock()
        connection = db.connect.return_value.__enter__.return_value
        cursor = connection.cursor.return_value.__enter__.return_value
        chunks = [
            {
                "type": "text",
                "page_number": 1,
                "content": "Machine learning is a branch of AI.",
            },
            {
                "type": "image",
                "page_number": 2,
                "content": "A neural network diagram.",
            },
        ]
        embeddings = [Embedding([0.1, 0.2]), Embedding([0.3, 0.4])]

        PostgresVectorStore(db).store_chunks(
            document_name="test.pdf",
            chunks=chunks,
            embeddings=embeddings,
        )

        self.assertEqual(cursor.execute.call_count, 2)
        self.assertEqual(
            cursor.execute.call_args_list[0].args[1],
            ("test.pdf", 1, "text", chunks[0]["content"], [0.1, 0.2]),
        )
        self.assertEqual(
            cursor.execute.call_args_list[1].args[1],
            ("test.pdf", 2, "image", chunks[1]["content"], [0.3, 0.4]),
        )
        connection.commit.assert_called_once_with()

    def test_store_chunks_rejects_mismatched_embeddings(self):
        db = MagicMock()

        with self.assertRaisesRegex(
            ValueError, "Number of chunks and embeddings must be equal"
        ):
            PostgresVectorStore(db).store_chunks(
                document_name="test.pdf",
                chunks=[{"content": "one"}],
                embeddings=[],
            )

        db.connect.assert_not_called()


if __name__ == "__main__":
    unittest.main()

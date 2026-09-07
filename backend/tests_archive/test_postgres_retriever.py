import os

from services.database.postgres_retriever import (
    PostgreSQLRetriever
)


# -----------------------------------------
# Create retriever
# -----------------------------------------

retriever = PostgreSQLRetriever(
    password=os.environ["DOCUMIND_DB_PASSWORD"]
)


# -----------------------------------------
# Ask question
# -----------------------------------------

question = input(
    "Ask a question: "
)


# -----------------------------------------
# Retrieve chunks
# -----------------------------------------

results = retriever.retrieve(
    question,
    k=3
)


# -----------------------------------------
# Display results
# -----------------------------------------

if not results:
    print("\nNo chunks found. Have you run ingestion yet?")

else:
    print("\nRetrieved chunks:\n")

    for i, result in enumerate(
        results,
        start=1
    ):
        print("=" * 60)
        print(
            f"Result {i}"
        )
        print(
            "Chunk ID:",
            result["id"]
        )
        print(
            "Document ID:",
            result["document_id"]
        )
        print(
            "Page ID:",
            result["page_id"]
        )
        print(
            "Chunk type:",
            result["chunk_type"]
        )
        print(
            "Distance:",
            result["distance"]
        )
        print(
            "\nContent:"
        )
        print(
            result["content"]
        )
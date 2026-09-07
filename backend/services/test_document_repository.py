import os

from services.database.postgres import PostgreSQL
from services.database.document_repository import DocumentRepository


db = PostgreSQL(password=os.environ["DOCUMIND_DB_PASSWORD"],)


repository = DocumentRepository(db)


# ----------------------------------------- 
# Create test user
# -----------------------------------------

with db.connect() as connection:

    with connection.cursor() as cursor:

        cursor.execute(
            """
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
            """,
            (
                "Test User",
                "test@documind.ai"
            )
        )

        user_id = cursor.fetchone()[0]

    connection.commit()


print("User ID:", user_id)


# -----------------------------------------
# Create document
# -----------------------------------------

document_id = repository.create_document(
    user_id=user_id,
    title="Machine Learning.pdf",
    file_path="uploads/Machine Learning.pdf",
    file_type="application/pdf",
    file_size=102400
)

print("Document ID:", document_id)


# -----------------------------------------
# Create page
# -----------------------------------------

page_id = repository.create_page(
    document_id=document_id,
    page_number=1,
    text_content="Machine learning is a branch of artificial intelligence."
)

print("Page ID:", page_id)


# -----------------------------------------
# Create chunks
# -----------------------------------------

chunk1 = repository.create_chunk(
    document_id=document_id,
    page_id=page_id,
    chunk_type="text",
    content="Machine learning is a branch of artificial intelligence.",
    chunk_index=0
)

chunk2 = repository.create_chunk(
    document_id=document_id,
    page_id=page_id,
    chunk_type="text",
    content="Machine learning algorithms learn patterns from data.",
    chunk_index=1
)


print("Chunk 1 ID:", chunk1)
print("Chunk 2 ID:", chunk2)


# -----------------------------------------
# Read document
# -----------------------------------------

document = repository.get_document(
    document_id
)

print("\nDocument:")
print(document)


# -----------------------------------------
# Read pages
# -----------------------------------------

pages = repository.get_pages(
    document_id
)

print("\nPages:")

for page in pages:
    print(page)


# -----------------------------------------
# Read chunks
# -----------------------------------------

chunks = repository.get_chunks(
    document_id
)

print("\nChunks:")

for chunk in chunks:
    print(chunk)
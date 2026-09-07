from services.read import PDF_reader
from services.ingestion_service import IngestionService
import os


# -----------------------------------------
# PDF path
# -----------------------------------------

PDF_PATH = "uploads/model_testing_sample (1).pdf"


# -----------------------------------------
# Check PDF exists
# -----------------------------------------

if not os.path.exists(PDF_PATH):

    print("PDF not found:")
    print(PDF_PATH)

    exit()


# -----------------------------------------
# Read PDF
# -----------------------------------------

reader = PDF_reader(
    file_path=PDF_PATH
)

full_text = reader.read_pdf()

print("\nPDF reading successful.")

print(
    "Total characters:",
    len(full_text)
)


# -----------------------------------------
# Convert text into pages
# -----------------------------------------
#
# Your current PDF_reader returns only
# full_text, so we temporarily create
# one page entry for testing.
#
# We will fix this properly afterward.
# -----------------------------------------

pages = [
    {
        "page_number": 1,
        "text": full_text
    }
]


# -----------------------------------------
# Create IngestionService
# -----------------------------------------

ingestion = IngestionService(
    password="Documind@123"
)


# -----------------------------------------
# Get / Create user
# -----------------------------------------

user_id = ingestion.get_or_create_user(
    name="Test User",
    email="test@documind.ai"
)

print(
    "\nUser ID:",
    user_id
)


# -----------------------------------------
# Ingest document
# -----------------------------------------

result = ingestion.ingest_document(

    user_id=user_id,

    title="Book.pdf",

    file_path=PDF_PATH,

    file_type="application/pdf",

    file_size=os.path.getsize(PDF_PATH),

    pages=pages
)


# -----------------------------------------
# Display result
# -----------------------------------------

print("\n==============================")
print("INGESTION RESULT")
print("==============================")

print(
    "Document ID:",
    result["document_id"]
)

print(
    "Total chunks:",
    result["chunks"]
)

print("\nIngestion successful!")
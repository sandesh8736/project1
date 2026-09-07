from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from services.read import PDF_reader
from services.ingestion_service import IngestionService
from services.postgres_rag import PostgreSQLRAG


app = FastAPI()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("uploads", exist_ok=True)

ingestion = IngestionService(password="Documind@123")

rag = PostgreSQLRAG(postgres_password="Documind@123",hf_token=None)
 
# Test API
# -------------------------

@app.get("/api/test")
def test():

    return {
        "message": "Hello from Documind AI"
    }


# -------------------------
# Upload PDF
# -------------------------

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read PDF page by page
    pdf_parser = PDF_reader(file_path)

    pages = pdf_parser.read_pdf()

    # Create document, pages, chunks and embeddings
    result = ingestion.ingest_document(
        user_id=1,
        title=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=os.path.getsize(file_path),
        pages=pages
    )

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "document_id": result["document_id"],
        "chunks": result["chunks"]
    }

# -------------------------
# Ask Question
# -------------------------

class QuestionRequest(BaseModel):
    question: str
    document_id: int



@app.post("/ask")
async def ask_question(request: QuestionRequest):

    result = rag.answer_question(
        request.question,
        k=3,
        document_id=request.document_id
    )

    return result
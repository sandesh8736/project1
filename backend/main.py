from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import os
import shutil

from services.auth_service import AuthService
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

auth_service = AuthService(password="Documind@123")

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        user_id = auth_service.get_user_id_from_token(token)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return user_id
 
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
async def upload_file(
    file: UploadFile = File(...),
    current_user_id:int = Depends(get_current_user)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read PDF page by page
    pdf_parser = PDF_reader(file_path)

    pages = pdf_parser.read_pdf()

    # Create document, pages, chunks and embeddings
    result = ingestion.ingest_document(
        user_id=current_user_id,
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
async def ask_question(
    request: QuestionRequest,
    current_user_id: int = Depends(get_current_user)
):
    result = rag.answer_question(
        request.question,
        k=3,
        document_id=request.document_id
    )

    return result

class RegisterRequest(BaseModel):

    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


@app.post("/auth/register")
async def register_user(request: RegisterRequest):

    try:

        user = auth_service.create_user(
            name=request.name,
            email=request.email,
            password=request.password
        )

        return {
            "message": "Registration successful",
            "user": user
        }

    except Exception as error:

        if "duplicate key" in str(error).lower():

            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        raise


@app.post("/auth/login")
async def login_user(request: LoginRequest):

    user = auth_service.authenticate_user(
        email=request.email,
        password=request.password
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = auth_service.create_access_token(
        user_id=user["id"]
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }
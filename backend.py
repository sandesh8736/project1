from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from services.read import read_pdf
from services.chunks import create_chunks
from services.embeddings import generate_embeddings
from services.vector_store import store_embeddings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/test")
def test():
    return {
        "message": "Hello from FastAPI"
    }

if not os.path.exists("uploads"):
    os.mkdir("uploads")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # readpdf
    full_text = read_pdf(file_path) 

    # create chunks
    chunks = create_chunks(full_text)

    # generate embeddings 
    embeddings = generate_embeddings(chunks)

    # store embeddings 
    store_embeddings(chunks,embeddings)

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "location": file_path,
        "total_chunks": len(chunks),
       # "status": "Embeddings stored successfully"
        
    }
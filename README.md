# DocuMind AI

DocuMind AI lets you upload a PDF and ask questions about its contents. It
extracts text from the PDF, splits it into chunks, stores vector embeddings in
ChromaDB, retrieves relevant chunks for each question, and uses a Hugging Face
language model to generate an answer.

## Tech stack

- Frontend: React, Create React App, Tailwind CSS, Lucide icons
- Backend: FastAPI and Uvicorn
- PDF processing: pypdf
- Embeddings: Sentence Transformers (`all-MiniLM-L6-v2`)
- Vector database: ChromaDB
- Answers: Hugging Face Inference API (`Qwen/Qwen2.5-7B-Instruct`)

## Project structure

```text
Documind_Ai/
├── backend/
│   ├── main.py                 # FastAPI routes
│   ├── requirements.txt
│   └── services/               # PDF, chunking, embedding, retrieval, RAG
└── my-app/
    └── src/                    # React user interface
```

## Prerequisites

- Python 3.10 or later
- Node.js 18 or later
- A Hugging Face access token with permission to use the selected inference
  model

## Run locally

### 1. Configure the backend

From the project root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env` and add your Hugging Face token:

```env
HF_TOKEN=your_hugging_face_token
```

Start the API:

```bash
uvicorn main:app --reload
```

The backend will be available at `http://127.0.0.1:8000`. Interactive API
documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Configure the frontend

Open a second terminal from the project root:

```bash
cd my-app
npm install
npm start
```

Open `http://localhost:3000`, upload a PDF, then ask questions in the chat
box.

## API

### `GET /api/test`

Checks that the API is running.

### `POST /upload`

Uploads and indexes a PDF. Send multipart form data with a `file` field.

```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@/path/to/document.pdf"
```

### `POST /ask`

Asks a question about the indexed document.

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the main topic of this document?"}'
```

## Current behavior and limitations

- Uploading a new PDF replaces the previously indexed document.
- The current interface is configured for local development: frontend on port
  `3000` and backend on port `8000`.
- Image-only/scanned PDFs need OCR before their text can be indexed.
- `uploads/`, ChromaDB data, virtual environments, and `.env` files are
  intentionally excluded from Git.

## Useful commands

```bash
# Run the frontend test suite
cd my-app && npm test

# Create a production frontend build
cd my-app && npm run build
```

## Security note

Never commit your `.env` file or Hugging Face token. Use environment variables
or a secret manager when deploying the application.

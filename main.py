from services. read_pdf import read_pdf
from services.chunks import create_chunks
from services.embeddings import generate_embeddings

full_text = read_pdf("uploads/Book.pdf")

chunks = create_chunks(full_text)

embeddings = generate_embeddings(chunks)
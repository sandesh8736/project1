 

def create_chunks(full_text):
    chunk_size = 1000
    overlap = 200

    chunks = []

    start = 0

    while start < len(full_text):

        end = start + chunk_size

        chunk = full_text[start:end]

        chunks.append(chunk)

        start = start + chunk_size - overlap

    return chunks

 

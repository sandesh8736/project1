from pathlib import Path

from services.multimodal.multimodal_processor import MultimodalProcessor
from services.multimodal.multimodal_chunker import MultimodalChunker
from services.multimodal.multimodal_embeddings import MultimodalEmbeddings


uploads_dir = Path(__file__).parent / "uploads"


def get_uploaded_pdf():
    pdf_files = [
        path for path in uploads_dir.glob("*.pdf")
        if path.is_file() and path.stat().st_size > 0
    ]
    if not pdf_files:
        raise FileNotFoundError(
            f"No non-empty PDF files found in upload folder: {uploads_dir}"
        )

    return max(pdf_files, key=lambda path: path.stat().st_mtime)


def main():
    pdf_path = get_uploaded_pdf()
    print(f"Processing PDF: {pdf_path.name}")

    # STEP 1: Process PDF
    document_data = MultimodalProcessor(pdf_path).process()

    # STEP 2: Create chunks
    chunks = MultimodalChunker(document_data).process()
    print("\nTotal chunks:", len(chunks))

    # STEP 3: Create embeddings
    embeddings = MultimodalEmbeddings().generate_embeddings(chunks)

    # STEP 4: Verify
    print("\n==========================")
    print("EMBEDDING TEST")
    print("==========================")
    print("Chunks:", len(chunks))
    print("Embeddings:", len(embeddings))

    if len(embeddings) > 0:
        print("Dimension:", len(embeddings[0]))
        print("\nFirst embedding:")
        print(embeddings[0][:10])


if __name__ == "__main__":
    main()

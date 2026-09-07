from pathlib import Path

from services.multimodal.multimodal_processor import MultimodalProcessor
from services.multimodal.multimodal_chunker import MultimodalChunker


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

    processor = MultimodalProcessor(pdf_path)
    document_data = processor.process()

    chunker = MultimodalChunker(document_data)
    chunks = chunker.process()

    print("\n==========================")
    print("MULTIMODAL CHUNKS")
    print("==========================")
    print("Total chunks:", len(chunks))

    for index, chunk in enumerate(chunks, start=1):
        print("\n--------------------------")
        print("Chunk:", index)
        print("Type:", chunk["type"])
        print("Page:", chunk["page_number"])
        print("Content:", chunk["content"][:300])


if __name__ == "__main__":
    main()

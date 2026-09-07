from services.multimodal.pdf_processor import PDFProcessor


pdf_path = "uploads/Book.pdf"


processor = PDFProcessor(pdf_path)

pages = processor.process()


print("\nProcessing completed.")

for page in pages[:5]:

    print("\nPage:", page["page_number"])
    print("Text characters:", len(page["text"]))
    print("Images:", page["image_count"])
import argparse

from services.multimodal.ocr import PDFOCR


def main():
    parser = argparse.ArgumentParser(description="OCR pages without embedded text.")
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default="uploads/Make-Time .pdf",
        help="Path to the PDF to process.",
    )
    parser.add_argument(
        "--lang",
        default="eng",
        help="Installed Tesseract language code (default: eng).",
    )
    args = parser.parse_args()

    results = PDFOCR(args.pdf_path, language=args.lang).process()

    print("\nOCR processing completed.")
    print("Pages processed with OCR:", len(results))

    for result in results:
        print("\n------------------------")
        print("Page:", result["page_number"])
        print("Text:")
        print(result["text"][:1000])


if __name__ == "__main__":
    main()

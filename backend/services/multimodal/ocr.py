import io
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image


class PDFOCR:

    def __init__(self, pdf_path, language="eng"):
        self.pdf_path = Path(pdf_path)
        self.language = language
        self.document = None
        self.ocr_text = []

    def open_pdf(self):
        if not self.pdf_path.is_file():
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")

        available_languages = pytesseract.get_languages(config="")
        if self.language not in available_languages:
            available = ", ".join(available_languages)
            raise RuntimeError(
                f"Tesseract language '{self.language}' is not installed. "
                f"Available languages: {available}"
            )

        self.document = pymupdf.open(self.pdf_path)

        print(
            "Total pages:",
            len(self.document)
        )

    def process_pages(self):
        if self.document is None:
            raise RuntimeError("Open the PDF before processing pages.")

        for page_number, page in enumerate(
            self.document
        ):

            text = page.get_text().strip()

            # If normal PDF text exists,
            # OCR is not required.
            if text:
                print(
                    f"Page {page_number + 1}: "
                    "Normal text detected"
                )

                continue

            print(
                f"Page {page_number + 1}: "
                "No text detected - running OCR"
            )

            # Convert PDF page to image
            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2)
            )

            image_bytes = pixmap.tobytes(
                "png"
            )

            with Image.open(io.BytesIO(image_bytes)) as image:
                # Run OCR while the in-memory image is still open.
                extracted_text = pytesseract.image_to_string(
                    image,
                    lang=self.language,
                )

            extracted_text = extracted_text.strip()

            self.ocr_text.append({
                "page_number": page_number + 1,
                "text": extracted_text
            })

            print(
                f"OCR characters: "
                f"{len(extracted_text)}"
            )

    def close_pdf(self):

        if self.document is not None:
            self.document.close()
            self.document = None

    def process(self):
        # Allow a PDFOCR instance to be used for more than one run.
        self.ocr_text = []

        try:
            self.open_pdf()
            self.process_pages()
        finally:
            # Do not retain an open file handle if Tesseract raises an error.
            self.close_pdf()

        return self.ocr_text

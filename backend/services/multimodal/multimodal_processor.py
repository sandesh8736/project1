from pathlib import Path


class MultimodalProcessor:

    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)
        self.document_data = self._new_document_data()

    @staticmethod
    def _new_document_data():
        return {
            "text": [],
            "images": [],
            "tables": [],
            "ocr": [],
        }

    def _create_text_processor(self):
        from .pdf_processor import PDFProcessor

        return PDFProcessor(self.pdf_path)

    def _create_image_extractor(self):
        from .image_extractor import ImageExtractor

        return ImageExtractor(self.pdf_path)

    def _create_table_extractor(self):
        from .table_extractor import TableExtractor

        return TableExtractor(self.pdf_path)

    def _create_ocr_processor(self):
        from .ocr import PDFOCR

        return PDFOCR(self.pdf_path)

    def process_text(self):
        processor = self._create_text_processor()

        pages = processor.process()

        for page in pages:

            text = page.get("text", "").strip()

            if text:

                self.document_data["text"].append({
                    "page_number": page["page_number"],
                    "text": text
                })

    def process_images(self):

        extractor = self._create_image_extractor()

        images = extractor.process()

        self.document_data["images"] = images

    def process_tables(self):

        extractor = self._create_table_extractor()

        tables = extractor.process()

        self.document_data["tables"] = tables

    def process_ocr(self):

        ocr = self._create_ocr_processor()

        ocr_results = ocr.process()

        self.document_data["ocr"] = ocr_results

    def process(self):
        # A processor instance may be reused without retaining data from a prior PDF run.
        self.document_data = self._new_document_data()
        self.process_text()
        self.process_images()
        self.process_tables()
        self.process_ocr()

        return self.document_data

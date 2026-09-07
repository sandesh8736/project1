import pymupdf


class PDFProcessor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.document = None
        self.pages = []

    def open_pdf(self):
        self.document = pymupdf.open(self.pdf_path)
        print("Total pages:", len(self.document))

    def process_pages(self):

        for page_number, page in enumerate(self.document):

            text = page.get_text()

            images = page.get_images(full=True)

            page_data = {
                "page_number": page_number + 1,
                "text": text,
                "image_count": len(images)
            }

            self.pages.append(page_data)

            print(
                f"Page {page_number + 1}: "
                f"text={len(text)} characters, "
                f"images={len(images)}"
            )

    def close_pdf(self):

        if self.document:
            self.document.close()

    def process(self):

        self.open_pdf()

        self.process_pages()

        self.close_pdf()

        return self.pages

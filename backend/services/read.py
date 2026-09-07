from pypdf import PdfReader


class PDF_reader:

    def __init__(self, file_path):

        self.file_path = file_path

    def read_pdf(self):

        reader = PdfReader(self.file_path)

        pages = []

        total_pages = len(reader.pages)

        for i in range(total_pages):

            text = reader.pages[i].extract_text()

            if text is None:
                text = ""

            pages.append({
                "page_number": i + 1,
                "text": text
            })

        return pages
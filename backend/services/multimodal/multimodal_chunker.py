class MultimodalChunker:

    def __init__(self, document_data, chunk_size=1000, overlap=200):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError(
                "overlap must be non-negative and smaller than chunk_size"
            )

        self.document_data = document_data

        self.chunk_size = chunk_size
        self.overlap = overlap

        self.chunks = []

    def create_text_chunks(self, text, page_number):

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk_text = text[start:end]

            self.chunks.append({
                "type": "text",
                "page_number": page_number,
                "content": chunk_text
            })

            start += self.chunk_size - self.overlap

    def process_text(self):

        for page in self.document_data["text"]:

            page_number = page["page_number"]

            text = page["text"]

            if text.strip():

                self.create_text_chunks(
                    text,
                    page_number
                )

    def process_ocr(self):

        for page in self.document_data["ocr"]:

            page_number = page["page_number"]

            text = page["text"]

            if not text.strip():
                continue

            self.create_text_chunks(
                text,
                page_number
            )

    def process_tables(self):

        for table in self.document_data["tables"]:

            page_number = table["page_number"]

            rows = table["data"]

            table_text = "Table:\n"

            for row in rows:

                table_text += " | ".join(
                    str(cell) if cell is not None else ""
                    for cell in row
                )

                table_text += "\n"

            self.chunks.append({
                "type": "table",
                "page_number": page_number,
                "content": table_text
            })

    def process_images(self):

        for image in self.document_data["images"]:
            # ImageExtractor returns a file path, while image-understanding
            # integrations may provide a metadata dictionary with a caption.
            if isinstance(image, str):
                self.chunks.append({
                    "type": "image",
                    "page_number": None,
                    "content": "Image file:\n" + image,
                })
                continue

            page_number = image.get(
                "page_number",
                None
            )

            description = image.get(
                "description",
                ""
            )

            if not description.strip():
                continue

            self.chunks.append({
                "type": "image",
                "page_number": page_number,
                "content": (
                    "Image description:\n"
                    + description
                )
            })

    def process(self):

        self.chunks = []

        self.process_text()

        self.process_ocr()

        self.process_tables()

        self.process_images()

        return self.chunks

from pathlib import Path

import pymupdf


class ImageExtractor:

    def __init__(self, pdf_path, output_folder="processed"):
        self.pdf_path = Path(pdf_path)
        self.output_folder = Path(output_folder)
        self.document = None
        self.extracted_images = []

    def open_pdf(self):
        if not self.pdf_path.is_file():
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")

        self.document = pymupdf.open(self.pdf_path)

    def create_output_folder(self):

        self.output_folder.mkdir(parents=True, exist_ok=True)

    def extract_images(self):
        if self.document is None:
            raise RuntimeError("Open the PDF before extracting images.")

        for page_number, page in enumerate(self.document):

            images = page.get_images(full=True)

            for image_number, image in enumerate(images):

                xref = image[0]

                image_data = self.document.extract_image(xref)

                image_bytes = image_data["image"]
                image_extension = image_data["ext"]

                file_name = (
                    f"page_{page_number + 1}"
                    f"_image_{image_number + 1}."
                    f"{image_extension}"
                )

                file_path = self.output_folder / file_name

                with open(file_path, "wb") as image_file:

                    image_file.write(image_bytes)

                self.extracted_images.append(str(file_path))

                print(
                    f"Image extracted: {file_path}"
                )

    def close_pdf(self):

        if self.document is not None:
            self.document.close()
            self.document = None

    def process(self):
        # A single extractor instance can be reused without returning stale paths.
        self.extracted_images = []
        self.create_output_folder()

        try:
            self.open_pdf()
            self.extract_images()
        finally:
            # Always release the file handle, including when extraction fails.
            self.close_pdf()

        return self.extracted_images

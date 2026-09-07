import pymupdf


class TableExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.document = None
        self.tables = []

    def open_pdf(self):

        self.document = pymupdf.open(
            self.pdf_path
        )

        print(
            "Total pages:",
            len(self.document)
        )

    def extract_tables(self):

        for page_number, page in enumerate(
            self.document
        ):

            print(
                f"\nChecking page {page_number + 1}..."
            )

            try:

                table_finder = page.find_tables()

                page_tables = table_finder.tables

                if not page_tables:

                    print("No tables found.")

                    continue

                print(
                    f"Tables found: "
                    f"{len(page_tables)}"
                )

                for table_number, table in enumerate(
                    page_tables
                ):

                    data = table.extract()

                    table_data = {
                        "page_number": page_number + 1,
                        "table_number": table_number + 1,
                        "data": data
                    }

                    self.tables.append(
                        table_data
                    )

                    print(
                        f"Table {table_number + 1}:"
                    )

                    for row in data:

                        print(row)

            except Exception as error:

                print(
                    f"Table extraction error "
                    f"on page {page_number + 1}: "
                    f"{error}"
                )

    def close_pdf(self):

        if self.document:

            self.document.close()

            self.document = None

    def process(self):

        self.tables = []

        try:
            self.open_pdf()
            self.extract_tables()
            return self.tables
        finally:
            self.close_pdf()

import argparse

from services.multimodal.table_extractor import TableExtractor


def main():
    parser = argparse.ArgumentParser(description="Extract tables from a PDF.")
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default="uploads/turing-1936-paper.pdf",
        help="Path to the PDF to process.",
    )
    args = parser.parse_args()

    tables = TableExtractor(args.pdf_path).process()

    print("\n==========================")
    print("TABLE EXTRACTION COMPLETE")
    print("==========================")
    print("Total tables:", len(tables))

    for table in tables:
        print("\n--------------------------")
        print("Page:", table["page_number"])
        print("Table:", table["table_number"])
        print("Data:")

        for row in table["data"]:
            print(row)


if __name__ == "__main__":
    main()
 
import argparse

from services.multimodal.image_extractor import ImageExtractor


def main():
    parser = argparse.ArgumentParser(description="Extract images embedded in a PDF.")
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default="uploads/2604.15597v1.pdf",
        help="Path to the PDF to process.",
    )
    parser.add_argument("--output", default="processed", help="Destination directory.")
    args = parser.parse_args()

    extractor = ImageExtractor(args.pdf_path, args.output)
    images = extractor.process()

    print("\nExtraction completed.")
    print("Total images:", len(images))

    for image in images:
        print(image)


if __name__ == "__main__":
    main()

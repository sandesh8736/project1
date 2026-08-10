from pypdf import PdfReader 


def read_pdf(file_path):
    reader = PdfReader(file_path)
    total_characters = 0;

    total_pages = len(reader.pages)
    full_text = ""

    for i in range(total_pages):
        text = reader.pages[i].extract_text()  

        if text:

            full_text += text + "\n"

    return full_text
           

 
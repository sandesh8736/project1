from pypdf import PdfReader 


def read_pdf(file_path):

    reader = PdfReader(file_path)
    total_charactes = 0;
    full_text = ""

    for i in range(total_pages):
        text = reader.pages[i].extract_text()  

        if text:

            full_text +=text

    return full_text
           

 
import pdfplumber

def extract_text(file):
    if hasattr(file, "seek"):
        file.seek(0)

    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

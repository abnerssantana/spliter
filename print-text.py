import pdfplumber
from glob import glob

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()

    return text

def main():
    directory = 'PDF_SPLIT'
    pdf_list = glob(f'{directory}/*.pdf')

    for pdf_path in pdf_list:
        text_content = extract_text_from_pdf(pdf_path)
        lines = text_content.split('\n')
        for line in lines:
            print(line)

if __name__ == "__main__":
    main()

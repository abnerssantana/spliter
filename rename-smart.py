import os
import pdfplumber
from glob import glob

# Functions for extracting text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_after_r_dollar(lines):
    for line in lines:
        if "R$" in line:
            return line.split("R$")[-1].replace(".", "").replace(",", "").strip()
    return None

# Functions for renaming and processing PDF files
def rename_pdf(pdf_path, output_directory, new_filename):
    if not os.path.exists(pdf_path) or not pdf_path.endswith('.pdf'):
        print(f"Invalid file path or not a PDF file: {pdf_path}")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")
    if os.path.exists(new_filepath):
        print(f"File already exists: {new_filepath}")
    else:
        os.rename(pdf_path, new_filepath)
        print(f"File renamed to: {new_filepath}")

def process_pdf(pdf_path, output_directory):
    text_content = extract_text_from_pdf(pdf_path)
    lines = text_content.split('\n')
    desired_text = extract_text_after_r_dollar(lines)
    if desired_text:
        return f"{desired_text}_renamed_file"
    return None

# Main function
def main():
    input_directory = 'PDF_SPLIT'
    output_directory = 'PDF_FINAL'

    if not os.path.exists(input_directory) or not os.path.isdir(input_directory):
        print(f"Invalid input directory: {input_directory}")
        return

    pdf_list = glob(f'{input_directory}/*.pdf')

    for pdf_path in pdf_list:
        new_filename = process_pdf(pdf_path, output_directory)
        if new_filename:
            rename_pdf(pdf_path, output_directory, new_filename)

if __name__ == "__main__":
    main()
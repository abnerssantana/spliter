import os
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
    input_directory = 'PDF_SPLIT'
    output_directory = 'PDF_FINAL'

    # Verificar se o diretório de saída existe e, se não, criá-lo
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_list = glob(f'{input_directory}/*.pdf')

    for pdf_path in pdf_list:
        text_content = extract_text_from_pdf(pdf_path)
        
        # Verificar se as linhas 5 e 13 podem ser extraídas corretamente
        lines = text_content.split('\n')
        if len(lines) >= 5 and len(lines[4]) > 0:
            # Inverter a linha 5 e extrair o texto até o primeiro espaço
            line_5_reversed = lines[4][::-1]
            last_space_index = line_5_reversed.find(' ')
            text_after_last_space = line_5_reversed[:last_space_index][::-1]
            
            new_filename = f"{lines[12].split(' ')[0]}-{text_after_last_space}"

            # Renomear o arquivo apenas se ele existir
            if os.path.exists(pdf_path):
                new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")
                os.rename(pdf_path, new_filepath)
                print(f"Arquivo renomeado para: {new_filepath}")
            else:
                print(f"Arquivo não encontrado: {pdf_path}")

if __name__ == "__main__":
    main()

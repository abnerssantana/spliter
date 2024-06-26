#ABNSS - Splitter | 22 MAR 2024 - Print Text PDF

import pdfplumber
from glob import glob

# Função para extrair texto de um arquivo PDF dado o caminho do arquivo.
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()
    return text

def main():
    # Define o diretório onde os arquivos PDF estão localizados.
    directory = 'PDF_PRINT'
    # Obtém a lista de caminhos para todos os arquivos PDF no diretório especificado.
    pdf_list = glob(f'{directory}/*.pdf')

    for pdf_path in pdf_list:
        # Extrai o conteúdo de texto do PDF.
        text_content = extract_text_from_pdf(pdf_path)
        # Divide o conteúdo do texto em linhas.
        lines = text_content.split('\n')
        # Imprime no console.
        for line in lines:
            print(line)
if __name__ == "__main__":
    main()

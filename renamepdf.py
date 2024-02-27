#ABNSS - Splitter | 27 FEV 2024 - Rename PDF
import os
import pdfplumber
from glob import glob

#1 - RecibodePagamento

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()

    return text

def extract_first_word_after_last_space(text, line_number):
    if len(text) >= line_number:
        words = text[line_number - 1].split(' ')
        if len(words) > 0:
            return words[-1]
    return ""

def extract_text_after_first_space(text, line_number):
    if len(text) >= line_number:
        words = text[line_number - 1].split(' ', 1)
        if len(words) > 1:
            return words[1]
    return ""

def main():
    input_directory = 'PDF_SPLIT'
    output_directory = 'PDF_FINAL'

    # Verificar se o diretório de saída existe e, se não, criá-lo
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_list = glob(f'{input_directory}/*.pdf')

    for pdf_path in pdf_list:
        text_content = extract_text_from_pdf(pdf_path)

        # Verificar se a segunda linha contém o texto desejado
        lines = text_content.split('\n')
        if len(lines) >= 2 and "RecibodePagamento" in lines[1]:
            # Utilizar a última palavra após o último espaço na linha 5
            last_word_after_last_space = extract_first_word_after_last_space(lines, 11)

            # Utilizar o texto depois do primeiro espaço na linha 7
            text_after_first_space_line_7 = extract_text_after_first_space(lines, 7)

            # Remover os caracteres ':', 'R$' e '.' do nome do arquivo
            last_word_after_last_space = last_word_after_last_space.replace(':', '')
            text_after_first_space_line_7 = text_after_first_space_line_7.replace('.', '')
            last_word_after_last_space = last_word_after_last_space.replace('R$', '')
            last_word_after_last_space = last_word_after_last_space.replace('.', '')

            new_filename = f"{last_word_after_last_space} - {text_after_first_space_line_7}"

            # Verificar se o arquivo original existe antes de tentar renomear
            if os.path.exists(pdf_path):
                new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")

                # Verificar se o novo caminho de arquivo já existe
                if os.path.exists(new_filepath):
                    print(f"Arquivo já existe: {new_filepath}")
                else:
                    os.rename(pdf_path, new_filepath)
                    print(f"Arquivo renomeado para: {new_filepath}")
            else:
                print(f"Arquivo não encontrado: {pdf_path}")
        else:
            print(f"Ignorando arquivo sem 'RecibodePagamento': {pdf_path}")

if __name__ == "__main__":
    main()

#2 - ComprovantedeEmissãodeTítulos

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        try:
            text = ""
            for page_num in range(len(pdf.pages)):
                page = pdf.pages[page_num]
                text += page.extract_text()
        except Exception as e:
            print(f"Erro ao extrair texto do PDF '{pdf_path}': {e}")
            return ""  # Retorna string vazia em caso de erro
    return text

def extract_first_word_after_last_space(text, line_number):
    if len(text) >= line_number:
        words = text[line_number - 1].split(' ')
        if len(words) > 0:
            return words[-1].replace(':', '').replace('R$', '').replace('.', '')
    return ""

def extract_text_until_first_space(text, line_number):
    if len(text) >= line_number:
        words = text[line_number - 1].split(' ')
        if len(words) > 0:
            return words[0].replace('.', '')
    return ""

def main():
    input_directory = 'PDF_SPLIT'
    output_directory = 'PDF_FINAL'

    # Verificar se o diretório de saída existe e, se não, criá-lo
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_list = glob(f'{input_directory}/*.pdf')

    for pdf_path in pdf_list:
        text_content = extract_text_from_pdf(pdf_path)

        # Verificar se a segunda linha contém o texto desejado
        lines = text_content.split('\n')
        if len(lines) >= 2 and "ComprovantedeEmissãodeTítulos" in lines[1]:
            
            # Utilizar a última palavra após o último espaço na linha 5
            last_word_after_last_space = extract_first_word_after_last_space(lines, 5)

            # Utilizar o texto até o primeiro espaço na linha 9
            text_until_first_space_line_9 = extract_text_until_first_space(lines, 9)

            new_filename = f"{last_word_after_last_space} - {text_until_first_space_line_9}"

            # Verificar se o arquivo original existe antes de tentar renomear
            if os.path.exists(pdf_path):
                new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")

                # Verificar se o novo caminho de arquivo já existe
                if os.path.exists(new_filepath):
                    print(f"Arquivo já existe: {new_filepath}")
                else:
                    os.rename(pdf_path, new_filepath)
                    print(f"Arquivo renomeado para: {new_filepath}")
            else:
                print(f"Arquivo não encontrado: {pdf_path}")
        else:
            print(f"Ignorando arquivo sem 'ComprovantedeEmissãodeTítulos': {pdf_path}")

if __name__ == "__main__":
    main()

#3 - ComprovantedeCréditoaoFavorecido

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        try:
            text = ""
            for page_num in range(len(pdf.pages)):
                page = pdf.pages[page_num]
                text += page.extract_text()
        except Exception as e:
            print(f"Erro ao extrair texto do PDF '{pdf_path}': {e}")
            return ""  # Retorna string vazia em caso de erro
    return text

def extract_first_word_from_line(lines, line_number):
    if len(lines) >= line_number:
        words = lines[line_number - 1].split(' ')
        if len(words) > 0:
            return words[0].replace('.', '')
    return ""

def extract_last_word_from_line(lines, line_number):
    if len(lines) >= line_number:
        words = lines[line_number - 1].split(' ')
        if len(words) > 0:
            return words[-1].replace(':', '').replace('R$', '').replace('.', '')
    return ""

def extract_first_word_after_last_space(lines, line_number):
    if len(lines) >= line_number:
        words = lines[line_number - 1].split(' ')
        if len(words) > 0:
            return words[-1].replace(':', '').replace('R$', '').replace('.', '')
    return ""

def extract_text_until_first_space(lines, line_number):
    if len(lines) >= line_number:
        words = lines[line_number - 1].split(' ')
        if len(words) > 0:
            return words[0].replace('.', '')
    return ""

def main():
    input_directory = 'PDF_SPLIT'
    output_directory = 'PDF_FINAL'

    # Verificar se o diretório de saída existe e, se não, criá-lo
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_list = glob(f'{input_directory}/*.pdf')

    for pdf_path in pdf_list:
        text_content = extract_text_from_pdf(pdf_path)

        # Verificar se a segunda linha contém o texto desejado
        lines = text_content.split('\n')
        if len(lines) >= 2 and "ComprovantedeCréditoaoFavorecido" in lines[1]:

            # Se na sexta linha estiver presente a palavra "Agência", pegar a primeira palavra da linha 14
            if len(lines) >= 6 and "Agência" in lines[5]:
                first_word_line_14 = extract_first_word_from_line(lines, 14)
                last_word_line_5 = extract_last_word_from_line(lines, 5)

                new_filename = f"{last_word_line_5} - {first_word_line_14}"

                # Verificar se o arquivo original existe antes de tentar renomear
                if os.path.exists(pdf_path):
                    new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")

                    # Verificar se o novo caminho de arquivo já existe
                    if os.path.exists(new_filepath):
                        print(f"Arquivo já existe: {new_filepath}")
                    else:
                        os.rename(pdf_path, new_filepath)
                        print(f"Arquivo renomeado para: {new_filepath}")
                else:
                    print(f"Arquivo não encontrado: {pdf_path}")
            else:
                # Utilizar a última palavra após o último espaço na linha 5
                last_word_after_last_space = extract_first_word_after_last_space(lines, 5)

                # Utilizar o texto até o primeiro espaço na linha 13
                text_until_first_space_line_13 = extract_text_until_first_space(lines, 13)

                new_filename = f"{last_word_after_last_space} - {text_until_first_space_line_13}"

                # Verificar se o arquivo original existe antes de tentar renomear
                if os.path.exists(pdf_path):
                    new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")

                    # Verificar se o novo caminho de arquivo já existe
                    if os.path.exists(new_filepath):
                        print(f"Arquivo já existe: {new_filepath}")
                    else:
                        os.rename(pdf_path, new_filepath)
                        print(f"Arquivo renomeado para: {new_filepath}")
                else:
                    print(f"Arquivo não encontrado: {pdf_path}")
        else:
            print(f"Ignorando arquivo sem 'ComprovantedeCréditoaoFavorecido': {pdf_path}")

if __name__ == "__main__":
    main()

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

def extract_first_word_from_line(text, line_number):
    if len(text) >= line_number:
        words = text[line_number - 1].split(' ')
        if len(words) > 0:
            return words[0]
    return ""

def extract_last_word_from_line(text, line_number):
    if len(text) >= line_number:
        words = text[line_number - 1].split(' ')
        if len(words) > 0:
            return words[-1]
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
            # Utilizar a primeira palavra depois do primeiro espaço na linha 7
            line_7_words = lines[6].split(' ')
            if len(line_7_words) > 1:
                first_word_after_space = line_7_words[1]
            else:
                first_word_after_space = ""

            # Utilizar a linha 11 após o primeiro espaço
            line_11_words = lines[10].split(' ')
            if len(line_11_words) > 1:
                text_after_first_space_line_11 = line_11_words[1]
            else:
                text_after_first_space_line_11 = ""

            new_filename = f"RP - {first_word_after_space}-{text_after_first_space_line_11}"

        # Se na 13ª linha estiver presente o texto "Nome", pegar a próxima linha
        elif len(lines) > 13 and "Nome" in lines[12]:
            new_filename = f"CCF - {extract_first_word_from_line(lines, 14)}"

        # Se na sexta linha estiver presente a palavra "Agência", pegar a primeira palavra da linha 14
        elif len(lines) >= 6 and "Agência" in lines[5]:
            first_word_line_14 = extract_first_word_from_line(lines, 14)
            last_word_line_5 = extract_last_word_from_line(lines, 5)
            new_filename = f"NovaCategoria - {last_word_line_5}-{first_word_line_14}"

        # Se não contiver "RecibodePagamento" na segunda linha, continuar com a lógica anterior
        else:
            if len(lines) >= 5 and len(lines[4]) > 0:
                line_5_reversed = lines[4][::-1]
                last_space_index = line_5_reversed.find(' ')
                text_after_last_space = line_5_reversed[:last_space_index][::-1]

                new_filename = f"CCF - {lines[12].split(' ')[0]}-{text_after_last_space}"

        # Renomear o arquivo apenas se ele existir
        if os.path.exists(pdf_path):
            new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")
            os.rename(pdf_path, new_filepath)
            print(f"Arquivo renomeado para: {new_filepath}")
        else:
            print(f"Arquivo não encontrado: {pdf_path}")

if __name__ == "__main__":
    main()

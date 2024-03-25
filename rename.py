import os
import pdfplumber
from glob import glob

# Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()
    return text

# Função para renomear um arquivo PDF
def rename_pdf(pdf_path, output_directory, new_filename):
    if os.path.exists(pdf_path):
        new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")
        counter = 1
        while os.path.exists(new_filepath):
            new_filepath = os.path.join(output_directory, f"{new_filename}({counter}).pdf")
            counter += 1
        os.rename(pdf_path, new_filepath)
        print(f"Arquivo renomeado para: {new_filepath}")
    else:
        print(f"Arquivo não encontrado: {pdf_path}")

# Função principal
def main():
    input_directory = 'PDF_SPLIT'  # Diretório de entrada dos arquivos PDF
    output_directory = 'PDF_FINAL'  # Diretório de saída para os arquivos renomeados
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_list = glob(f'{input_directory}/*.pdf')  # Lista todos os arquivos PDF no diretório de entrada

    if not pdf_list:
        print("Diretório de entrada vazio. Coloque os arquivos PDF em 'PDF_SPLIT'.")
        return

    # Loop através de cada arquivo PDF
    for pdf_path in pdf_list:
        text_content = extract_text_from_pdf(pdf_path)  # Extrai o texto do PDF
        lines = text_content.split('\n')  # Divide o texto em linhas

        # Verifica se há informações suficientes para renomear o arquivo
        if len(lines) >= 2:
            # Verifica o tipo de documento com base no conteúdo da segunda linha
            if "RecibodePagamento" in lines[1]:  # Se for um recibo de pagamento
                if  "DARE-SP/GNRE-SEFAZ/SP" in lines[8]:  # Se a palavra "Agência" estiver na linha 5
                    last_word_after_last_space = lines[11].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_after_last_space} - FGTS"
                    rename_pdf(pdf_path, output_directory, new_filename)    
                elif  "COMPROVANTEDEPAGAMENTORECOLHIMENTO-FGTSGRF" in lines[5]:  # Se a palavra "Agência" estiver na linha 5
                    last_word_after_last_space = lines[11].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_after_last_space} - FGTS"
                    rename_pdf(pdf_path, output_directory, new_filename)
                elif  "DocumentodeArrecadaçãodoSistema" in lines[11]:  # Se a palavra "Agência" estiver na linha 5
                    last_word_after_last_space = lines[18].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_after_last_space} - DARF"
                    rename_pdf(pdf_path, output_directory, new_filename)    
                elif  "COMPROVANTEDERECOLHIMENTO-FGTSRESCISORIO" in lines[5]:  # Se a palavra "Agência" estiver na linha 5
                    last_word_after_last_space = lines[10].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_after_last_space} - FGTSRESCISORIO"
                    rename_pdf(pdf_path, output_directory, new_filename)      
                else:
                    last_word_after_last_space = lines[10].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    text_after_first_space_line_7 = lines[6].split(maxsplit=1)[-1].replace('.', '')
                    new_filename = f"{last_word_after_last_space} - {text_after_first_space_line_7}"
                    rename_pdf(pdf_path, output_directory, new_filename)
            elif "ComprovantedeEmissãodeTítulos" in lines[1]:  # Se for um comprovante de emissão de títulos
                last_word_after_last_space = lines[4].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                text_until_first_space_line_9 = lines[8].split()[0].replace('.', '')
                new_filename = f"{last_word_after_last_space} - {text_until_first_space_line_9}"
                rename_pdf(pdf_path, output_directory, new_filename)
            elif "PAGAMENTO A FORNECEDORES" in lines[1]:  # Se for um comprovante de ComprovantedeEmissãodeTítulos
                if "ComprovantedeEmissãodeTítulos" in lines[2]:  # Se a palavra "ComprovantedeEmissãodeTítulos" estiver na linha 2
                    last_word_after_last_space = lines[5].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    text_after_first_space_line_9 = lines[9].split(maxsplit=1)[-1].replace('.', '')
                    new_filename = f"{last_word_after_last_space} - {text_after_first_space_line_9}" 
                elif "DARE-SP" in lines[13]:  # Se a palavra "DARE-SP" estiver na linha 13
                    last_word_after_last_space = lines[22].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_after_last_space} - DARE"
                    rename_pdf(pdf_path, output_directory, new_filename) 
                elif "DARF" in lines[11]:  # Se a palavra "DARF" estiver na linha 11
                    last_word_after_last_space = lines[22].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_after_last_space} - DARF"
                    rename_pdf(pdf_path, output_directory, new_filename) 
                elif "MUNICIPIO" in lines[12]:  # Se a palavra "MUNICIPIO" estiver na linha 12
                    last_word_after_last_space = lines[5].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_after_last_space} - MUNICIPIO"
                    rename_pdf(pdf_path, output_directory, new_filename)               
            elif "ComprovantedeCréditoaoFavorecido" in lines[1]:  # Se for um comprovante de crédito ao favorecido
                if "Agência" in lines[5]:  # Se a palavra "Agência" estiver na linha 5
                    first_word_line_14 = lines[13].split()[0].replace('.', '')
                    last_word_line_5 = lines[4].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    new_filename = f"{last_word_line_5} - {first_word_line_14}"
                    rename_pdf(pdf_path, output_directory, new_filename)
                else:
                    last_word_after_last_space = lines[4].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    text_until_first_space_line_13 = lines[12].split()[0].replace('.', '')
                    new_filename = f"{last_word_after_last_space} - {text_until_first_space_line_13}"
                    rename_pdf(pdf_path, output_directory, new_filename)
        else:
            print(f"Arquivo sem informações suficientes para renomear: {pdf_path}")

if __name__ == "__main__":
    main()

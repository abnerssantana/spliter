import re
import os
from PyPDF2 import PdfWriter, PdfReader

def sanitize_filename(filename):
    # Substitui caracteres inválidos para nomes de arquivos por nada, exceto vírgulas
    return re.sub(r'[\\/*?.:"<>|]', "", filename)

def extract_name_and_value(text):
    # Verifica se o documento é um DARF
    if "DARF" in text:
        # Procura o valor total
        total_match = re.search(r"Total:\s*([\d.,]+)", text)
        if total_match:
            total = total_match.group(1)
            return f"DARF-{total}"
    
    # Se não for DARF, tenta encontrar o nome e valor do destinatário ou da empresa
    name_patterns = [
        r"Dados do Destinatário\s*Nome\s*(.*?)\s*(?:CNPJ/CPF|$)",
        r"Dados do Favorecido\s*Nome\s*(.*?)\s*(?:CNPJ/CPF|$)",
        r"Nome/Razão Social do Beneficiário Original\s*\n\s*(.*?)(?:\s*\n|$)",
        r"Empresa:\s*(.*?)\s*(?:Convenio|$)",  # Novo padrão para capturar o nome da empresa
    ]
    
    name = None
    for pattern in name_patterns:
        name_match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            # Interrompe ao encontrar "CPF/CNPJ do Beneficiário Original"
            name = re.sub(r'CPF/CNPJ do Beneficiário Original.*', '', name, flags=re.IGNORECASE).strip()
            break
    
    # Tentativa de encontrar o valor do pagamento
    value_match = re.search(r"Valor[:\s]*R?\$?\s*([\d.,]+)", text, re.IGNORECASE)

    if name and value_match:
        # Limpa e formata o nome e o valor
        name = sanitize_filename(name)
        value = value_match.group(1).replace('.', '').replace(',', '')  # Remove pontos e vírgulas
        return f"{value} - {name}"
    return None

def get_unique_filename(output_folder, base_filename):
    # Garante que o nome do arquivo seja único no diretório de saída
    counter = 1
    filename = base_filename
    while os.path.exists(os.path.join(output_folder, filename + ".pdf")):
        filename = f"{base_filename}-{counter}"
        counter += 1
    return filename

def split_pdfs_in_folder(input_folder, output_folder):
    # Cria o diretório de saída se ele não existir
    os.makedirs(output_folder, exist_ok=True)

    # Percorre todos os arquivos no diretório de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            input_pdf_path = os.path.join(input_folder, filename)
            reader = PdfReader(input_pdf_path)

            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)

                # Extrai o texto da página atual
                page_text = page.extract_text() 
                output_filename = extract_name_and_value(page_text)

                # Define o nome do arquivo de saída com base nos dados extraídos ou número da página
                if output_filename:
                    base_filename = output_filename
                else:
                    base_filename = f"{os.path.splitext(filename)[0]}-pag-{i+1}"

                # Garante que o nome do arquivo seja único
                unique_filename = get_unique_filename(output_folder, base_filename)
                output_path = os.path.join(output_folder, f"{unique_filename}.pdf")

                # Salva a página como um novo arquivo PDF
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
                
                print(f"Created: {output_path}")
                #print(f"Texto extraído: {page_text}")


# Caminho da pasta de entrada e da pasta de saída
input_folder = "comprovantes"
output_folder = "pdfs"

# Chama a função para dividir os PDFs na pasta
split_pdfs_in_folder(input_folder, output_folder)

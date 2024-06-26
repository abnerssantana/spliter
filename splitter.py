import os
import json
import PyPDF2
import pdfplumber
from glob import glob
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Arquivo de configuração para armazenar os diretórios selecionados
CONFIG_FILE = 'config.json'

# Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()
    return text

# Função para limpar o nome do arquivo
def clean_filename(filename):
    return filename.replace('/', '_').replace('\\', '_')

# Função para renomear um arquivo PDF
def rename_pdf(pdf_path, output_directory, new_filename, renaming_counter):
    new_filename = clean_filename(new_filename)  # Limpa o nome do arquivo
    if os.path.exists(pdf_path):
        new_filepath = os.path.join(output_directory, f"{new_filename}.pdf")
        counter = 1
        while os.path.exists(new_filepath):
            new_filepath = os.path.join(output_directory, f"{new_filename}({counter}).pdf")
            counter += 1
        os.rename(pdf_path, new_filepath)
        renaming_counter[0] += 1
        print(f"Arquivo renomeado para: {new_filepath}")
    else:
        print(f"Arquivo não encontrado: {pdf_path}")

# Função para processar os arquivos PDF
def process_pdfs(input_directory, output_directory, renaming_counter):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_list = glob(f'{input_directory}/*.pdf')  # Lista todos os arquivos PDF no diretório de entrada

    if not pdf_list:
        messagebox.showerror("Erro", "Diretório de entrada vazio. Coloque os arquivos PDF em 'PDF_SPLIT'.")
        return

    # Loop através de cada arquivo PDF
    for pdf_path in pdf_list:
        print(f"Processando arquivo: {pdf_path}")  # Log para verificar o arquivo sendo processado
        text_content = extract_text_from_pdf(pdf_path)  # Extrai o texto do PDF
        if text_content:
            lines = text_content.split('\n')  # Divide o texto em linhas

            # Verifica se há informações suficientes para renomear o arquivo
            if len(lines) >= 2:
                # Verifica o tipo de documento com base no conteúdo da segunda linha
                if "RecibodePagamento" in lines[1]:  # Se for um recibo de pagamento
                    if "DARE-SP/GNRE-SEFAZ/SP" in lines[8]:  
                        last_word_after_last_space = lines[11].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_after_last_space} - FGTS"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)    
                    elif "COMPROVANTEDEPAGAMENTORECOLHIMENTO-FGTSGRF" in lines[5]:  
                        last_word_after_last_space = lines[11].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_after_last_space} - FGTS"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)
                    elif "DocumentodeArrecadaçãodoSistema" in lines[11]:  
                        last_word_after_last_space = lines[18].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_after_last_space} - DARF"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)    
                    elif "COMPROVANTEDERECOLHIMENTO-FGTSRESCISORIO" in lines[5]:  
                        last_word_after_last_space = lines[10].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_after_last_space} - FGTSRESCISORIO"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)      
                    else:
                        last_word_after_last_space = lines[10].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        text_after_first_space_line_7 = lines[6].split(maxsplit=1)[-1].replace('.', '')
                        new_filename = f"{last_word_after_last_space} - {text_after_first_space_line_7}"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)
                elif "ComprovantedeEmissãodeTítulos" in lines[1]:  # Se for um comprovante de emissão de títulos
                    last_word_after_last_space = lines[4].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                    text_until_first_space_line_9 = lines[8].split()[0].replace('.', '')
                    new_filename = f"{last_word_after_last_space} - {text_until_first_space_line_9}"
                    rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)
                elif "PAGAMENTO A FORNECEDORES" in lines[1]:  # Se for um comprovante de pagamento a fornecedores
                    if "ComprovantedeEmissãodeTítulos" in lines[2]:  # Se a palavra "ComprovantedeEmissãodeTítulos" estiver na linha 2
                        last_word_after_last_space = lines[5].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        text_after_first_space_line_9 = lines[9].split(maxsplit=1)[-1].replace('.', '')
                        new_filename = f"{last_word_after_last_space} - {text_after_first_space_line_9}" 
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)
                    elif "DARE-SP" in lines[13]:  # Se a palavra "DARE-SP" estiver na linha 13
                        last_word_after_last_space = lines[22].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_after_last_space} - DARE"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter) 
                    elif "DARF" in lines[11]:  # Se a palavra "DARF" estiver na linha 11
                        last_word_after_last_space = lines[22].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_after_last_space} - DARF"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter) 
                    elif "MUNICIPIO" in lines[12]:  # Se a palavra "MUNICIPIO" estiver na linha 12
                        last_word_after_last_space = lines[5].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_after_last_space} - MUNICIPIO"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)               
                elif "ComprovantedeCréditoaoFavorecido" in lines[1]:  # Se for um comprovante de crédito ao favorecido
                    if "Agência" in lines[5]:  
                        first_word_line_14 = lines[13].split()[0].replace('.', '')
                        last_word_line_5 = lines[4].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        new_filename = f"{last_word_line_5} - {first_word_line_14}"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)
                    else:
                        last_word_after_last_space = lines[4].split()[-1].replace(':', '').replace('R$', '').replace('.', '')
                        text_until_first_space_line_13 = lines[12].split()[0].replace('.', '')
                        new_filename = f"{last_word_after_last_space} - {text_until_first_space_line_13}"
                        rename_pdf(pdf_path, output_directory, new_filename, renaming_counter)
            else:
                print(f"Arquivo sem informações suficientes para renomear: {pdf_path}")
        else:
            print(f"Erro ao extrair texto do arquivo: {pdf_path}")

    messagebox.showinfo("Informação", f"Processamento concluído. Total de arquivos renomeados: {renaming_counter[0]}.")

# Função para carregar diretórios do arquivo de configuração
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {"input_directory": "", "output_directory": "", "split_input_file": "", "split_output_directory": ""}

# Função para salvar diretórios no arquivo de configuração
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

# Função para dividir um PDF em páginas separadas
def dividir_pdf(input_path, output_path, splitting_counter):
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            output_file_path = os.path.join(output_path, f"page_{page_num + 1}.pdf")
            counter = 1
            while os.path.exists(output_file_path):
                output_file_path = os.path.join(output_path, f"page_{page_num + 1}({counter}).pdf")
                counter += 1

            with open(output_file_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                splitting_counter[0] += 1
                print(f'Página {page_num + 1} dividida para {output_file_path}')

    messagebox.showinfo("Informação", f"PDF dividido em páginas separadas. Total de páginas divididas: {splitting_counter[0]}.")

# Função para selecionar o diretório de entrada
def select_input_directory():
    input_directory = filedialog.askdirectory(title="Selecione o Diretório de Entrada")
    input_dir_var.set(input_directory)

# Função para selecionar o diretório de saída
def select_output_directory():
    output_directory = filedialog.askdirectory(title="Selecione o Diretório de Saída")
    output_dir_var.set(output_directory)

# Função para selecionar o arquivo de entrada para divisão
def select_split_input_file():
    input_file = filedialog.askopenfilename(title="Selecione o Arquivo PDF de Entrada", filetypes=[("PDF files", "*.pdf")])
    split_input_file_var.set(input_file)

# Função para selecionar o diretório de saída para divisão
def select_split_output_directory():
    output_directory = filedialog.askdirectory(title="Selecione o Diretório de Saída para Páginas Separadas")
    split_output_dir_var.set(output_directory)

# Função para iniciar o processamento
def start_processing():
    input_directory = input_dir_var.get()
    output_directory = output_dir_var.get()
    if input_directory and output_directory:
        config["input_directory"] = input_directory
        config["output_directory"] = output_directory
        save_config(config)
        renaming_counter = [0]  # Contador para arquivos renomeados
        process_pdfs(input_directory, output_directory, renaming_counter)
    else:
        messagebox.showerror("Erro", "Por favor, selecione os diretórios de entrada e saída.")

# Função para iniciar a divisão de PDF
def start_splitting():
    input_file = split_input_file_var.get()
    output_directory = split_output_dir_var.get()
    if input_file and output_directory:
        config["split_input_file"] = input_file
        config["split_output_directory"] = output_directory
        save_config(config)
        splitting_counter = [0]  # Contador para páginas divididas
        dividir_pdf(input_file, output_directory, splitting_counter)
    else:
        messagebox.showerror("Erro", "Por favor, selecione o arquivo PDF de entrada e o diretório de saída.")

# Função para centralizar a janela na tela
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Criação da interface gráfica
app = tk.Tk()
app.title("Splitter - Divisor e Renomeador de PDFs")

# Carrega os diretórios do arquivo de configuração
config = load_config()

# Criação das variáveis de controle
input_dir_var = tk.StringVar(value=config.get("input_directory", ""))
output_dir_var = tk.StringVar(value=config.get("output_directory", ""))
split_input_file_var = tk.StringVar(value=config.get("split_input_file", ""))
split_output_dir_var = tk.StringVar(value=config.get("split_output_directory", ""))

# Estilo de fundo
style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0')
style.configure('TButton', background='#d9d9d9')

# Criação das abas
tab_control = ttk.Notebook(app)
tab_rename = ttk.Frame(tab_control, style='TFrame')
tab_split = ttk.Frame(tab_control, style='TFrame')
tab_control.add(tab_split, text="Dividir PDF")
tab_control.add(tab_rename, text="Renomear PDFs")
tab_control.pack(expand=1, fill="both")

# Aba de renomear PDFs
frame_rename = ttk.Frame(tab_rename, style='TFrame')
frame_rename.pack(padx=10, pady=10)

input_dir_label = ttk.Label(frame_rename, text="Diretório de Entrada:", style='TLabel')
input_dir_label.grid(row=0, column=0, sticky="e")
input_dir_entry = ttk.Entry(frame_rename, textvariable=input_dir_var, width=40)
input_dir_entry.grid(row=0, column=1, padx=5, pady=5)
input_dir_button = ttk.Button(frame_rename, text="Selecionar", command=select_input_directory, style='TButton')
input_dir_button.grid(row=0, column=2, padx=5, pady=5)

output_dir_label = ttk.Label(frame_rename, text="Diretório de Saída:", style='TLabel')
output_dir_label.grid(row=1, column=0, sticky="e")
output_dir_entry = ttk.Entry(frame_rename, textvariable=output_dir_var, width=40)
output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
output_dir_button = ttk.Button(frame_rename, text="Selecionar", command=select_output_directory, style='TButton')
output_dir_button.grid(row=1, column=2, padx=5, pady=5)

process_button = ttk.Button(tab_rename, text="Iniciar Processamento", command=start_processing, style='TButton')
process_button.pack(pady=10)

# Aba de dividir PDFs
frame_split = ttk.Frame(tab_split, style='TFrame')
frame_split.pack(padx=10, pady=10)

split_input_file_label = ttk.Label(frame_split, text="Arquivo PDF de Entrada:", style='TLabel')
split_input_file_label.grid(row=0, column=0, sticky="e")
split_input_file_entry = ttk.Entry(frame_split, textvariable=split_input_file_var, width=40)
split_input_file_entry.grid(row=0, column=1, padx=5, pady=5)
split_input_file_button = ttk.Button(frame_split, text="Selecionar", command=select_split_input_file, style='TButton')
split_input_file_button.grid(row=0, column=2, padx=5, pady=5)

split_output_dir_label = ttk.Label(frame_split, text="Diretório de Saída:", style='TLabel')
split_output_dir_label.grid(row=1, column=0, sticky="e")
split_output_dir_entry = ttk.Entry(frame_split, textvariable=split_output_dir_var, width=40)
split_output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
split_output_dir_button = ttk.Button(frame_split, text="Selecionar", command=select_split_output_directory, style='TButton')
split_output_dir_button.grid(row=1, column=2, padx=5, pady=5)

split_button = ttk.Button(tab_split, text="Iniciar Divisão", command=start_splitting, style='TButton')
split_button.pack(pady=10)

# Centraliza a janela na tela
center_window(app)

app.mainloop()

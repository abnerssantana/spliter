import PyPDF2

def dividir_pdf(input_path, output_path):
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            output_file_path = f"{output_path}/page_{page_num + 1}.pdf"
            with open(output_file_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                print(f'Página {page_num + 1} dividida para {output_file_path}')

if __name__ == "__main__":
    input_file_path = "PDF/Comprovante.pdf"
    output_folder_path = "PDF_SPLIT"

    dividir_pdf(input_file_path, output_folder_path)

# Splitter - Divisor de Comprovantes

## Softwares Necessários:
1. Python 3: https://www.python.org/
2. PyPDF2 (pip install PyPDF2)
3. pdfplumber (pip install pdfplumber)

### INSTRUÇÕES DE USO

* Adicione o arquivo "comprovantes.pdf" à pasta PDF (o arquivo deve ter esse nome).
* Na pasta principal Splitter, digite "cmd" na barra de endereços e pressione ↵ Enter.
* Na janela do terminal que abrir, execute o comando: python .\splitpdf.py (divide o arquivo em páginas).
* Os novos arquivos serão criados na pasta PDF_SPLIT.
* Na janela do terminal, execute o próximo comando: renamepdf.py (captura o texto valor/nome e renomeia).
* Os novos arquivos renomeados estarão na pasta PDF_FINAL.
* Se o tipo de comprovante não for identificado, eles serão mantidos na pasta PDF_SPLIT.

#### *Versão 0.1 - 27 de fevereiro de 2024*
#### *Versão 0.3 - 25 de março de 2024*
 - Renomeia arquivos com mesmo nome adicionando (Nº)
 - Ajuste nos filtros de tipos de arquivos

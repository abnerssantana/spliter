# Splitter - Divisor de Comprovantes

## Softwares Necessários:

1. Python 3: https://www.python.org/
2. PyPDF2 (pip install PyPDF2)
3. pdfplumber (pip install pdfplumber)

## INSTRUÇÕES DE USO

Adicione os arquivos de comprovantes à pasta PDF.
Na pasta principal Splitter, digite "cmd" na barra de endereços e pressione ↵ Enter.
Na janela do terminal que abrir, execute o comando: python .\splitpdf.py (divide o arquivo em páginas).
Os novos arquivos serão criados na pasta PDF_SPLIT.
Na janela do terminal, execute o próximo comando: python renamepdf.py (captura o texto valor/nome e renomeia).
Os novos arquivos renomeados estarão na pasta PDF_FINAL.
Se o tipo de comprovante não for identificado, eles serão mantidos na pasta PDF_SPLIT.

Versão 0.1 - 27 de fevereiro de 2024

Versão 0.3 - 25 de março de 2024

* Renomeia arquivos com mesmo nome adicionando (Nº)
* Ajuste nos filtros de tipos de arquivos

Versão 1.0 - 25 de junho de 2024

* Adicionado código para garantir que um arquivo dividido não sobrescreva um existente, adicionando um contador ao nome do arquivo se ele já existir no diretório de saída.
* Melhorias na interface gráfica para permitir a seleção de diretórios e arquivos de entrada/saída.
* Funções de processamento e divisão de PDFs atualizadas para incluir verificação de existência de arquivos e adicionar contadores.
* Remover caracteres que não são permitidos como nome de arquivo. 
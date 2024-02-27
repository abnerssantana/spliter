# SPLITER

  1. Python 3.9.5 
  2. pip3
  3. Visual Studio Code (VSC)

#### STEPS

1. Change default profile within VSC:
    * CMD/CTRL + SHIFT + P
    * Search "Terminal: Select Default Profile"
    * Click "Command Prompt" 
   
2. Create and activate the virtual environment + install library (run commands in a new CMD terminal)
   1. py -m venv venv 
      * (Creates virtual environment)
   2. venv\Scripts\activate                   
      * (activates virtual environment)
   3. python -m pip install --upgrade pip     
      * (Upgrade pip in virtual environment)
   4. python -m pip install --upgrade pymupdf
      * (Install the PyMuPDF library)
   
3. Create the python file (you can use any name or follow the tutorial)
import os
from tkinter import Tk, filedialog
from pdf2docx import Converter

# Hide the main Tkinter window
root = Tk()
root.withdraw()

# Open a file dialog to select the PDF file
pdf_file = filedialog.askopenfilename(
    title="Select PDF file", 
    filetypes=[("PDF files", "*.pdf")]
)

# Ask for the output DOCX file path using a save dialog
docx_file = filedialog.asksaveasfilename(
    title="Save DOCX file as", 
    defaultextension=".docx", 
    filetypes=[("Word Documents", "*.docx")]
)

# Check if the user selected a file and proceed with conversion
if not pdf_file:
    print("No PDF file selected. Exiting...")
elif not docx_file:
    print("No output file path selected. Exiting...")
else:
    # Create a converter object and convert the PDF to DOCX
    print(f"Converting {pdf_file} to {docx_file}...")

    try:
        # Create the converter and handle the conversion
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        
        print(f"Conversion complete! Your DOCX file has been saved to: {docx_file}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

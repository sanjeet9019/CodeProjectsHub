"""
Utility to extract text from PDF resumes using pdfplumber.
"""

import pdfplumber

def load_pdf_text(file_path):
    """
    Extracts and concatenates text from all pages of a PDF.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        str: Combined text from all pages.
    """
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())


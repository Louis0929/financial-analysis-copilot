"""
File reader module for Financial Statement Analysis Co-Pilot
Handles reading various file formats: TXT, PDF, DOCX, XLSX, CSV
"""

import os
import pandas as pd
from pathlib import Path

# Import libraries for different file formats
try:
    import PyPDF2
    import docx
    from openpyxl import load_workbook
except ImportError as e:
    print(f"⚠️ Some file format libraries are missing: {e}")

def read_txt_file(filepath):
    """Read content from a TXT file"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_file(filepath):
    """Read content from a PDF file"""
    try:
        import PyPDF2
        content = ""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
        return content
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF files. Install with: pip install PyPDF2")

def read_docx_file(filepath):
    """Read content from a Word document"""
    try:
        import docx
        doc = docx.Document(filepath)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content
    except ImportError:
        raise ImportError("python-docx is required for Word files. Install with: pip install python-docx")

def read_excel_file(filepath):
    """Read content from an Excel file"""
    try:
        # Read all sheets and combine content
        excel_file = pd.ExcelFile(filepath)
        content = ""
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            content += f"\n--- SHEET: {sheet_name} ---\n"
            content += df.to_string(index=False) + "\n"
        
        return content
    except ImportError:
        raise ImportError("pandas and openpyxl are required for Excel files. Install with: pip install pandas openpyxl")

def read_csv_file(filepath):
    """Read content from a CSV file"""
    try:
        df = pd.read_csv(filepath)
        return df.to_string(index=False)
    except ImportError:
        raise ImportError("pandas is required for CSV files. Install with: pip install pandas")

def read_report(filepath):
    """
    Read financial report content from various file formats
    Supports: TXT, PDF, DOCX, XLSX, CSV
    
    Args:
        filepath (str): Path to the financial report file
        
    Returns:
        str: Content of the financial report or None if error
    """
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"❌ Error: File not found at {filepath}")
            return None
        
        # Get file extension
        file_extension = Path(filepath).suffix.lower()
        
        # Read based on file type
        if file_extension == '.txt':
            content = read_txt_file(filepath)
        elif file_extension == '.pdf':
            content = read_pdf_file(filepath)
        elif file_extension == '.docx':
            content = read_docx_file(filepath)
        elif file_extension in ['.xlsx', '.xls']:
            content = read_excel_file(filepath)
        elif file_extension == '.csv':
            content = read_csv_file(filepath)
        else:
            print(f"❌ Unsupported file format: {file_extension}")
            return None
        
        print(f"✅ Successfully loaded {file_extension.upper()} report from: {filepath}")
        print(f"📄 Content length: {len(content)} characters")
        return content
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None 
import PyPDF2
from io import BytesIO
from typing import Union

def extract_text_from_pdf(pdf_file: Union[BytesIO, bytes]) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_file: PDF file object (from Streamlit file uploader) or bytes
        
    Returns:
        Extracted text as a string
    """
    try:
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        # Clean up text
        text = text.strip()
        
        if not text:
            return "Error: Could not extract text from PDF. The file might be image-based or corrupted."
        
        return text
        
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"


def get_pdf_metadata(pdf_file: Union[BytesIO, bytes]) -> dict:
    """
    Extract metadata from a PDF file.
    
    Args:
        pdf_file: PDF file object
        
    Returns:
        Dictionary containing PDF metadata
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        metadata = {
            'num_pages': len(pdf_reader.pages),
            'author': pdf_reader.metadata.get('/Author', 'Unknown') if pdf_reader.metadata else 'Unknown',
            'title': pdf_reader.metadata.get('/Title', 'Unknown') if pdf_reader.metadata else 'Unknown',
            'subject': pdf_reader.metadata.get('/Subject', 'Unknown') if pdf_reader.metadata else 'Unknown'
        }
        
        return metadata
        
    except Exception as e:
        return {'error': str(e)}

"""
Document parser for extracting text from various file formats.
Supports PDF, DOCX, Markdown, and plain text files.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import logging

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

class DocumentParser:
    """Parser for extracting text content from various document formats."""
    
    SUPPORTED_FORMATS = {'.pdf', '.docx', '.doc', '.md', '.txt'}
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def parse_documents(self, file_paths: List[str]) -> Dict[str, str]:
        """
        Parse multiple documents and return extracted text.
        
        Args:
            file_paths: List of file paths to parse
            
        Returns:
            Dictionary mapping file paths to extracted text content
        """
        results = {}
        
        for file_path in file_paths:
            try:
                text = self.extract_text_from_file(file_path)
                results[file_path] = text
                self.logger.info(f"Successfully parsed {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to parse {file_path}: {str(e)}")
                results[file_path] = ""
                
        return results
    
    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from a single file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        suffix = Path(file_path).suffix.lower()
        
        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {suffix}")
            
        if suffix == ".pdf":
            return self._extract_from_pdf(file_path)
        elif suffix in [".docx", ".doc"]:
            return self._extract_from_docx(file_path)
        elif suffix in [".md", ".txt"]:
            return self._extract_from_text(file_path)
        else:
            raise ValueError(f"Handler not implemented for format: {suffix}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        if PdfReader is None:
            raise ImportError("PyPDF2 is required to parse PDF files")
            
        try:
            reader = PdfReader(file_path)
            text_parts = []
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    
            return "\n".join(text_parts)
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        if Document is None:
            raise ImportError("python-docx is required to parse DOCX files")
            
        try:
            doc = Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
                    
            return "\n".join(text_parts)
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def _extract_from_text(self, file_path: str) -> str:
        """Extract text from markdown or plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    def validate_files(self, file_paths: List[str]) -> List[str]:
        """
        Validate that all files exist and have supported formats.
        
        Args:
            file_paths: List of file paths to validate
            
        Returns:
            List of validation error messages (empty if all valid)
        """
        errors = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                errors.append(f"File not found: {file_path}")
                continue
                
            suffix = Path(file_path).suffix.lower()
            if suffix not in self.SUPPORTED_FORMATS:
                errors.append(f"Unsupported format {suffix}: {file_path}")
                
        return errors 
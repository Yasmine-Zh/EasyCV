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
    
    def __init__(self, verbose=True):
        self.logger = logging.getLogger(__name__)
        self.verbose = verbose  # 添加调试输出控制
        
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
    
    def parse_document(self, file_path: str) -> str:
        """
        Parse a single document and return extracted text.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
        """
        return self.extract_text_from_file(file_path)
    
    def debug_parse_document(self, file_path: str) -> str:
        """
        Parse document with detailed debug output and full content display.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
        """
        print(f"\n🔍 详细解析模式 - 开始处理文档")
        print("=" * 60)
        
        content = self.extract_text_from_file(file_path)
        
        if content.strip():
            print(f"\n📝 完整提取内容:")
            print("=" * 60)
            print(content)
            print("=" * 60)
            print(f"📊 统计信息:")
            print(f"  - 总字符数: {len(content)}")
            print(f"  - 总行数: {len(content.splitlines())}")
            print(f"  - 非空行数: {len([line for line in content.splitlines() if line.strip()])}")
        else:
            print("❌ 未提取到任何内容")
        
        print("\n🔍 详细解析完成")
        print("=" * 60)
        
        return content
    
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
        file_name = Path(file_path).name
        
        if self.verbose:
            print(f"\n📄 开始解析文档: {file_name}")
            print(f"📁 文件路径: {file_path}")
            print(f"🔧 文件格式: {suffix}")
        
        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {suffix}")
            
        extracted_content = ""
        if suffix == ".pdf":
            extracted_content = self._extract_from_pdf(file_path)
        elif suffix in [".docx", ".doc"]:
            extracted_content = self._extract_from_docx(file_path)
        elif suffix in [".md", ".txt"]:
            extracted_content = self._extract_from_text(file_path)
        else:
            raise ValueError(f"Handler not implemented for format: {suffix}")
        
        if self.verbose:
            print(f"✅ 文档解析完成: {file_name}")
            print(f"📊 提取内容长度: {len(extracted_content)} 字符")
            if extracted_content.strip():
                print(f"📝 提取内容预览 (前200字符):")
                print("-" * 50)
                print(extracted_content[:200] + ("..." if len(extracted_content) > 200 else ""))
                print("-" * 50)
            else:
                print("⚠️  警告: 未提取到任何内容")
        
        return extracted_content
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        if PdfReader is None:
            raise ImportError("PyPDF2 is required to parse PDF files")
            
        try:
            reader = PdfReader(file_path)
            text_parts = []
            
            if self.verbose:
                print(f"📖 PDF总页数: {len(reader.pages)}")
            
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    if self.verbose:
                        print(f"📄 第{page_num}页: 提取了 {len(page_text)} 个字符")
                        # 显示每页前50个字符
                        preview = page_text.strip()[:50].replace('\n', ' ')
                        print(f"   预览: {preview}{'...' if len(page_text) > 50 else ''}")
                else:
                    if self.verbose:
                        print(f"📄 第{page_num}页: ⚠️  未提取到内容")
                    
            full_text = "\n".join(text_parts)
            
            if self.verbose:
                print(f"✅ PDF解析完成，共提取 {len(full_text)} 个字符")
                if len(text_parts) > 0:
                    print(f"📊 有效页面: {len(text_parts)}/{len(reader.pages)}")
                    
            return full_text
        except Exception as e:
            if self.verbose:
                print(f"❌ PDF解析失败: {str(e)}")
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
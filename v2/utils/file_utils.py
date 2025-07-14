"""
File utilities for common file operations and data handling.
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
import tempfile

class FileUtils:
    """Utility class for file operations and data handling."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def ensure_directory(self, directory_path: str) -> Path:
        """
        Ensure directory exists, create if it doesn't.
        
        Args:
            directory_path: Path to directory
            
        Returns:
            Path object for the directory
        """
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def save_text_file(self, content: str, file_path: str, encoding: str = 'utf-8') -> str:
        """
        Save text content to file.
        
        Args:
            content: Text content to save
            file_path: Path where to save the file
            encoding: File encoding
            
        Returns:
            Absolute path to saved file
        """
        try:
            path = Path(file_path)
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding=encoding) as file:
                file.write(content)
                
            self.logger.info(f"Saved text file: {file_path}")
            return str(path.absolute())
            
        except Exception as e:
            self.logger.error(f"Error saving text file {file_path}: {str(e)}")
            raise Exception(f"Failed to save text file: {str(e)}")
    
    def load_text_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """
        Load text content from file.
        
        Args:
            file_path: Path to file
            encoding: File encoding
            
        Returns:
            File content as string
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                
            self.logger.info(f"Loaded text file: {file_path}")
            return content
            
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                self.logger.warning(f"Used fallback encoding for: {file_path}")
                return content
            except Exception as e:
                raise Exception(f"Failed to read file with any encoding: {str(e)}")
                
        except Exception as e:
            self.logger.error(f"Error loading text file {file_path}: {str(e)}")
            raise Exception(f"Failed to load text file: {str(e)}")
    
    def save_json(self, data: Dict[str, Any], file_path: str, indent: int = 2) -> str:
        """
        Save data as JSON file.
        
        Args:
            data: Data to save
            file_path: Path where to save the file
            indent: JSON indentation
            
        Returns:
            Absolute path to saved file
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
                
            self.logger.info(f"Saved JSON file: {file_path}")
            return str(path.absolute())
            
        except Exception as e:
            self.logger.error(f"Error saving JSON file {file_path}: {str(e)}")
            raise Exception(f"Failed to save JSON file: {str(e)}")
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Loaded data as dictionary
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            self.logger.info(f"Loaded JSON file: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading JSON file {file_path}: {str(e)}")
            raise Exception(f"Failed to load JSON file: {str(e)}")
    
    def copy_file(self, source_path: str, destination_path: str) -> str:
        """
        Copy file from source to destination.
        
        Args:
            source_path: Source file path
            destination_path: Destination file path
            
        Returns:
            Absolute path to copied file
        """
        try:
            source = Path(source_path)
            destination = Path(destination_path)
            
            if not source.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")
                
            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source, destination)
            
            self.logger.info(f"Copied file: {source_path} -> {destination_path}")
            return str(destination.absolute())
            
        except Exception as e:
            self.logger.error(f"Error copying file: {str(e)}")
            raise Exception(f"Failed to copy file: {str(e)}")
    
    def move_file(self, source_path: str, destination_path: str) -> str:
        """
        Move file from source to destination.
        
        Args:
            source_path: Source file path
            destination_path: Destination file path
            
        Returns:
            Absolute path to moved file
        """
        try:
            source = Path(source_path)
            destination = Path(destination_path)
            
            if not source.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")
                
            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(source), str(destination))
            
            self.logger.info(f"Moved file: {source_path} -> {destination_path}")
            return str(destination.absolute())
            
        except Exception as e:
            self.logger.error(f"Error moving file: {str(e)}")
            raise Exception(f"Failed to move file: {str(e)}")
    
    def remove_file(self, file_path: str) -> bool:
        """
        Remove file if it exists.
        
        Args:
            file_path: Path to file to remove
            
        Returns:
            True if file was removed, False if it didn't exist
        """
        try:
            path = Path(file_path)
            
            if path.exists():
                path.unlink()
                self.logger.info(f"Removed file: {file_path}")
                return True
            else:
                self.logger.warning(f"File not found for removal: {file_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error removing file {file_path}: {str(e)}")
            raise Exception(f"Failed to remove file: {str(e)}")
    
    def remove_directory(self, directory_path: str) -> bool:
        """
        Remove directory and all its contents.
        
        Args:
            directory_path: Path to directory to remove
            
        Returns:
            True if directory was removed, False if it didn't exist
        """
        try:
            path = Path(directory_path)
            
            if path.exists() and path.is_dir():
                shutil.rmtree(path)
                self.logger.info(f"Removed directory: {directory_path}")
                return True
            else:
                self.logger.warning(f"Directory not found for removal: {directory_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error removing directory {directory_path}: {str(e)}")
            raise Exception(f"Failed to remove directory: {str(e)}")
    
    def list_files(self, directory_path: str, pattern: str = "*", 
                  recursive: bool = False) -> List[str]:
        """
        List files in directory matching pattern.
        
        Args:
            directory_path: Directory to search
            pattern: File pattern to match
            recursive: Whether to search recursively
            
        Returns:
            List of file paths
        """
        try:
            path = Path(directory_path)
            
            if not path.exists():
                return []
                
            if recursive:
                files = list(path.rglob(pattern))
            else:
                files = list(path.glob(pattern))
                
            # Filter only files (not directories)
            file_paths = [str(f) for f in files if f.is_file()]
            
            return sorted(file_paths)
            
        except Exception as e:
            self.logger.error(f"Error listing files in {directory_path}: {str(e)}")
            return []
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in bytes
        """
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0
    
    def create_temp_file(self, content: str, suffix: str = ".tmp") -> str:
        """
        Create temporary file with content.
        
        Args:
            content: Content to write to file
            suffix: File suffix
            
        Returns:
            Path to temporary file
        """
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, 
                                           delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
                
            self.logger.info(f"Created temporary file: {temp_path}")
            return temp_path
            
        except Exception as e:
            self.logger.error(f"Error creating temporary file: {str(e)}")
            raise Exception(f"Failed to create temporary file: {str(e)}")
    
    def validate_path(self, file_path: str) -> Dict[str, Any]:
        """
        Validate file path and return information.
        
        Args:
            file_path: Path to validate
            
        Returns:
            Dictionary with validation results
        """
        path = Path(file_path)
        
        return {
            'exists': path.exists(),
            'is_file': path.is_file() if path.exists() else False,
            'is_directory': path.is_dir() if path.exists() else False,
            'is_absolute': path.is_absolute(),
            'suffix': path.suffix,
            'parent_exists': path.parent.exists(),
            'size': self.get_file_size(file_path) if path.exists() else 0,
            'readable': os.access(path, os.R_OK) if path.exists() else False,
            'writable': os.access(path, os.W_OK) if path.exists() else False
        } 
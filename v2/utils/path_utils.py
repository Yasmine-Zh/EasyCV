"""
Cross-platform path utilities for EasyCV
Ensures compatibility between Windows and macOS/Linux
"""

import os
import sys
from pathlib import Path
from typing import Union, List, Optional


def normalize_path(path: Union[str, Path]) -> Path:
    """
    Normalize a path to be cross-platform compatible
    
    Args:
        path: Input path as string or Path object
        
    Returns:
        Normalized Path object
    """
    if isinstance(path, str):
        path = Path(path)
    
    # Resolve relative paths and normalize
    return path.expanduser().resolve()


def safe_join(*paths: Union[str, Path]) -> Path:
    """
    Safely join multiple path components
    
    Args:
        *paths: Path components to join
        
    Returns:
        Joined and normalized Path object
    """
    if not paths:
        return Path.cwd()
    
    base_path = normalize_path(paths[0])
    
    for path_component in paths[1:]:
        if isinstance(path_component, str):
            path_component = Path(path_component)
        base_path = base_path / path_component
    
    return base_path.resolve()


def create_safe_directory(path: Union[str, Path]) -> Path:
    """
    Create a directory safely with cross-platform compatibility
    
    Args:
        path: Directory path to create
        
    Returns:
        Created directory path
    """
    normalized_path = normalize_path(path)
    normalized_path.mkdir(parents=True, exist_ok=True)
    return normalized_path


def get_valid_filename(filename: str) -> str:
    """
    Create a valid filename for both Windows and Unix systems
    
    Args:
        filename: Original filename
        
    Returns:
        Valid filename
    """
    # Characters that are invalid in Windows filenames
    invalid_chars = '<>:"/\\|?*'
    
    # Replace invalid characters with underscores
    valid_filename = filename
    for char in invalid_chars:
        valid_filename = valid_filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    valid_filename = valid_filename.strip(' .')
    
    # Ensure filename is not empty
    if not valid_filename:
        valid_filename = "untitled"
    
    # Truncate if too long (Windows has 255 char limit)
    if len(valid_filename) > 255:
        name, ext = os.path.splitext(valid_filename)
        max_name_len = 255 - len(ext)
        valid_filename = name[:max_name_len] + ext
    
    return valid_filename


def get_temp_dir() -> Path:
    """
    Get a cross-platform temporary directory
    
    Returns:
        Temporary directory path
    """
    import tempfile
    return Path(tempfile.gettempdir())


def get_home_dir() -> Path:
    """
    Get user's home directory in a cross-platform way
    
    Returns:
        User's home directory path
    """
    return Path.home()


def get_desktop_dir() -> Optional[Path]:
    """
    Get user's desktop directory if it exists
    
    Returns:
        Desktop directory path or None if not found
    """
    home = get_home_dir()
    
    # Try common desktop directory names
    desktop_names = ['Desktop', 'desktop']
    
    for name in desktop_names:
        desktop_path = home / name
        if desktop_path.exists() and desktop_path.is_dir():
            return desktop_path
    
    return None


def get_documents_dir() -> Optional[Path]:
    """
    Get user's documents directory if it exists
    
    Returns:
        Documents directory path or None if not found
    """
    home = get_home_dir()
    
    # Try common documents directory names
    doc_names = ['Documents', 'documents', 'My Documents']
    
    for name in doc_names:
        doc_path = home / name
        if doc_path.exists() and doc_path.is_dir():
            return doc_path
    
    return None


def is_safe_path(path: Union[str, Path], base_dir: Optional[Union[str, Path]] = None) -> bool:
    """
    Check if a path is safe (no directory traversal attacks)
    
    Args:
        path: Path to check
        base_dir: Base directory to restrict to (optional)
        
    Returns:
        True if path is safe, False otherwise
    """
    try:
        normalized_path = normalize_path(path)
        
        if base_dir:
            base_normalized = normalize_path(base_dir)
            # Check if the path is within the base directory
            try:
                normalized_path.relative_to(base_normalized)
                return True
            except ValueError:
                return False
        
        # Basic safety check - no parent directory traversal
        path_str = str(normalized_path)
        return '..' not in path_str and not path_str.startswith('/')
        
    except (OSError, ValueError):
        return False


def get_file_extension(filename: Union[str, Path]) -> str:
    """
    Get file extension in lowercase
    
    Args:
        filename: Filename or path
        
    Returns:
        File extension (including dot) in lowercase
    """
    if isinstance(filename, Path):
        return filename.suffix.lower()
    return Path(filename).suffix.lower()


def list_files_by_extension(directory: Union[str, Path], 
                          extensions: List[str]) -> List[Path]:
    """
    List files in directory with specific extensions
    
    Args:
        directory: Directory to search
        extensions: List of extensions (e.g., ['.pdf', '.docx'])
        
    Returns:
        List of matching file paths
    """
    dir_path = normalize_path(directory)
    
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    
    # Normalize extensions to lowercase
    extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                 for ext in extensions]
    
    matching_files = []
    
    try:
        for file_path in dir_path.iterdir():
            if file_path.is_file() and get_file_extension(file_path) in extensions:
                matching_files.append(file_path)
    except (OSError, PermissionError):
        pass
    
    return sorted(matching_files)


# Platform-specific utilities
def get_platform_info() -> dict:
    """
    Get platform information
    
    Returns:
        Dictionary with platform details
    """
    return {
        'system': sys.platform,
        'is_windows': sys.platform.startswith('win'),
        'is_macos': sys.platform == 'darwin',
        'is_linux': sys.platform.startswith('linux'),
        'path_separator': os.sep,
        'path_list_separator': os.pathsep
    } 
"""
Markdown generator for resume profiles.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class MarkdownGenerator:
    """Generator for markdown format resume profiles."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate(self, profile_data: Dict[str, Any], output_dir: Path, 
                profile_name: str, version: str) -> Path:
        """
        Generate markdown resume file.
        
        Args:
            profile_data: Profile content and metadata
            output_dir: Directory for output files
            profile_name: Name of the profile
            version: Version string
            
        Returns:
            Path to generated markdown file
        """
        try:
            # Generate filename
            filename = f"{profile_name}.{version}.md"
            output_path = output_dir / filename
            
            # Get content from profile data
            content = profile_data.get('content', '')
            
            # Add metadata header if not present
            if not content.startswith('---'):
                metadata_header = self._generate_metadata_header(profile_data, profile_name, version)
                content = metadata_header + '\n\n' + content
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            self.logger.info(f"Generated markdown file: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating markdown: {str(e)}")
            raise Exception(f"Failed to generate markdown file: {str(e)}")
    
    def _generate_metadata_header(self, profile_data: Dict[str, Any], 
                                profile_name: str, version: str) -> str:
        """Generate YAML metadata header for markdown file."""
        created_at = profile_data.get('created_at', datetime.now().isoformat())
        
        header = f"""---
title: "{profile_name} Resume"
version: "{version}"
created_at: "{created_at}"
generated_by: "EasyCV"
---"""
        
        return header
    
    def update_content(self, markdown_path: Path, new_content: str) -> Path:
        """
        Update existing markdown file with new content.
        
        Args:
            markdown_path: Path to existing markdown file
            new_content: New content to write
            
        Returns:
            Path to updated file
        """
        try:
            with open(markdown_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
                
            self.logger.info(f"Updated markdown file: {markdown_path}")
            return markdown_path
            
        except Exception as e:
            self.logger.error(f"Error updating markdown: {str(e)}")
            raise Exception(f"Failed to update markdown file: {str(e)}")
    
    def read_content(self, markdown_path: Path) -> str:
        """
        Read content from markdown file.
        
        Args:
            markdown_path: Path to markdown file
            
        Returns:
            File content as string
        """
        try:
            with open(markdown_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            return content
            
        except Exception as e:
            self.logger.error(f"Error reading markdown: {str(e)}")
            raise Exception(f"Failed to read markdown file: {str(e)}")
    
    def extract_metadata(self, markdown_content: str) -> Dict[str, Any]:
        """
        Extract YAML metadata from markdown content.
        
        Args:
            markdown_content: Markdown content with potential YAML front matter
            
        Returns:
            Dictionary of metadata
        """
        metadata = {}
        
        if not markdown_content.startswith('---'):
            return metadata
            
        try:
            # Find end of YAML front matter
            lines = markdown_content.split('\n')
            yaml_end = -1
            
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    yaml_end = i
                    break
            
            if yaml_end > 0:
                yaml_content = '\n'.join(lines[1:yaml_end])
                
                # Simple YAML parsing (for basic key-value pairs)
                for line in yaml_content.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        metadata[key] = value
                        
        except Exception as e:
            self.logger.warning(f"Error parsing metadata: {str(e)}")
            
        return metadata
    
    def remove_metadata(self, markdown_content: str) -> str:
        """
        Remove YAML metadata from markdown content.
        
        Args:
            markdown_content: Markdown content with potential YAML front matter
            
        Returns:
            Content without metadata
        """
        if not markdown_content.startswith('---'):
            return markdown_content
            
        lines = markdown_content.split('\n')
        yaml_end = -1
        
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                yaml_end = i
                break
        
        if yaml_end > 0:
            return '\n'.join(lines[yaml_end + 1:]).lstrip('\n')
        else:
            return markdown_content
    
    def format_content(self, content: str, style_preferences: Optional[Dict[str, Any]] = None) -> str:
        """
        Format markdown content according to style preferences.
        
        Args:
            content: Raw markdown content
            style_preferences: Formatting preferences
            
        Returns:
            Formatted markdown content
        """
        if not style_preferences:
            return content
            
        # Apply basic formatting rules
        formatted = content
        
        # Example formatting rules (can be expanded)
        if style_preferences.get('heading_style') == 'atx':
            # Ensure ATX style headings (# ## ###)
            pass
        elif style_preferences.get('heading_style') == 'setext':
            # Convert to setext style headings where appropriate
            pass
            
        if style_preferences.get('line_breaks') == 'double':
            # Ensure double line breaks between sections
            formatted = formatted.replace('\n\n\n', '\n\n')
            
        return formatted
    
    def validate_markdown(self, content: str) -> Dict[str, Any]:
        """
        Validate markdown content and return analysis.
        
        Args:
            content: Markdown content to validate
            
        Returns:
            Validation results
        """
        lines = content.split('\n')
        
        # Count different elements
        headings = len([line for line in lines if line.strip().startswith('#')])
        lists = len([line for line in lines if line.strip().startswith(('- ', '* ', '+ ', '1.'))])
        links = content.count('[')
        
        # Check for common sections
        common_sections = ['experience', 'education', 'skills', 'contact']
        found_sections = []
        
        content_lower = content.lower()
        for section in common_sections:
            if section in content_lower:
                found_sections.append(section)
        
        return {
            'total_lines': len(lines),
            'non_empty_lines': len([line for line in lines if line.strip()]),
            'headings': headings,
            'lists': lists,
            'links': links,
            'found_sections': found_sections,
            'has_metadata': content.startswith('---'),
            'word_count': len(content.split()),
            'character_count': len(content)
        } 
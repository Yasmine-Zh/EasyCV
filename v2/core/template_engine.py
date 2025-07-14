"""
Template engine for processing resume templates and variable substitution.
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class TemplateEngine:
    """Template engine for processing resume templates with variable substitution."""
    
    def __init__(self, template_dir: str = "templates"):
        """
        Initialize template engine.
        
        Args:
            template_dir: Directory containing template files
        """
        self.template_dir = Path(template_dir)
        self.logger = logging.getLogger(__name__)
        
        # Variable pattern for template substitution
        self.variable_pattern = re.compile(r'\{\{(\w+)\}\}')
        
    def load_template(self, template_name: str) -> str:
        """
        Load template content from file.
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Template content as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
            
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.logger.info(f"Loaded template: {template_name}")
                return content
        except Exception as e:
            raise Exception(f"Error loading template {template_name}: {str(e)}")
    
    def process_template(self, template_content: str, variables: Dict[str, Any]) -> str:
        """
        Process template by substituting variables.
        
        Args:
            template_content: Template content with variables
            variables: Dictionary of variables to substitute
            
        Returns:
            Processed template with variables substituted
        """
        try:
            # Simple variable substitution
            processed = template_content
            
            for key, value in variables.items():
                placeholder = f"{{{{{key}}}}}"
                processed = processed.replace(placeholder, str(value))
            
            # Log any unresolved variables
            unresolved = self.variable_pattern.findall(processed)
            if unresolved:
                self.logger.warning(f"Unresolved template variables: {unresolved}")
            
            return processed
            
        except Exception as e:
            self.logger.error(f"Error processing template: {str(e)}")
            raise Exception(f"Template processing failed: {str(e)}")
    
    def extract_template_variables(self, template_content: str) -> List[str]:
        """
        Extract all variable names from template content.
        
        Args:
            template_content: Template content
            
        Returns:
            List of variable names found in template
        """
        return self.variable_pattern.findall(template_content)
    
    def validate_template(self, template_content: str) -> Dict[str, Any]:
        """
        Validate template structure and return analysis.
        
        Args:
            template_content: Template content to validate
            
        Returns:
            Validation results with structure analysis
        """
        variables = self.extract_template_variables(template_content)
        
        # Check for common resume sections
        common_sections = [
            'experience', 'education', 'skills', 'contact', 'summary'
        ]
        
        found_sections = []
        missing_sections = []
        
        content_lower = template_content.lower()
        for section in common_sections:
            if section in content_lower:
                found_sections.append(section)
            else:
                missing_sections.append(section)
        
        return {
            'variables': variables,
            'variable_count': len(variables),
            'found_sections': found_sections,
            'missing_sections': missing_sections,
            'total_lines': len(template_content.splitlines()),
            'is_valid': len(variables) > 0 and len(found_sections) > 0
        }
    
    def create_template_from_content(self, content: str, output_name: str) -> str:
        """
        Create a new template file from provided content.
        
        Args:
            content: Template content
            output_name: Name for the new template file
            
        Returns:
            Path to created template file
        """
        template_path = self.template_dir / output_name
        
        # Ensure template directory exists
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(content)
                
            self.logger.info(f"Created template: {output_name}")
            return str(template_path)
            
        except Exception as e:
            raise Exception(f"Error creating template {output_name}: {str(e)}")
    
    def list_available_templates(self) -> List[str]:
        """
        List all available template files.
        
        Returns:
            List of template file names
        """
        if not self.template_dir.exists():
            return []
            
        try:
            templates = []
            for file_path in self.template_dir.iterdir():
                if file_path.is_file() and file_path.suffix in ['.md', '.txt']:
                    templates.append(file_path.name)
                    
            return sorted(templates)
            
        except Exception as e:
            self.logger.error(f"Error listing templates: {str(e)}")
            return []
    
    def merge_templates(self, primary_template: str, secondary_template: str, 
                       merge_rules: Optional[Dict[str, str]] = None) -> str:
        """
        Merge two templates based on specified rules.
        
        Args:
            primary_template: Primary template content
            secondary_template: Secondary template content
            merge_rules: Rules for merging (optional)
            
        Returns:
            Merged template content
        """
        # Simple merge implementation - can be enhanced
        if merge_rules is None:
            merge_rules = {}
            
        # For now, just append secondary to primary with a separator
        separator = "\n\n<!-- Merged Content -->\n\n"
        merged = primary_template + separator + secondary_template
        
        self.logger.info("Templates merged successfully")
        return merged
    
    def backup_template(self, template_name: str) -> str:
        """
        Create a backup of an existing template.
        
        Args:
            template_name: Name of template to backup
            
        Returns:
            Path to backup file
        """
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
            
        # Create backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{template_path.stem}_backup_{timestamp}{template_path.suffix}"
        backup_path = self.template_dir / backup_name
        
        try:
            with open(template_path, 'r', encoding='utf-8') as source:
                content = source.read()
                
            with open(backup_path, 'w', encoding='utf-8') as backup:
                backup.write(content)
                
            self.logger.info(f"Created backup: {backup_name}")
            return str(backup_path)
            
        except Exception as e:
            raise Exception(f"Error creating backup: {str(e)}") 
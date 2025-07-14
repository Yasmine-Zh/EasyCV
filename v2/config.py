"""
Configuration settings for EasyCV resume generator.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """Configuration class for EasyCV application."""
    
    # Default settings
    DEFAULT_OUTPUT_DIR = "profiles"
    DEFAULT_TEMPLATE_DIR = "templates"
    DEFAULT_AI_MODEL = "gpt-4"
    DEFAULT_KEEP_VERSIONS = 5
    
    # File format settings
    SUPPORTED_INPUT_FORMATS = {'.pdf', '.docx', '.doc', '.md', '.txt'}
    OUTPUT_FORMATS = ['markdown', 'word', 'html']
    
    # Style themes
    AVAILABLE_THEMES = ['professional', 'modern', 'creative', 'traditional']
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Optional path to configuration file
        """
        self.settings = self._load_default_settings()
        
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_environment()
    
    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default configuration settings."""
        return {
            # Directories
            'output_dir': self.DEFAULT_OUTPUT_DIR,
            'template_dir': self.DEFAULT_TEMPLATE_DIR,
            
            # AI settings
            'openai_api_key': None,
            'ai_model': self.DEFAULT_AI_MODEL,
            'ai_temperature': 0.3,
            'ai_max_tokens': 2000,
            
            # Generation settings
            'keep_versions': self.DEFAULT_KEEP_VERSIONS,
            'auto_cleanup': True,
            'generate_all_formats': True,
            'default_theme': 'professional',
            
            # Output settings
            'include_metadata': True,
            'add_timestamps': True,
            'create_index_html': True,
            'github_pages_config': True,
            
            # Logging
            'log_level': 'INFO',
            'log_file': None,
            
            # Feature flags
            'enable_style_analysis': True,
            'enable_ai_enhancement': True,
            'enable_validation': True,
            
            # Limits
            'max_file_size_mb': 10,
            'max_files_per_batch': 20,
            'timeout_seconds': 300
        }
    
    def _load_from_file(self, config_file: str):
        """Load settings from configuration file."""
        try:
            import json
            
            config_path = Path(config_file)
            if config_path.suffix.lower() == '.json':
                with open(config_path, 'r', encoding='utf-8') as file:
                    file_settings = json.load(file)
                    self.settings.update(file_settings)
            else:
                # Simple key=value format
                with open(config_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Try to convert to appropriate type
                            if value.lower() in ('true', 'false'):
                                value = value.lower() == 'true'
                            elif value.isdigit():
                                value = int(value)
                            elif value.replace('.', '').isdigit():
                                value = float(value)
                                
                            self.settings[key] = value
                            
        except Exception as e:
            raise Exception(f"Error loading config file {config_file}: {str(e)}")
    
    def _load_from_environment(self):
        """Load settings from environment variables."""
        env_mappings = {
            'EASYCV_OUTPUT_DIR': 'output_dir',
            'EASYCV_TEMPLATE_DIR': 'template_dir',
            'OPENAI_API_KEY': 'openai_api_key',
            'EASYCV_AI_MODEL': 'ai_model',
            'EASYCV_LOG_LEVEL': 'log_level',
            'EASYCV_KEEP_VERSIONS': 'keep_versions',
            'EASYCV_DEFAULT_THEME': 'default_theme'
        }
        
        for env_var, setting_key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Type conversion
                if setting_key in ['keep_versions']:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                elif setting_key in ['auto_cleanup', 'generate_all_formats']:
                    value = value.lower() in ('true', '1', 'yes')
                    
                self.settings[setting_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.settings[key] = value
    
    def update(self, new_settings: Dict[str, Any]):
        """
        Update multiple configuration values.
        
        Args:
            new_settings: Dictionary of settings to update
        """
        self.settings.update(new_settings)
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate configuration settings.
        
        Returns:
            Validation results with any errors or warnings
        """
        errors = []
        warnings = []
        
        # Check required settings
        if not self.get('openai_api_key'):
            warnings.append("OpenAI API key not set. AI features will be unavailable.")
        
        # Check directory paths
        for dir_key in ['output_dir', 'template_dir']:
            dir_path = self.get(dir_key)
            if dir_path:
                try:
                    Path(dir_path).mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Cannot create {dir_key} directory '{dir_path}': {str(e)}")
        
        # Check numeric values
        numeric_settings = {
            'keep_versions': (1, 100),
            'ai_temperature': (0.0, 2.0),
            'ai_max_tokens': (100, 4000),
            'max_file_size_mb': (1, 100),
            'max_files_per_batch': (1, 50),
            'timeout_seconds': (30, 3600)
        }
        
        for setting, (min_val, max_val) in numeric_settings.items():
            value = self.get(setting)
            if value is not None:
                try:
                    num_value = float(value)
                    if not (min_val <= num_value <= max_val):
                        warnings.append(f"{setting} value {value} outside recommended range [{min_val}, {max_val}]")
                except (ValueError, TypeError):
                    errors.append(f"{setting} must be a number, got: {value}")
        
        # Check theme
        theme = self.get('default_theme')
        if theme and theme not in self.AVAILABLE_THEMES:
            warnings.append(f"Unknown theme '{theme}'. Available themes: {', '.join(self.AVAILABLE_THEMES)}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI-related configuration."""
        return {
            'api_key': self.get('openai_api_key'),
            'model': self.get('ai_model'),
            'temperature': self.get('ai_temperature'),
            'max_tokens': self.get('ai_max_tokens'),
            'timeout': self.get('timeout_seconds')
        }
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output-related configuration."""
        return {
            'output_dir': self.get('output_dir'),
            'keep_versions': self.get('keep_versions'),
            'auto_cleanup': self.get('auto_cleanup'),
            'generate_all_formats': self.get('generate_all_formats'),
            'include_metadata': self.get('include_metadata'),
            'add_timestamps': self.get('add_timestamps'),
            'default_theme': self.get('default_theme')
        }
    
    def save_to_file(self, config_file: str):
        """
        Save current configuration to file.
        
        Args:
            config_file: Path to save configuration
        """
        try:
            config_path = Path(config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            if config_path.suffix.lower() == '.json':
                import json
                with open(config_path, 'w', encoding='utf-8') as file:
                    json.dump(self.settings, file, indent=2)
            else:
                # Simple key=value format
                with open(config_path, 'w', encoding='utf-8') as file:
                    file.write("# EasyCV Configuration\n")
                    file.write(f"# Generated: {os.getenv('USER', 'unknown')} on {Path.cwd()}\n\n")
                    
                    for key, value in sorted(self.settings.items()):
                        file.write(f"{key}={value}\n")
                        
        except Exception as e:
            raise Exception(f"Error saving config to {config_file}: {str(e)}")
    
    def create_sample_config(self, output_file: str):
        """
        Create a sample configuration file with comments.
        
        Args:
            output_file: Path to create sample config
        """
        sample_content = """# EasyCV Configuration File
# Remove the # to enable a setting

# Directories
#output_dir=profiles
#template_dir=templates

# AI Settings (Required for AI features)
#openai_api_key=your_openai_api_key_here
#ai_model=gpt-4
#ai_temperature=0.3
#ai_max_tokens=2000

# Generation Settings
#keep_versions=5
#auto_cleanup=true
#generate_all_formats=true
#default_theme=professional

# Output Settings
#include_metadata=true
#add_timestamps=true
#create_index_html=true
#github_pages_config=true

# Logging
#log_level=INFO
#log_file=easycv.log

# Feature Flags
#enable_style_analysis=true
#enable_ai_enhancement=true
#enable_validation=true

# Limits
#max_file_size_mb=10
#max_files_per_batch=20
#timeout_seconds=300
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(sample_content)
        except Exception as e:
            raise Exception(f"Error creating sample config: {str(e)}")

# Global configuration instance
config = Config() 
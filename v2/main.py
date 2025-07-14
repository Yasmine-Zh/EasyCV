"""
Main entry point for EasyCV resume generator.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional

# Add the v2 directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from core import DocumentParser, AIProcessor, TemplateEngine, OutputGenerator
from utils import FileUtils

class EasyCVApp:
    """Main application class for EasyCV."""
    
    def __init__(self):
        """Initialize the application."""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.document_parser = DocumentParser()
        self.template_engine = TemplateEngine(config.get('template_dir'))
        self.output_generator = OutputGenerator(config.get('output_dir'))
        self.file_utils = FileUtils()
        
        # AI processor (initialized when needed)
        self.ai_processor = None
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_level = getattr(logging, config.get('log_level', 'INFO').upper())
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                *([logging.FileHandler(config.get('log_file'))] if config.get('log_file') else [])
            ]
        )
    
    def initialize_ai_processor(self):
        """Initialize AI processor if not already done."""
        if self.ai_processor is None:
            try:
                ai_config = config.get_ai_config()
                if ai_config['api_key']:
                    self.ai_processor = AIProcessor(
                        api_key=ai_config['api_key'],
                        model=ai_config['model']
                    )
                    self.logger.info("AI processor initialized successfully")
                else:
                    raise ValueError("OpenAI API key not configured")
            except Exception as e:
                self.logger.error(f"Failed to initialize AI processor: {str(e)}")
                raise
    
    def generate_initial_profile(self, profile_name: str, documents: List[str], 
                               job_description: str, template_path: str,
                               style_reference: Optional[str] = None) -> str:
        """
        Generate initial profile from documents and job description.
        
        Args:
            profile_name: Name for the profile
            documents: List of input document paths
            job_description: Job description text or file path
            template_path: Path to template file
            style_reference: Optional style reference content
            
        Returns:
            Path to output directory
        """
        try:
            self.logger.info(f"Starting initial profile generation for: {profile_name}")
            
            # Validate inputs
            self._validate_inputs(documents, template_path)
            
            # Parse documents
            self.logger.info("Parsing input documents...")
            documents_text = self.document_parser.parse_documents(documents)
            
            # Load job description
            jd_text = self._load_job_description(job_description)
            
            # Load template
            template_content = self.template_engine.load_template(template_path)
            
            # Initialize AI processor
            self.initialize_ai_processor()
            
            # Extract relevant experience using AI
            self.logger.info("Extracting relevant experience with AI...")
            extracted_info = self.ai_processor.extract_relevant_experience(
                documents_text, jd_text
            )
            
            # Generate profile content
            self.logger.info("Generating profile content...")
            profile_content = self.ai_processor.generate_profile_from_template(
                template_content, extracted_info, profile_name, jd_text
            )
            
            # Analyze style if reference provided
            style_analysis = None
            if style_reference and config.get('enable_style_analysis'):
                self.logger.info("Analyzing style reference...")
                style_analysis = self.ai_processor.analyze_resume_style(style_reference)
            
            # Prepare profile data
            profile_data = {
                'content': profile_content,
                'profile_name': profile_name,
                'source_documents': documents,
                'job_description': jd_text,
                'template_path': template_path,
                'style_reference': style_reference
            }
            
            # Generate all output formats
            self.logger.info("Generating output files...")
            output_paths = self.output_generator.generate_complete_profile(
                profile_data, profile_name, style_analysis
            )
            
            output_dir = Path(output_paths['markdown']).parent
            self.logger.info(f"Profile generation completed successfully: {output_dir}")
            
            return str(output_dir)
            
        except Exception as e:
            self.logger.error(f"Error generating profile: {str(e)}")
            raise
    
    def update_existing_profile(self, old_profile_path: str, new_documents: List[str],
                              new_job_description: Optional[str] = None) -> str:
        """
        Update an existing profile with new information.
        
        Args:
            old_profile_path: Path to existing markdown profile
            new_documents: List of new document paths
            new_job_description: Optional new job description
            
        Returns:
            Path to new output directory
        """
        try:
            self.logger.info(f"Updating existing profile: {old_profile_path}")
            
            # Validate inputs
            if not Path(old_profile_path).exists():
                raise FileNotFoundError(f"Profile not found: {old_profile_path}")
            
            # Load old profile
            old_content = self.file_utils.load_text_file(old_profile_path)
            
            # Parse new documents
            new_documents_text = self.document_parser.parse_documents(new_documents)
            
            # Load new job description if provided
            new_jd_text = None
            if new_job_description:
                new_jd_text = self._load_job_description(new_job_description)
            
            # Initialize AI processor
            self.initialize_ai_processor()
            
            # Update profile content
            self.logger.info("Updating profile content with AI...")
            updated_content = self.ai_processor.update_existing_profile(
                old_content, new_documents_text, new_jd_text
            )
            
            # Generate updated outputs
            self.logger.info("Generating updated output files...")
            output_paths = self.output_generator.update_existing_profile(
                old_profile_path, updated_content
            )
            
            output_dir = Path(output_paths['markdown']).parent
            self.logger.info(f"Profile update completed successfully: {output_dir}")
            
            return str(output_dir)
            
        except Exception as e:
            self.logger.error(f"Error updating profile: {str(e)}")
            raise
    
    def list_profiles(self) -> List[dict]:
        """List all available profiles."""
        return self.output_generator.list_profiles()
    
    def cleanup_old_versions(self, profile_name: str, keep_versions: Optional[int] = None):
        """Clean up old versions of a profile."""
        keep = keep_versions or config.get('keep_versions')
        removed = self.output_generator.cleanup_old_versions(profile_name, keep)
        self.logger.info(f"Cleaned up {len(removed)} old versions for {profile_name}")
        return removed
    
    def _validate_inputs(self, documents: List[str], template_path: str):
        """Validate input files."""
        # Validate documents
        errors = self.document_parser.validate_files(documents)
        if errors:
            raise ValueError(f"Document validation errors: {'; '.join(errors)}")
        
        # Validate template
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # Check file sizes
        max_size = config.get('max_file_size_mb', 10) * 1024 * 1024
        for doc_path in documents:
            size = Path(doc_path).stat().st_size
            if size > max_size:
                raise ValueError(f"File too large: {doc_path} ({size / 1024 / 1024:.1f}MB)")
        
        # Check batch size
        if len(documents) > config.get('max_files_per_batch', 20):
            raise ValueError(f"Too many files. Maximum: {config.get('max_files_per_batch')}")
    
    def _load_job_description(self, job_description: str) -> str:
        """Load job description from text or file."""
        if Path(job_description).exists():
            return self.file_utils.load_text_file(job_description)
        else:
            return job_description

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="EasyCV - AI-powered resume generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate new profile
  python main.py generate --profile john_doe --docs cv.pdf projects.md --jd job_desc.txt --template template.md

  # Update existing profile
  python main.py update --old-profile profiles/john_doe/v20240101/john_doe.v20240101.md --docs new_project.pdf

  # List all profiles
  python main.py list

  # Clean up old versions
  python main.py cleanup --profile john_doe --keep 3
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate new profile')
    gen_parser.add_argument('--profile', required=True, help='Profile name')
    gen_parser.add_argument('--docs', nargs='+', required=True, help='Input documents (PDF, DOCX, MD, TXT)')
    gen_parser.add_argument('--jd', required=True, help='Job description (text or file path)')
    gen_parser.add_argument('--template', required=True, help='Template file path')
    gen_parser.add_argument('--style', help='Style reference content or file path')
    gen_parser.add_argument('--output-dir', help='Output directory (overrides config)')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update existing profile')
    update_parser.add_argument('--old-profile', required=True, help='Path to existing markdown profile')
    update_parser.add_argument('--docs', nargs='+', required=True, help='New documents to incorporate')
    update_parser.add_argument('--jd', help='New job description (optional)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all profiles')
    list_parser.add_argument('--detailed', action='store_true', help='Show detailed information')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up old profile versions')
    cleanup_parser.add_argument('--profile', required=True, help='Profile name')
    cleanup_parser.add_argument('--keep', type=int, help='Number of versions to keep')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_parser.add_argument('--validate', action='store_true', help='Validate configuration')
    config_parser.add_argument('--sample', help='Create sample config file')
    config_parser.add_argument('--show', action='store_true', help='Show current configuration')
    
    # Global options
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Log level')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI features')
    
    return parser

def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Load configuration
        if args.config:
            config._load_from_file(args.config)
        
        # Override log level if specified
        if args.log_level:
            config.set('log_level', args.log_level)
        
        # Initialize app
        app = EasyCVApp()
        
        # Execute command
        if args.command == 'generate':
            if args.output_dir:
                config.set('output_dir', args.output_dir)
            
            output_dir = app.generate_initial_profile(
                profile_name=args.profile,
                documents=args.docs,
                job_description=args.jd,
                template_path=args.template,
                style_reference=args.style
            )
            print(f"Profile generated successfully: {output_dir}")
            
        elif args.command == 'update':
            output_dir = app.update_existing_profile(
                old_profile_path=args.old_profile,
                new_documents=args.docs,
                new_job_description=args.jd
            )
            print(f"Profile updated successfully: {output_dir}")
            
        elif args.command == 'list':
            profiles = app.list_profiles()
            if not profiles:
                print("No profiles found.")
            else:
                print(f"Found {len(profiles)} profiles:")
                for profile in profiles:
                    if args.detailed:
                        print(f"  {profile['name']} (v{profile['latest_version']}) - {profile['last_updated']}")
                        print(f"    Versions: {profile['total_versions']}")
                        print(f"    Output: {profile['output_dir']}")
                    else:
                        print(f"  {profile['name']} (v{profile['latest_version']})")
                        
        elif args.command == 'cleanup':
            removed = app.cleanup_old_versions(args.profile, args.keep)
            print(f"Removed {len(removed)} old versions: {', '.join(removed)}")
            
        elif args.command == 'config':
            if args.validate:
                validation = config.validate()
                if validation['valid']:
                    print("Configuration is valid.")
                else:
                    print("Configuration issues found:")
                    for error in validation['errors']:
                        print(f"  ERROR: {error}")
                for warning in validation['warnings']:
                    print(f"  WARNING: {warning}")
                    
            elif args.sample:
                config.create_sample_config(args.sample)
                print(f"Sample configuration created: {args.sample}")
                
            elif args.show:
                print("Current configuration:")
                for key, value in sorted(config.settings.items()):
                    print(f"  {key}: {value}")
                    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
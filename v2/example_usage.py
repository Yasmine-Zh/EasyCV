#!/usr/bin/env python3
"""
Example usage script for EasyCV - demonstrates basic functionality
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demonstrate_config():
    """Demonstrate configuration management"""
    print("=== EasyCV Configuration Demo ===")
    
    try:
        from config import config
        
        print("Default configuration:")
        for key, value in sorted(config.settings.items()):
            print(f"  {key}: {value}")
        
        print("\nCreating sample configuration file...")
        config.create_sample_config("sample_config.txt")
        print("Sample configuration created: sample_config.txt")
        
        print("\nValidating configuration...")
        validation = config.validate()
        if validation['valid']:
            print("✓ Configuration is valid")
        else:
            print("✗ Configuration has issues:")
            for error in validation['errors']:
                print(f"  ERROR: {error}")
        
        for warning in validation['warnings']:
            print(f"  WARNING: {warning}")
            
    except Exception as e:
        print(f"Error demonstrating config: {e}")

def demonstrate_document_parsing():
    """Demonstrate document parsing capabilities"""
    print("\n=== Document Parser Demo ===")
    
    try:
        from core.document_parser import DocumentParser
        
        parser = DocumentParser(verbose=True)
        
        print("Supported formats:", parser.SUPPORTED_FORMATS)
        
        # Create a sample text file for testing
        sample_file = "sample_document.txt"
        with open(sample_file, 'w') as f:
            f.write("""John Doe Resume
            
Experience:
- Software Engineer at TechCorp (2020-2023)
- Intern at StartupXYZ (2019-2020)

Skills:
- Python, JavaScript, React
- Machine Learning, Data Analysis
- Project Management
""")
        
        print(f"\nParsing sample document: {sample_file}")
        result = parser.parse_documents([sample_file])
        
        for file_path, content in result.items():
            print(f"\nContent from {file_path}:")
            print(content[:200] + "..." if len(content) > 200 else content)
        
        # Clean up
        os.remove(sample_file)
        print(f"\nCleaned up sample file: {sample_file}")
        
    except Exception as e:
        print(f"Error demonstrating document parsing: {e}")

def demonstrate_template_engine():
    """Demonstrate template engine capabilities"""
    print("\n=== Template Engine Demo ===")
    
    try:
        from core.template_engine import TemplateEngine
        
        engine = TemplateEngine()
        
        # Create a simple template
        template_content = """# {{name}} Resume

## Contact Information
- Email: {{email}}
- Phone: {{phone}}

## Experience
{{experience}}

## Skills
{{skills}}
"""
        
        print("Sample template:")
        print(template_content)
        
        # Process template with sample data
        variables = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0123',
            'experience': 'Software Engineer with 5 years experience',
            'skills': 'Python, JavaScript, Machine Learning'
        }
        
        processed = engine.process_template(template_content, variables)
        
        print("\nProcessed template:")
        print(processed)
        
        # Validate template
        validation = engine.validate_template(template_content)
        print(f"\nTemplate validation:")
        print(f"  Variables found: {validation['variables']}")
        print(f"  Sections found: {validation['found_sections']}")
        print(f"  Is valid: {validation['is_valid']}")
        
    except Exception as e:
        print(f"Error demonstrating template engine: {e}")

def demonstrate_version_management():
    """Demonstrate version management"""
    print("\n=== Version Manager Demo ===")
    
    try:
        from utils.version_manager import VersionManager
        
        vm = VersionManager()
        
        # Generate versions
        version1 = vm.generate_version()
        print(f"Generated version: {version1}")
        
        # Parse version info
        version_info = vm.get_version_info(version1)
        print(f"Version info: {version_info}")
        
        # Test version comparison
        versions = [version1, vm.generate_version()]
        sorted_versions = vm.sort_versions(versions)
        print(f"Sorted versions: {sorted_versions}")
        
        latest = vm.get_latest_version(versions)
        print(f"Latest version: {latest}")
        
    except Exception as e:
        print(f"Error demonstrating version management: {e}")

def demonstrate_generators():
    """Demonstrate output generators"""
    print("\n=== Output Generators Demo ===")
    
    try:
        from generators.markdown_generator import MarkdownGenerator
        
        generator = MarkdownGenerator()
        
        # Sample profile data
        profile_data = {
            'content': """# John Doe Resume

## Experience
Senior Software Engineer at TechCorp (2020-2023)
- Led development of microservices architecture
- Improved system performance by 40%

## Skills
- Python, JavaScript, React
- AWS, Docker, Kubernetes
- Machine Learning, Data Analysis
""",
            'profile_name': 'john_doe',
            'created_at': '2024-01-01T12:00:00'
        }
        
        # Create output directory
        output_dir = Path("demo_output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate markdown
        md_path = generator.generate(profile_data, output_dir, "john_doe", "v20240101")
        print(f"Generated markdown: {md_path}")
        
        # Validate generated content
        with open(md_path, 'r') as f:
            content = f.read()
            
        validation = generator.validate_markdown(content)
        print(f"Markdown validation: {validation}")
        
        # Clean up
        import shutil
        shutil.rmtree(output_dir)
        print("Cleaned up demo output directory")
        
    except Exception as e:
        print(f"Error demonstrating generators: {e}")

def main():
    """Main demonstration function"""
    print("EasyCV - AI-Powered Resume Generator")
    print("=" * 50)
    print("This script demonstrates the core functionality of EasyCV")
    print("without requiring OpenAI API keys or external dependencies.")
    print()
    
    # Run demonstrations
    demonstrate_config()
    demonstrate_document_parsing()
    demonstrate_template_engine()
    demonstrate_version_management()
    demonstrate_generators()
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")
    print("\nTo use EasyCV with AI features:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run: python main.py generate --help")

if __name__ == "__main__":
    main() 
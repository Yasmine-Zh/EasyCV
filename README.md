# EasyCV - AI-Powered Resume Generator

EasyCV is an intelligent resume generation tool that uses AI to create professional, tailored resumes from your existing documents and job descriptions. It generates multiple output formats including Markdown, Word documents, and responsive HTML websites.

## Features

- **AI-Powered Content Generation**: Uses OpenAI GPT models to extract and optimize your experience for specific job requirements
- **Multiple Input Formats**: Supports PDF, DOCX, Markdown, and text files
- **Multiple Output Formats**: Generates Markdown, Word documents, and responsive HTML websites
- **Style Analysis**: Analyzes reference resumes to match formatting preferences
- **Version Management**: Automatic versioning and cleanup of old resume versions
- **GitHub Pages Ready**: Generates websites ready for deployment to GitHub Pages
- **Template System**: Flexible template system for different resume layouts
- **Command Line Interface**: Easy-to-use CLI for batch processing and automation

## Project Structure

```
EasyCV/
├── v2/                          # Main application (latest version)
│   ├── core/                    # Core functionality modules
│   │   ├── document_parser.py   # Document parsing (PDF, DOCX, MD, TXT)
│   │   ├── ai_processor.py      # AI content generation and optimization
│   │   ├── template_engine.py   # Template processing and management
│   │   └── output_generator.py  # Multi-format output generation
│   ├── utils/                   # Utility modules
│   │   ├── file_utils.py        # File operations and management
│   │   └── version_manager.py   # Version control for profiles
│   ├── generators/              # Format-specific generators
│   │   ├── markdown_generator.py # Markdown output
│   │   ├── word_generator.py     # Word document output
│   │   └── website_generator.py  # HTML/website output
│   ├── templates/               # Resume templates
│   ├── static/                  # Static assets for websites
│   ├── main.py                  # Main CLI application
│   ├── config.py               # Configuration management
│   └── requirements.txt        # Python dependencies
├── templates/                   # Global templates
│   └── Personal_Profile_Template.md
├── v1/                         # Legacy version
├── css/                        # Shared stylesheets
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for AI features)

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/your-username/EasyCV.git
cd EasyCV

# Install Python dependencies
cd v2
pip install -r requirements.txt
```

### Configuration

1. **Set up OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

2. **Create configuration file** (optional):
   ```bash
   python main.py config --sample config.txt
   # Edit config.txt with your preferences
   ```

## Usage

### Basic Usage

#### Generate a New Resume

```bash
cd v2
python main.py generate \
  --profile john_doe \
  --docs /path/to/old_resume.pdf /path/to/projects.md \
  --jd "Job description text or /path/to/job_description.txt" \
  --template ../templates/Personal_Profile_Template.md
```

#### Update an Existing Resume

```bash
python main.py update \
  --old-profile profiles/john_doe/v202401011200/john_doe.v202401011200.md \
  --docs /path/to/new_project.pdf \
  --jd "New job description"
```

#### List All Profiles

```bash
python main.py list --detailed
```

#### Clean Up Old Versions

```bash
python main.py cleanup --profile john_doe --keep 3
```

### Advanced Usage

#### With Style Reference

```bash
python main.py generate \
  --profile jane_smith \
  --docs resume.docx portfolio.md \
  --jd job_posting.txt \
  --template template.md \
  --style reference_resume.pdf
```

#### Custom Configuration

```bash
python main.py generate \
  --profile john_doe \
  --docs resume.pdf \
  --jd job.txt \
  --template template.md \
  --config custom_config.txt \
  --output-dir custom_output
```

## Configuration Options

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for AI features)
- `EASYCV_OUTPUT_DIR`: Default output directory
- `EASYCV_TEMPLATE_DIR`: Default template directory
- `EASYCV_AI_MODEL`: AI model to use (default: gpt-4)
- `EASYCV_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Configuration File

Create a configuration file to customize EasyCV behavior:

```bash
python main.py config --sample config.txt
```

Example configuration:
```
# AI Settings
openai_api_key=your_key_here
ai_model=gpt-4
ai_temperature=0.3

# Output Settings  
output_dir=my_profiles
keep_versions=5
generate_all_formats=true
default_theme=professional

# Feature Flags
enable_style_analysis=true
enable_ai_enhancement=true
```

## Output Formats

### 1. Markdown (`profile_name.version.md`)
- Structured markdown with YAML front matter
- Easy to edit and version control
- Compatible with static site generators

### 2. Word Document (`profile_name.version.docx`)
- Professional formatting
- Ready for printing or email
- Maintains consistent styling

### 3. HTML Website (`profile_name.version.html`)
- Responsive design
- Multiple themes (professional, modern, creative, traditional)
- GitHub Pages ready
- Includes CSS and configuration files

## File Organization

Generated files are organized as follows:

```
profiles/
└── john_doe/
    ├── v202401011200/
    │   ├── john_doe.v202401011200.md      # Markdown resume
    │   ├── john_doe.v202401011200.docx    # Word document
    │   ├── john_doe.v202401011200.html    # HTML website
    │   ├── styles.css                     # Website styles
    │   ├── _config.yml                    # GitHub Pages config
    │   ├── index.html                     # Redirect page
    │   └── metadata.json                  # Generation metadata
    └── v202401021400/
        └── ... (newer version)
```

## Templates

### Using Existing Templates

The project includes a default template at `templates/Personal_Profile_Template.md`. You can use it as-is or modify it for your needs.

### Creating Custom Templates

Templates are markdown files with optional variable substitution:

```markdown
# {{profile_name}} Resume

## Experience
{{experience_content}}

## Skills
{{skills_content}}
```

Variables are automatically populated by the AI processor.

## Themes

EasyCV supports multiple visual themes for HTML output:

- **Professional**: Clean, business-appropriate styling
- **Modern**: Contemporary design with subtle colors
- **Creative**: More colorful, suitable for creative roles
- **Traditional**: Classic, conservative formatting

Themes are automatically selected based on AI analysis of your style reference or can be set manually in configuration.

## Development

### Running Tests

```bash
cd v2
pytest tests/
```

### Code Formatting

```bash
black .
flake8 .
mypy .
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Ensure your API key is set correctly
   - Check your OpenAI account has sufficient credits
   - Verify the model name is correct

2. **Document Parsing Errors**
   - Ensure input files are not corrupted
   - Check file permissions
   - Verify file formats are supported

3. **Output Generation Errors**
   - Check available disk space
   - Ensure output directory is writable
   - Verify all dependencies are installed

### Debug Mode

Run with debug logging to troubleshoot issues:

```bash
python main.py generate --log-level DEBUG [other options]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT models
- The Python community for excellent libraries
- Contributors and users of EasyCV

## Support

For support, please:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information about your problem

---

**Note**: This is version 2 of EasyCV with significant improvements over v1. For legacy support, see the `v1/` directory.
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
- **Web Interface**: User-friendly Gradio-based web interface for easy file upload and resume generation (双版本支持：标准版和兼容版)
- **Cross-Platform**: Compatible with Windows, macOS, and Linux systems
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
│   │   ├── version_manager.py   # Version control for profiles
│   │   └── path_utils.py        # Cross-platform path handling
│   ├── generators/              # Format-specific generators
│   │   ├── markdown_generator.py # Markdown output
│   │   ├── word_generator.py     # Word document output
│   │   └── website_generator.py  # HTML/website output
│   ├── web/                     # Web interface
│   │   ├── gradio_app.py        # Gradio-based web UI (标准版本)
│   │   ├── gradio_app_simple.py # Gradio-based web UI (简化版本)
│   │   └── gradio_app_minimal.py # Gradio-based web UI (超简版本)
│   ├── templates/               # Resume templates
│   ├── static/                  # Static assets for websites
│   ├── main.py                  # Main CLI application
│   ├── launch_ui.py            # Web interface launcher (标准版本)
│   ├── launch_ui_simple.py     # Web interface launcher (简化版本)
│   ├── launch_ui_minimal.py    # Web interface launcher (超简版本)
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

EasyCV provides two main ways to use the tool: a user-friendly **Web Interface** for beginners and a powerful **Command Line Interface** for advanced users and automation.

### 🌐 Web Interface (Recommended for Beginners)

The web interface provides an intuitive, point-and-click experience for resume generation.

#### Quick Start

EasyCV provides **three versions** of the web interface to accommodate different environments and compatibility needs:

**🚀 Standard Version (Full Features)**
```bash
cd v2
python launch_ui.py
```
- 完整功能的Gradio界面
- 支持Python 3.9+
- 包含所有高级特性和组件
- 可能遇到Gradio兼容性问题

**🔧 Simple Version (Balanced)**
```bash
cd v2
python launch_ui_simple.py
```
- 简化的Gradio界面，兼容性更好
- 支持Python 3.8+
- 基础功能完整，适合旧版Python环境
- 仍可能遇到JSON schema错误

**⚡ Minimal Version (Maximum Compatibility)**
```bash
cd v2
python launch_ui_minimal.py
```
- 超级简化界面，使用最基本组件
- 支持Python 3.8+
- 功能有限但兼容性最好
- 专为解决Gradio兼容性问题设计

#### 版本选择指南

| 特性 | 标准版本 | 简化版本 | 超简版本 |
|------|----------|----------|----------|
| Python要求 | 3.9+ | 3.8+ | 3.8+ |
| 功能完整度 | 完整 | 基础 | 有限 |
| 界面复杂度 | 完整功能 | 简化界面 | 最简界面 |
| 兼容性 | 一般 | 良好 | 最佳 |
| 推荐场景 | 最新环境 | 一般环境 | 兼容性问题 |

**推荐使用顺序**: 标准版本 → 简化版本 → 超简版本

**如果遇到`TypeError: argument of type 'bool' is not iterable`等Gradio错误，请使用超简版本。**

#### 使用步骤

1. **选择并启动版本**：根据上述指南选择合适的启动脚本

2. **访问浏览器界面**: 
   - 界面将自动在默认浏览器中打开
   - 或手动访问: `http://localhost:7860`

3. **上传并生成简历**:
   - 上传现有简历/文档 (PDF, DOCX, Markdown, TXT)
   - 输入目标职位描述
   - 点击"生成简历"
   - 下载专业格式化的简历

#### Web Interface Features

- **📁 Drag & Drop File Upload**: Easily upload multiple documents
- **🎯 Job-Targeted Optimization**: Paste job descriptions for AI optimization
- **📝 Template Customization**: Edit resume templates in real-time
- **🎨 Style Reference**: Upload reference resumes for style matching
- **📊 Multi-Format Output**: Generate Markdown, Word, and HTML simultaneously
- **📂 Profile Management**: View and manage existing resume profiles
- **🔧 Cross-Platform**: Works on Windows, macOS, and Linux

#### Supported File Types

- **Input**: PDF, DOCX, Markdown (.md), Plain Text (.txt)
- **Output**: Markdown (.md), Word (.docx), HTML website

#### Platform Compatibility

The web interface automatically handles file paths for different operating systems:
- **Windows**: `C:\Users\Username\Documents\resume.pdf`
- **macOS**: `/Users/Username/Documents/resume.pdf`
- **Linux**: `/home/username/Documents/resume.pdf`

### 📟 Command Line Interface

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

### 🌐 语言支持 / Language Support

EasyCV supports generating resumes in multiple languages:

#### Web Interface
- **English**: 完全的英文简历生成，使用专业的美式英语术语
- **Chinese**: 完全的中文简历生成，使用专业的中文术语
- **Bilingual**: 双语简历，同时包含英文和中文内容

#### Command Line Interface
```bash
# Generate English resume (default)
python main.py generate --profile john_doe --docs cv.pdf --jd job_desc.txt --template templates/English_Resume_Template.md --language english

# Generate Chinese resume
python main.py generate --profile 张三 --docs cv.pdf --jd job_desc.txt --template templates/Personal_Profile_Template.md --language chinese

# Generate bilingual resume
python main.py generate --profile john_doe --docs cv.pdf --jd job_desc.txt --template templates/English_Resume_Template.md --language bilingual
```

#### 确保英文简历质量 / Ensuring English Resume Quality

1. **使用英文模板**: 
   - Web界面: 选择"English"语言选项
   - CLI: 使用 `--language english` 参数

2. **AI指令优化**: 系统会自动向AI发送明确的英文生成指令
   - 强制使用美式英语术语
   - 确保所有输出内容都是英文
   - 优化简历的专业性和可读性

3. **模板选择**:
   - 使用专门的英文模板: `templates/English_Resume_Template.md`
   - 或自定义英文格式的模板

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

4. **Web Interface Issues**
   - **Interface won't start**: Check if Gradio is installed (`pip install gradio>=4.0.0`)
   - **JSON Schema错误 (`bool is not iterable`)**: 使用超简版本 `python launch_ui_minimal.py`
   - **Gradio组件兼容性错误**: 切换到简化版本 `python launch_ui_simple.py`
   - **Python 3.8兼容性问题**: 使用简化版本或超简版本
   - **复杂界面组件报错**: 标准版本需要Python 3.9+，否则使用其他版本
   - **File upload fails**: Ensure file size is under 100MB and format is supported
   - **Cross-platform path errors**: The tool automatically handles Windows/macOS paths
   - **Port already in use**: Try changing the port: `python launch_ui.py --server-port 7861`
   - **Browser doesn't open**: Manually visit `http://localhost:7860`
   
   **版本选择建议**:
   - 如果遇到`TypeError: argument of type 'bool' is not iterable`，使用超简版本
   - 如果遇到任何Gradio相关错误，优先尝试简化版本
   - 标准版本适合Python 3.9+环境且无兼容性问题
   - 简化版本提供更好的向下兼容性
   - 超简版本专为解决深层Gradio兼容性问题设计

### Debug Mode

**For Command Line Interface:**
```bash
python main.py generate --log-level DEBUG [other options]
```

**For Web Interface:**
```bash
# Launch with debug mode
cd v2
python -c "
from web.gradio_app import EasyCVGradioApp
app = EasyCVGradioApp()
app.launch(debug=True)
"
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
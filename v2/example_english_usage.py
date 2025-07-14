#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English Resume Generation Example for EasyCV

This example demonstrates how to generate English resumes using EasyCV.
"""

def example_web_interface():
    """Example: Using Web Interface for English Resume"""
    print("""
🌐 Web Interface - English Resume Generation

1. Start the web interface:
   cd v2
   python launch_ui.py

2. In the browser interface:
   - Select "English" from the "Resume Language" dropdown
   - Upload your documents (PDF, DOCX, etc.)
   - Enter the job description in English
   - Click "Generate Resume"
   - Download your English resume

The AI will automatically:
- Extract information from your documents
- Generate content in professional American English
- Use proper English terminology and formatting
- Optimize for the target job description
""")

def example_cli_usage():
    """Example: Using CLI for English Resume"""
    print("""
💻 Command Line Interface - English Resume Generation

Basic English resume generation:
python main.py generate \\
    --profile john_doe \\
    --docs cv.pdf projects.md \\
    --jd job_description.txt \\
    --template templates/English_Resume_Template.md \\
    --language english

With style reference:
python main.py generate \\
    --profile jane_smith \\
    --docs resume.pdf portfolio.md \\
    --jd job_desc.txt \\
    --template templates/English_Resume_Template.md \\
    --style reference_resume.pdf \\
    --language english

The system will:
- Parse all input documents
- Extract relevant experience
- Generate content in English only
- Apply the English template
- Create professional output files
""")

def example_ai_instructions():
    """Example: AI instructions for English generation"""
    print("""
🤖 AI Processing for English Resumes

The system automatically sends these instructions to the AI:

System Message:
"You are a professional resume writer who creates tailored resumes in ENGLISH language 
based on specific templates and job requirements. Always respond in ENGLISH only."

Prompt Instructions:
1. **LANGUAGE**: Generate ALL content in ENGLISH only. Use professional American English terminology.
2. Follow the exact structure and format of the template
3. Replace placeholder content with relevant information
4. Ensure all sections are filled appropriately
5. Maintain professional language and formatting
6. Include quantifiable achievements where possible
7. Use keywords from the job description naturally
8. ALL output must be in ENGLISH language only

This ensures high-quality, professional English resumes every time.
""")

if __name__ == "__main__":
    print("=== EasyCV English Resume Generation Examples ===")
    
    example_web_interface()
    example_cli_usage()
    example_ai_instructions()
    
    print("""
🎯 Quick Tips for Best English Resumes:

1. Use the dedicated English template: templates/English_Resume_Template.md
2. Provide job descriptions in English for better keyword matching
3. Upload documents with clear, well-structured content
4. Select "English" language option in web interface
5. Use --language english parameter in CLI

For maximum compatibility, use the minimal version if you encounter any issues:
python launch_ui_minimal.py
""") 
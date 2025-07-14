import gradio as gr
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import os
from src.resume_generator import ResumeGenerator

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    raise ValueError("OPENAI_API_KEY not set in environment")


def generate(profile_name, jd_text, template_file, doc_files):
    version = ResumeGenerator(profile_name).generate_version()
    generator = ResumeGenerator(profile_name)

    # Save uploaded files
    temp_dir = tempfile.mkdtemp()
    saved_docs = []
    for f in doc_files:
        path = Path(temp_dir) / f.name
        path.write_bytes(f.read())
        saved_docs.append(str(path))

    template_path = Path(temp_dir) / template_file.name
    template_path.write_bytes(template_file.read())

    md_path, output_dir = generator.generate_markdown_profile(
        saved_docs, jd_text, template_path, version
    )
    doc_path, html_path = generator.generate_outputs(md_path, output_dir, version)

    return str(md_path), str(doc_path), str(html_path)


demo = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="Profile Name"),
        gr.Textbox(lines=8, label="Target Job Description"),
        gr.File(label="Markdown Template (.md)"),
        gr.File(file_types=[".pdf", ".docx", ".md", ".txt"], label="Historical Documents", file_count="multiple")
    ],
    outputs=[
        gr.Textbox(label="Generated Markdown Path"),
        gr.Textbox(label="Generated Word Resume Path"),
        gr.Textbox(label="Generated HTML Resume Path")
    ],
    title="AI Resume Generator",
    description="Upload your experience documents, a markdown resume template, and a job description to generate customized resumes."
)

demo.launch()

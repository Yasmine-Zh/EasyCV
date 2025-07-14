from pathlib import Path
from markdown2 import markdown
import docx
import openai
from .utils import extract_text_from_file, load_text_file

class ResumeGenerator:
    def __init__(self, profile_name, base_dir="profiles"):
        self.profile_name = profile_name
        self.base_dir = Path(base_dir)

    def generate_version(self):
        from datetime import datetime
        return f"v{datetime.now().strftime('%Y%m%d%H%M')}"

    def create_output_dir(self, version):
        output_dir = self.base_dir / self.profile_name / version
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def generate_markdown_profile(self, documents, jd_text, template_path, version):
        extracted_info = self.extract_info_from_documents(documents, jd_text)
        markdown_text = self.fill_template_with_info(template_path, extracted_info)

        output_dir = self.create_output_dir(version)
        md_file_path = output_dir / f"{self.profile_name}.{version}.md"
        md_file_path.write_text(markdown_text, encoding="utf-8")
        return md_file_path, output_dir

    def generate_outputs(self, markdown_path, output_dir, version):
        md_text = markdown_path.read_text(encoding="utf-8")

        doc_path = output_dir / f"{self.profile_name}.{version}.docx"
        self.convert_markdown_to_word(md_text, doc_path)

        html_path = output_dir / f"{self.profile_name}.{version}.html"
        html_path.write_text(markdown(md_text), encoding="utf-8")

        return doc_path, html_path

    def extract_info_from_documents(self, documents, jd_text):
        all_text = "\n\n".join(extract_text_from_file(doc) for doc in documents)
        prompt = f"""
Extract and summarize the most relevant experience from the following user documents to match the job description.

Job Description:
{jd_text}

User Documents:
{all_text}

Format your response as markdown under headings like Experience, Skills, Education, etc.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

    def fill_template_with_info(self, template_path, extracted_info):
        return extracted_info  # Placeholder, can be templated

    def convert_markdown_to_word(self, md_text, doc_path):
        doc = docx.Document()
        for line in md_text.splitlines():
            doc.add_paragraph(line)
        doc.save(doc_path)

    def merge_old_and_new_info(self, old_md_path, new_inputs, new_jd_text):
        old_text = load_text_file(old_md_path)
        new_text = "\n\n".join(extract_text_from_file(doc) for doc in new_inputs)
        prompt = f"""
Update the following markdown resume using these new materials and job description.

Old Resume:
{old_text}

New Inputs:
{new_text}

New Job Description:
{new_jd_text}

Return updated markdown resume.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

    def parse_filename(self, md_path):
        parts = Path(md_path).stem.split(".")
        return parts[0], parts[1]

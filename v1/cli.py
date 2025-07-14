# === This file will be renamed to cli.py or main.py ===
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from src.resume_generator import ResumeGenerator
from src.utils import extract_text_from_file


def main():
    parser = argparse.ArgumentParser(description="Generate structured resumes using AI")
    parser.add_argument("--profile", required=True, help="Profile name")
    parser.add_argument("--docs", nargs="+", required=True, help="List of input files (PDF, DOCX, MD, etc.)")
    parser.add_argument("--jd", required=True, help="Path to job description file")
    parser.add_argument("--template", required=True, help="Path to markdown template file")
    parser.add_argument("--base_dir", default="profiles", help="Base output directory")
    parser.add_argument("--openai_key_env", default="OPENAI_API_KEY", help="Environment variable for OpenAI API key")
    args = parser.parse_args()

    load_dotenv()
    import openai
    openai.api_key = os.getenv(args.openai_key_env)
    if not openai.api_key:
        raise ValueError("OpenAI API key not found in environment variable")

    jd_text = Path(args.jd).read_text(encoding="utf-8")
    generator = ResumeGenerator(args.profile, args.base_dir)
    version = generator.generate_version()

    md_path, output_dir = generator.generate_markdown_profile(args.docs, jd_text, args.template, version)
    generator.generate_outputs(md_path, output_dir, version)
    print(f"Files saved to: {output_dir}")


if __name__ == "__main__":
    main()

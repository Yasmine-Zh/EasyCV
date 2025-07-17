import argparse
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def render_resume(json_path: Path, template_path: Path, output_path: Path = None):
    # 加载 JSON 简历数据
    with open(json_path, "r", encoding="utf-8") as f:
        resume_data = json.load(f)

    # 设置 Jinja2 环境
    env = Environment(loader=FileSystemLoader(template_path.parent))
    template = env.get_template(template_path.name)

    # 渲染 HTML 内容
    rendered_html = template.render(**resume_data)

    # 生成默认输出路径
    if output_path is None:
        suffix = f".rendered_{template_path.stem}.html"
        output_path = Path(f"{json_path.with_suffix(suffix)}")

    # 写入 HTML 文件
    output_path.write_text(rendered_html, encoding="utf-8")
    print(f"[✔] Resume rendered successfully → {output_path.resolve()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render HTML resume using a JSON profile and Jinja2 template.")
    parser.add_argument("profile_json", type=Path, help="Path to resume JSON data file")
    parser.add_argument("template_html", type=Path, help="Path to Jinja2-compatible HTML template")
    parser.add_argument("--output", type=Path, help="Optional output HTML file path")

    args = parser.parse_args()

    render_resume(args.profile_json, args.template_html, args.output)

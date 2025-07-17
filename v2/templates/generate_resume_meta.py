# Re-import necessary modules due to state reset
import json
import yaml
from pathlib import Path

# UK Quantitative Analyst resume content
quant_resume = {
    "name": "James Carter",
    "email": "james.carter@financehub.uk",
    "phone": "+44 7911 123456",
    "location": "London, UK",
    "linkedin": "https://linkedin.com/in/jamescarter-quant",
    "summary": "Quantitative Analyst with 7+ years of experience in financial modelling, derivatives pricing, and systematic trading strategies. Strong background in stochastic calculus, statistical arbitrage, and Python-based backtesting frameworks.",
    "experiences": [
        {
            "organization": "Rothwell Capital",
            "time": "2020 - Present",
            "title": "Senior Quantitative Analyst",
            "content": (
                "• Designed and backtested options volatility arbitrage strategies, achieving a Sharpe ratio > 2.1 over 3 years.\n"
                "• Built pricing models for exotic derivatives (barrier options, callable swaps) using finite difference methods.\n"
                "• Collaborated with traders and risk teams to calibrate real-time VaR models under Basel III.\n"
                "• Deployed live models on a custom Python/C++ low-latency framework."
            )
        },
        {
            "organization": "Astor Global Markets",
            "time": "2016 - 2020",
            "title": "Quant Analyst",
            "content": (
                "• Developed factor-based equity trading strategies across UK and EU markets.\n"
                "• Used PCA, Lasso regression, and co-integration to model relative value signals.\n"
                "• Delivered alpha generation tools integrated into front-office dashboards."
            )
        },
        {
            "organization": "HSBC Global Banking & Markets",
            "time": "2014 - 2016",
            "title": "Graduate Analyst (Quant Rotation)",
            "content": (
                "• Rotated across risk, fixed income, and FX quant teams.\n"
                "• Implemented Monte Carlo engine for pricing convertible bonds in C++.\n"
                "• Automated stress testing scenarios using historical and hypothetical shocks."
            )
        }
    ],
    "education": [
        {
            "school": "University of Cambridge",
            "degree": "MPhil in Statistical Finance",
            "time": "2013 - 2014",
            "content": "Dissertation: 'Numerical Techniques in Option Pricing under Jump Diffusion Models'."
        },
        {
            "school": "University of Warwick",
            "degree": "BSc in Mathematics and Economics",
            "time": "2010 - 2013",
            "content": "Graduated First Class Honours. Modules included stochastic processes, econometrics, game theory."
        }
    ],
    "skills": [
        {"skill": "Python (NumPy, pandas, PyTorch)", "degree": "Expert"},
        {"skill": "C++ (QuantLib, Eigen)", "degree": "Advanced"},
        {"skill": "Matlab & R", "degree": "Intermediate"},
        {"skill": "Derivatives Pricing", "degree": "Expert"},
        {"skill": "Statistical Modelling", "degree": "Advanced"},
        {"skill": "Backtesting & Portfolio Optimization", "degree": "Advanced"},
        {"skill": "Bloomberg/Reuters API", "degree": "Intermediate"},
        {"skill": "Git/Linux", "degree": "Intermediate"}
    ],
    "achievements": [
        "Won 1st place in Global Derivatives Challenge 2022 (London Round).",
        "Published paper in Wilmott Journal: 'Pricing American Options with Stochastic Volatility'.",
        "Passed CFA Level II; FRM Certified (2021)."
    ]
}


def render_markdown_header(data):
    name = data.get("name", "").upper()
    contact = f"{data.get('email', '')} | {data.get('location', '')} | {data.get('phone', '')} | {data.get('linkedin', '')}"
    return (
        f'<p align="center" style="line-height: 1.2; margin: 0;">'
        f'<strong style="font-size: 2em;">{name}</strong><br>'
        f'<small>{contact}</small>'
        f'</p>'
    )


def render_skills_table_3col(skills):
    def format_cell(skill):
        return f"{skill['skill']} ({skill['degree']})"

    rows = []
    for i in range(0, len(skills), 3):
        row = skills[i:i+3]
        cells = [format_cell(s) for s in row]
        while len(cells) < 3:
            cells.append("")  # pad if not divisible by 3
        rows.append("\t\t".join(cells))

    # header = "| Skill | Skill | Skill |"
    # divider = "|-------|-------|-------|"
    # return "\n".join([divider] + rows)

    return "\n".join(rows)


def render_markdown_body(data):
    lines = [render_markdown_header(data), ""]
    # lines = [f"# {data['name']}", f'<p align="center"><sub> {data["email"]} | {data["phone"]} | {data["location"]} | {data["linkedin"]}</sub></p>', ""] 
    # lines += [f'<p align="center"><sub> {data["email"]} | {data["phone"]} | {data["location"]} | {data["linkedin"]}</sub></p>', ""]
    lines += [f"## Summary", data["summary"], ""]

    if "experiences" in data:
        lines.append("## Work Experience")
        for exp in data["experiences"]:
            lines.append(f"**{exp['title']}**, {exp['organization']} ({exp['time']})")
            lines.append(exp["content"])
            lines.append("")

    if "education" in data:
        lines.append("## Education")
        for edu in data["education"]:
            lines.append(f"**{edu['degree']}**, {edu['school']} ({edu['time']})")
            lines.append(edu["content"])
            lines.append("")

    if "skills" in data:
        lines.append("## Skills")
        lines.append(render_skills_table_3col(data["skills"]))
        lines.append("")

        # for s in data["skills"]:
        #     lines.append(f"- {s['skill']} ({s['degree']})")
        # lines.append("")

    if "achievements" in data:
        lines.append("## Achievements")
        for a in data["achievements"]:
            lines.append(f"- {a}")
        lines.append("")

    return "\n".join(lines)

# Save JSON and Markdown+YAML
Path("structured_templates").mkdir(exist_ok=True)

with open("/Users/zhangyaxuan/Projects/EasyCV/v2/templates/sample_template_uk_quant.json", "w", encoding="utf-8") as f:
    json.dump(quant_resume, f, indent=2)

yaml_text_quant = yaml.dump(quant_resume, sort_keys=False, allow_unicode=True)
markdown_body = render_markdown_body(quant_resume)
md_output_quant = f"---\n{yaml_text_quant}---\n\n{markdown_body}"

with open("/Users/zhangyaxuan/Projects/EasyCV/v2/templates/sample_template_uk_quant.md", "w", encoding="utf-8") as f:
    f.write(md_output_quant)

md_output_quant[:1000]  # Preview

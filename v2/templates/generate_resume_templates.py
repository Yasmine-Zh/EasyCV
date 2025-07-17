# Recreate the template directory after kernel reset
from pathlib import Path
template_dir = Path("v2/templates/resume_html_templates")
template_dir.mkdir(parents=True, exist_ok=True)

# Clean and compact HTML resume template variants
templates = {
    "clean_compact_1.html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ name }} - Resume</title>
    <style>
        body { font-family: Helvetica, sans-serif; font-size: 14px; margin: 30px auto; max-width: 720px; color: #333; }
        h1 { text-align: center; font-size: 26px; margin: 0; }
        .contact { text-align: center; font-size: 12px; margin-bottom: 16px; }
        h2 { font-size: 18px; border-bottom: 1px solid #ccc; margin-top: 20px; margin-bottom: 8px; }
        .job, .edu { margin-bottom: 8px; }
        ul { margin-top: 4px; margin-bottom: 4px; padding-left: 20px; }
        li { margin-bottom: 2px; }
    </style>
</head>
<body>
    <h1>{{ name }}</h1>
    <div class="contact">{{ location }} · {{ email }} · {{ phone }}</div>

    <h2>Summary</h2>
    <p>{{ summary }}</p>

    <h2>Experience</h2>
    {% for exp in experiences %}
    <div class="job"><strong>{{ exp.title }}</strong>, {{ exp.organization }} ({{ exp.time }})</div>
    <ul>
        {% for line in exp.content.split('\\n') %}
        <li>{{ line }}</li>
        {% endfor %}
    </ul>
    {% endfor %}

    <h2>Education</h2>
    {% for edu in education %}
    <div class="edu"><strong>{{ edu.degree }}</strong>, {{ edu.school }} ({{ edu.time }})</div>
    <p>{{ edu.content }}</p>
    {% endfor %}

    <h2>Skills</h2>
    <ul>
        {% for skill in skills %}
        <li>{{ skill.skill }} ({{ skill.degree }})</li>
        {% endfor %}
    </ul>

    <h2>Achievements</h2>
    <ul>
        {% for ach in achievements %}
        <li>{{ ach }}</li>
        {% endfor %}
    </ul>
</body>
</html>
""",
    "clean_compact_2.html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ name }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; font-size: 13px; margin: 2em auto; max-width: 700px; }
        h1 { text-align: center; font-size: 24px; margin-bottom: 4px; }
        .meta { text-align: center; font-size: 11px; color: #555; margin-bottom: 20px; }
        h2 { font-size: 16px; border-bottom: 1px solid #ccc; margin-top: 24px; }
        .section { margin-bottom: 12px; }
        ul { padding-left: 1.2em; margin: 0; }
        li { margin: 2px 0; }
    </style>
</head>
<body>
    <h1>{{ name }}</h1>
    <div class="meta">{{ location }} · {{ email }} · {{ phone }}</div>

    <div class="section">
        <h2>Summary</h2>
        <p>{{ summary }}</p>
    </div>

    <div class="section">
        <h2>Experience</h2>
        {% for exp in experiences %}
        <p><strong>{{ exp.title }}</strong>, {{ exp.organization }} ({{ exp.time }})</p>
        <ul>
            {% for line in exp.content.split('\\n') %}
            <li>{{ line }}</li>
            {% endfor %}
        </ul>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Education</h2>
        {% for edu in education %}
        <p><strong>{{ edu.degree }}</strong>, {{ edu.school }} ({{ edu.time }})</p>
        <p>{{ edu.content }}</p>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Skills</h2>
        <ul>
            {% for skill in skills %}
            <li>{{ skill.skill }} ({{ skill.degree }})</li>
            {% endfor %}
        </ul>
    </div>

    <div class="section">
        <h2>Achievements</h2>
        <ul>
            {% for ach in achievements %}
            <li>{{ ach }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""
}

# Write all templates to disk
for filename, html in templates.items():
    (template_dir / filename).write_text(html.strip(), encoding="utf-8")

list(template_dir.glob("clean_*.html"))


# 修改 clean_compact_2.html 模板，增强公司突出 + 时间靠右 + 内容小字号紧凑布局

new_clean_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ name }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; font-size: 13px; margin: 2em auto; max-width: 700px; }
        h1 { text-align: center; font-size: 24px; margin-bottom: 4px; }
        .meta { text-align: center; font-size: 11px; color: #555; margin-bottom: 20px; }
        h2 { font-size: 16px; border-bottom: 1px solid #ccc; margin-top: 24px; }
        .section { margin-bottom: 12px; }
        .header-line { display: flex; justify-content: space-between; font-weight: bold; }
        .subpoints { font-size: 12px; margin: 0 0 6px 1em; padding-left: 1em; color: #333; }
        ul.subpoints { list-style: disc; margin-top: 4px; }
        li { margin: 2px 0; }
    </style>
</head>
<body>
    <h1>{{ name }}</h1>
    <div class="meta">{{ location }} · {{ email }} · {{ phone }}</div>

    <div class="section">
        <h2>Summary</h2>
        <p>{{ summary }}</p>
    </div>

    <div class="section">
        <h2>Experience</h2>
        {% for exp in experiences %}
        <div class="header-line">
            <div>{{ exp.title }}, <strong>{{ exp.organization }}</strong></div>
            <div>{{ exp.time }}</div>
        </div>
        <ul class="subpoints">
            {% for line in exp.content.split('\\n') %}
            <li>{{ line }}</li>
            {% endfor %}
        </ul>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Education</h2>
        {% for edu in education %}
        <div class="header-line">
            <div><strong>{{ edu.school }}</strong>, {{ edu.degree }}</div>
            <div>{{ edu.time }}</div>
        </div>
        <p class="subpoints">{{ edu.content }}</p>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Skills</h2>
        <ul class="subpoints">
            {% for skill in skills %}
            <li>{{ skill.skill }} ({{ skill.degree }})</li>
            {% endfor %}
        </ul>
    </div>

    <div class="section">
        <h2>Achievements</h2>
        <ul class="subpoints">
            {% for ach in achievements %}
            <li>{{ ach }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

# 保存为新模板文件
new_template_path = template_dir / "clean_compact_emphasis.html"
new_template_path.write_text(new_clean_template.strip(), encoding="utf-8")


# 彩色版本的增强模板：加入人物头像、彩色标题栏、超链接样式
colorful_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ name }}</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            max-width: 800px;
            margin: 2em auto;
            background-color: #f8f9fa;
            color: #212529;
        }
        header {
            background-color: #0077b6;
            color: white;
            padding: 1.2em;
            border-radius: 8px;
            display: flex;
            align-items: center;
        }
        header img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 1.5em;
        }
        .contact {
            font-size: 13px;
            margin-top: 0.5em;
        }
        a {
            color: #f3f3f3;
            text-decoration: underline;
        }
        h2 {
            color: #0077b6;
            border-bottom: 2px solid #dee2e6;
            padding-bottom: 4px;
            margin-top: 28px;
        }
        .section { margin-bottom: 1em; }
        .header-line {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
        }
        .subpoints {
            font-size: 13px;
            margin: 0 0 6px 1em;
            padding-left: 1.2em;
            color: #343a40;
        }
        ul.subpoints { list-style: disc; margin-top: 4px; }
        li { margin: 2px 0; }
    </style>
</head>
<body>
    <header>
        <img src="{{ photo_url or 'https://randomuser.me/api/portraits/men/32.jpg' }}" alt="Profile Photo" />
        <div>
            <h1 style="margin: 0;">{{ name }}</h1>
            <div class="contact">
                {{ location }} · {{ email }} · {{ phone }}<br>
                <a href="{{ linkedin }}">{{ linkedin }}</a>
            </div>
        </div>
    </header>

    <div class="section">
        <h2>Summary</h2>
        <p>{{ summary }}</p>
    </div>

    <div class="section">
        <h2>Experience</h2>
        {% for exp in experiences %}
        <div class="header-line">
            <div>{{ exp.title }}, <strong>{{ exp.organization }}</strong></div>
            <div>{{ exp.time }}</div>
        </div>
        <ul class="subpoints">
            {% for line in exp.content.split('\\n') %}
            <li>{{ line }}</li>
            {% endfor %}
        </ul>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Education</h2>
        {% for edu in education %}
        <div class="header-line">
            <div><strong>{{ edu.school }}</strong>, {{ edu.degree }}</div>
            <div>{{ edu.time }}</div>
        </div>
        <p class="subpoints">{{ edu.content }}</p>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Skills</h2>
        <ul class="subpoints">
            {% for skill in skills %}
            <li>{{ skill.skill }} ({{ skill.degree }})</li>
            {% endfor %}
        </ul>
    </div>

    <div class="section">
        <h2>Achievements</h2>
        <ul class="subpoints">
            {% for ach in achievements %}
            <li>{{ ach }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

# 写入模板文件
color_template_path = template_dir / "clean_colorful_profile.html"
color_template_path.write_text(colorful_template.strip(), encoding="utf-8")



# 彩色版本（无头像版）HTML简历模板，适合无图 GitHub Pages 展示
colorful_no_photo_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ name }}</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            max-width: 800px;
            margin: 2em auto;
            background-color: #f9f9f9;
            color: #212529;
        }
        header {
            background-color: #0077b6;
            color: white;
            padding: 1.2em;
            border-radius: 8px;
            text-align: center;
        }
        .contact {
            font-size: 13px;
            margin-top: 0.3em;
        }
        a {
            color: #f1f1f1;
            text-decoration: underline;
        }
        h2 {
            color: #0077b6;
            border-bottom: 2px solid #dee2e6;
            padding-bottom: 4px;
            margin-top: 28px;
        }
        .section { margin-bottom: 1em; }
        .header-line {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
        }
        .subpoints {
            font-size: 13px;
            margin: 0 0 6px 1em;
            padding-left: 1.2em;
            color: #343a40;
        }
        ul.subpoints { list-style: disc; margin-top: 4px; }
        li { margin: 2px 0; }
    </style>
</head>
<body>
    <header>
        <h1 style="margin: 0;">{{ name }}</h1>
        <div class="contact">
            {{ location }} · {{ email }} · {{ phone }}<br>
            <a href="{{ linkedin }}">{{ linkedin }}</a>
        </div>
    </header>

    <div class="section">
        <h2>Summary</h2>
        <p>{{ summary }}</p>
    </div>

    <div class="section">
        <h2>Experience</h2>
        {% for exp in experiences %}
        <div class="header-line">
            <div>{{ exp.title }}, <strong>{{ exp.organization }}</strong></div>
            <div>{{ exp.time }}</div>
        </div>
        <ul class="subpoints">
            {% for line in exp.content.split('\\n') %}
            <li>{{ line }}</li>
            {% endfor %}
        </ul>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Education</h2>
        {% for edu in education %}
        <div class="header-line">
            <div><strong>{{ edu.school }}</strong>, {{ edu.degree }}</div>
            <div>{{ edu.time }}</div>
        </div>
        <p class="subpoints">{{ edu.content }}</p>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Skills</h2>
        <ul class="subpoints">
            {% for skill in skills %}
            <li>{{ skill.skill }} ({{ skill.degree }})</li>
            {% endfor %}
        </ul>
    </div>

    <div class="section">
        <h2>Achievements</h2>
        <ul class="subpoints">
            {% for ach in achievements %}
            <li>{{ ach }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

# 保存为新模板文件
color_no_img_template_path = template_dir / "clean_colorful_nophoto.html"
color_no_img_template_path.parent.mkdir(parents=True, exist_ok=True)
color_no_img_template_path.write_text(colorful_no_photo_template.strip(), encoding="utf-8")

color_no_img_template_path.name

from docx import Document

# 加载原始 Wonsulting 模板
original_path = "/Users/zhangyaxuan/Projects/EasyCV/v2/templates/resume_docx_templates/wonsulting_resume_template.docx"
doc = Document(original_path)

# 定义替换词典：原文 -> Jinja2 占位符
replacements = {
    "Name": "{{ name }}",
    "Location": "{{ location }}",
    "LinkedIn": "{{ linkedin }}",
    "Phone Number": "{{ phone }}",
    "Email": "{{ email }}",
    "Github": "{{ github }}",
    "University": "{{ education.school }}",
    "Major/Degree": "{{ education.degree }}",
    "Graduation Date": "{{ education.graduation_date }}",
    "GPA, Organizations, Coursework, etc.": "GPA: {{ education.gpa }} | Organizations: {{ education.organizations }} | Courses: {{ education.courses }}",
    "Company": "{{ job.company }}",
    "Position": "{{ job.position }}",
    "Dates": "{{ job.date }}",
    "Location": "{{ job.location }}",  # 位置字段在教育和工作中通用
    "These skills should be concrete and testable. These should not be soft skills like communication, organizational, and interpersonal skills, but instead incorporated into your bulleted accomplishment statements above. You can add technology skills (Ex: Microsoft Office, Quickbooks, SQL, etc.) and languages (Ex: Spanish, French)": "{{ summary }}",
    "Skills: These skills should be concrete and testable. These should not be soft skills like communication, organizational, and interpersonal skills, but instead incorporated into your bulleted accomplishment statements above. You can add technology skills (Ex: Microsoft Office, Quickbooks, SQL, etc.) and languages (Ex: Spanish, French)": "Skills: {{ skills | join(', ') }}",
    "Achievements: What are you interested in getting into + what do you like to do outside of work/for fun?": "Achievements: {{ achievements }}"
}

# 替换段落内容
for para in doc.paragraphs:
    for key, val in replacements.items():
        if key in para.text:
            inline = para.runs
            for i in range(len(inline)):
                if key in inline[i].text:
                    inline[i].text = inline[i].text.replace(key, val)

# 保存修改后的文档
output_path = "/Users/zhangyaxuan/Projects/EasyCV/v2/templates/resume_docx_templates/clean_resume_template.docx"
doc.save(output_path)


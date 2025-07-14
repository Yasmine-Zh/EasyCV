#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyCV Gradio Web Interface - 超级简化版本
专为解决兼容性问题设计的最小化界面
"""

import os
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any, List, Tuple, Optional, Dict

try:
    import gradio as gr
except ImportError:
    print("❌ Gradio未安装。请运行: pip install gradio>=4.0.0")
    sys.exit(1)

# 添加项目路径到sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 简化的模拟类
class SimpleConfig:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')

class SimpleDocumentParser:
    def parse_document(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return f"已解析文档内容:\n{content[:500]}..." if len(content) > 500 else content
        except Exception as e:
            return f"解析错误: {str(e)}"

class SimpleAIProcessor:
    def __init__(self, config):
        self.config = config
        
    def generate_resume_content(self, **kwargs):
        return {
            'name': kwargs.get('profile_name', '姓名'),
            'experience': '工作经验内容',
            'skills': '技能列表',
            'education': '教育背景',
            'summary': '个人简介'
        }

class SimpleOutputGenerator:
    def __init__(self, config):
        self.config = config
        
    def generate_markdown(self, content, path):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"# {content.get('name', '简历')}\n\n")
                f.write(f"## 个人简介\n{content.get('summary', '')}\n\n")
                f.write(f"## 工作经验\n{content.get('experience', '')}\n\n")
                f.write(f"## 技能\n{content.get('skills', '')}\n\n")
                f.write(f"## 教育背景\n{content.get('education', '')}\n\n")
            return f"✅ Markdown文件已生成: {path}"
        except Exception as e:
            return f"❌ 生成失败: {str(e)}"

class EasyCVMinimalApp:
    def __init__(self):
        self.config = SimpleConfig()
        self.doc_parser = SimpleDocumentParser()
        self.ai_processor = SimpleAIProcessor(self.config)
        self.output_generator = SimpleOutputGenerator(self.config)
        
    def process_files(self, file):
        if not file:
            return "请先上传文件"
        
        try:
            # 简化为单文件处理
            if hasattr(file, 'name'):
                content = self.doc_parser.parse_document(file.name)
                return f"=== {os.path.basename(file.name)} ===\n{content}"
            else:
                return "未能提取到内容"
        except Exception as e:
            return f"处理文件时出错: {str(e)}"
    
    def generate_resume(self, profile_name, job_description, extracted_content, language="English"):
        try:
            if not profile_name:
                return "❌ 请输入个人档案名称", "", ""
            
            # 模拟AI处理
            resume_data = self.ai_processor.generate_resume_content(
                profile_name=profile_name,
                job_description=job_description,
                extracted_content=extracted_content
            )
            
            # 生成输出
            output_dir = Path("profiles") / profile_name / "latest"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            markdown_path = output_dir / "resume.md"
            
            # 根据语言生成不同内容
            if language == "English":
                # 修改resume_data为英文
                resume_data = {
                    'name': resume_data.get('name', profile_name),
                    'summary': resume_data.get('summary', 'Professional summary'),
                    'experience': resume_data.get('experience', 'Work experience'),
                    'skills': resume_data.get('skills', 'Technical skills'),
                    'education': resume_data.get('education', 'Educational background')
                }
                markdown_result = self.output_generator.generate_markdown(resume_data, markdown_path)
            elif language == "Chinese":
                # 修改resume_data为中文
                resume_data = {
                    'name': resume_data.get('name', profile_name),
                    'summary': resume_data.get('summary', '个人简介'),
                    'experience': resume_data.get('experience', '工作经验'),
                    'skills': resume_data.get('skills', '技术技能'),
                    'education': resume_data.get('education', '教育背景')
                }
                markdown_result = self.output_generator.generate_markdown(resume_data, markdown_path)
            else:  # Bilingual
                # 双语版本
                resume_data = {
                    'name': f"{resume_data.get('name', profile_name)} / {resume_data.get('name', profile_name)}",
                    'summary': f"{resume_data.get('summary', 'Professional summary')} / {resume_data.get('summary', '个人简介')}",
                    'experience': f"{resume_data.get('experience', 'Work experience')} / {resume_data.get('experience', '工作经验')}",
                    'skills': f"{resume_data.get('skills', 'Technical skills')} / {resume_data.get('skills', '技术技能')}",
                    'education': f"{resume_data.get('education', 'Educational background')} / {resume_data.get('education', '教育背景')}"
                }
                markdown_result = self.output_generator.generate_markdown(resume_data, markdown_path)
            
            # 读取生成的内容用于下载
            try:
                with open(markdown_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
            except:
                # 如果生成失败，创建基本的英文简历模板
                if language == "English":
                    markdown_content = f"""# {resume_data.get('name', profile_name)}'s Resume

## Personal Summary
{resume_data.get('summary', 'Professional summary to be filled')}

## Work Experience
{resume_data.get('experience', 'Work experience to be filled')}

## Skills
{resume_data.get('skills', 'Technical and soft skills to be listed')}

## Education
{resume_data.get('education', 'Educational background to be filled')}

---
*Generated by EasyCV - AI Resume Generator*
"""
                elif language == "Chinese":
                    markdown_content = f"""# {resume_data.get('name', profile_name)}的简历

## 个人简介
{resume_data.get('summary', '个人简介待填写')}

## 工作经验
{resume_data.get('experience', '工作经验待填写')}

## 技能
{resume_data.get('skills', '技术和软技能待列出')}

## 教育背景
{resume_data.get('education', '教育背景待填写')}

---
*由 EasyCV - AI简历生成器 生成*
"""
                else:  # Bilingual
                    markdown_content = f"""# {resume_data.get('name', profile_name)}'s Resume / {resume_data.get('name', profile_name)}的简历

## Personal Summary / 个人简介
{resume_data.get('summary', 'Professional summary to be filled / 个人简介待填写')}

## Work Experience / 工作经验
{resume_data.get('experience', 'Work experience to be filled / 工作经验待填写')}

## Skills / 技能
{resume_data.get('skills', 'Technical and soft skills to be listed / 技术和软技能待列出')}

## Education / 教育背景
{resume_data.get('education', 'Educational background to be filled / 教育背景待填写')}

---
*Generated by EasyCV - AI Resume Generator / 由 EasyCV - AI简历生成器 生成*
"""
                # 写入文件
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                markdown_result = f"✅ {language} resume generated: {markdown_path}"
            
            return (
                f"✅ 简历生成完成！\n{markdown_result}",
                markdown_content,
                str(markdown_path)
            )
            
        except Exception as e:
            error_msg = f"❌ 生成失败: {str(e)}\n{traceback.format_exc()}"
            return error_msg, "", ""
    
    def create_interface(self):
        # 使用最简单的Gradio组件，去掉所有复杂配置
        with gr.Blocks() as interface:
            
            gr.Markdown("# EasyCV - AI简历生成器")
            gr.Markdown("简化界面版本")
            
            # 去掉Row和Column布局，使用最简单的垂直排列
            profile_name = gr.Textbox(label="个人档案名称")
            
            job_description = gr.Textbox(label="目标职位描述", lines=3)
            
            # 简化Radio组件
            language_choice = gr.Radio(["English", "Chinese", "Bilingual"], value="English", label="简历语言")
            
            # 简化File组件，去掉file_count参数
            uploaded_files = gr.File(label="上传简历文档")
            
            process_btn = gr.Button("处理文件")
            
            extracted_content = gr.Textbox(label="提取的内容", lines=6)
            
            generate_btn = gr.Button("生成简历")
            
            generation_status = gr.Textbox(label="生成状态")
            
            markdown_output = gr.Textbox(label="生成的Markdown", lines=8)
            
            download_path = gr.Textbox(label="文件路径")
            
            # 简化事件绑定
            process_btn.click(
                self.process_files,
                uploaded_files,
                extracted_content
            )
            
            generate_btn.click(
                self.generate_resume,
                inputs=[profile_name, job_description, extracted_content, language_choice],
                outputs=[generation_status, markdown_output, download_path]
            )
            
        return interface
    
    def launch(self, **kwargs):
        interface = self.create_interface()
        
        # 最简单的启动配置，去掉复杂参数
        port = kwargs.get('server_port', 7860)
        share = kwargs.get('share', False)
        
        print(f"""
🚀 EasyCV 简化版启动中...
📍 访问地址: http://localhost:{port}
⚠️  这是简化版本，功能有限但兼容性更好
        """)
        
        # 使用最基本的launch参数
        interface.launch(
            server_port=port,
            share=share
        )

def main():
    try:
        app = EasyCVMinimalApp()
        app.launch()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print(f"🔍 详细错误: {traceback.format_exc()}")

if __name__ == "__main__":
    main() 
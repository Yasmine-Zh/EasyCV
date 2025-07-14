"""
Gradio Web Interface for EasyCV
Provides an easy-to-use web interface for resume generation
"""

import gradio as gr
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.document_parser import DocumentParser
from core.ai_processor import AIProcessor
from core.template_engine import TemplateEngine
from core.output_generator import OutputGenerator
from utils.path_utils import (
    normalize_path, safe_join, create_safe_directory, 
    get_valid_filename, get_temp_dir, get_platform_info
)
from utils.file_utils import FileUtils
from utils.version_manager import VersionManager
from config import ConfigManager


class EasyCVGradioApp:
    """
    Gradio application for EasyCV resume generation
    """
    
    def __init__(self):
        """Initialize the Gradio application"""
        self.config_manager = ConfigManager()
        self.temp_dir = get_temp_dir() / "easycv_temp"
        create_safe_directory(self.temp_dir)
        
        # Initialize components
        self.document_parser = DocumentParser()
        self.ai_processor = AIProcessor(self.config_manager)
        self.template_engine = TemplateEngine()
        self.output_generator = OutputGenerator(self.config_manager)
        self.file_utils = FileUtils()
        self.version_manager = VersionManager()
        
        # Platform info
        self.platform_info = get_platform_info()
        
    def process_uploaded_files(self, files: List[Any]) -> Tuple[str, str]:
        """
        Process uploaded files and extract content
        
        Args:
            files: List of uploaded file objects from Gradio
            
        Returns:
            Tuple of (success_message, extracted_content)
        """
        if not files:
            return "❌ 请至少上传一个文件", ""
            
        try:
            all_content = []
            processed_files = []
            
            for file in files:
                if file is None:
                    continue
                    
                # Get file path
                file_path = Path(file.name)
                
                # Parse document
                content = self.document_parser.parse_document(str(file_path))
                if content.strip():
                    all_content.append(f"=== {file_path.name} ===\n{content}\n")
                    processed_files.append(file_path.name)
                    
            if not all_content:
                return "❌ 无法从上传的文件中提取内容", ""
                
            extracted_text = "\n".join(all_content)
            success_msg = f"✅ 成功处理 {len(processed_files)} 个文件: {', '.join(processed_files)}"
            
            return success_msg, extracted_text
            
        except Exception as e:
            return f"❌ 处理文件时出错: {str(e)}", ""
    
    def generate_resume(self, 
                       profile_name: str,
                       job_description: str,
                       extracted_content: str,
                       template_content: str,
                       style_reference: Optional[Any] = None,
                       output_formats: List[str] = None) -> Tuple[str, str, str, str]:
        """
        Generate resume in multiple formats
        
        Args:
            profile_name: Name for the profile
            job_description: Target job description
            extracted_content: Extracted content from uploaded files
            template_content: Resume template content
            style_reference: Optional style reference file
            output_formats: List of desired output formats
            
        Returns:
            Tuple of (status_message, markdown_path, word_path, html_path)
        """
        try:
            if not profile_name.strip():
                return "❌ 请输入个人档案名称", "", "", ""
                
            if not job_description.strip():
                return "❌ 请输入工作描述", "", "", ""
                
            if not extracted_content.strip():
                return "❌ 请先上传并处理文档", "", "", ""
            
            # Clean profile name
            safe_profile_name = get_valid_filename(profile_name.strip())
            
            # Create version
            version = self.version_manager.create_version()
            
            # Create output directory
            output_dir = create_safe_directory(
                safe_join("profiles", safe_profile_name, f"v{version}")
            )
            
            # Process style reference if provided
            style_content = ""
            if style_reference is not None:
                try:
                    style_path = Path(style_reference.name)
                    style_content = self.document_parser.parse_document(str(style_path))
                except Exception as e:
                    print(f"Warning: Could not process style reference: {e}")
            
            # Generate resume content using AI
            resume_data = self.ai_processor.generate_resume_content(
                experience_docs=extracted_content,
                job_description=job_description,
                style_reference=style_content
            )
            
            # Apply template
            if template_content.strip():
                try:
                    final_content = self.template_engine.apply_template(
                        template_content, 
                        resume_data
                    )
                except Exception as e:
                    print(f"Warning: Template application failed: {e}")
                    final_content = self._format_resume_data(resume_data)
            else:
                final_content = self._format_resume_data(resume_data)
            
            # Generate outputs
            output_files = {}
            
            if not output_formats:
                output_formats = ['markdown', 'word', 'html']
            
            # Generate markdown
            if 'markdown' in output_formats:
                md_path = output_dir / f"{safe_profile_name}.v{version}.md"
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                output_files['markdown'] = str(md_path)
            
            # Generate Word document
            if 'word' in output_formats:
                word_path = output_dir / f"{safe_profile_name}.v{version}.docx"
                try:
                    self.output_generator.generate_word(final_content, str(word_path))
                    output_files['word'] = str(word_path)
                except Exception as e:
                    print(f"Warning: Word generation failed: {e}")
                    output_files['word'] = ""
            
            # Generate HTML website
            if 'html' in output_formats:
                html_path = output_dir / f"{safe_profile_name}.v{version}.html"
                try:
                    self.output_generator.generate_website(
                        final_content, 
                        str(output_dir),
                        f"{safe_profile_name}.v{version}"
                    )
                    output_files['html'] = str(html_path)
                except Exception as e:
                    print(f"Warning: HTML generation failed: {e}")
                    output_files['html'] = ""
            
            # Save metadata
            metadata = {
                'profile_name': safe_profile_name,
                'version': version,
                'timestamp': self.version_manager.get_timestamp(),
                'job_description': job_description,
                'output_formats': output_formats,
                'platform': self.platform_info,
                'files_generated': output_files
            }
            
            metadata_path = output_dir / "metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            success_msg = f"✅ 简历生成成功！\n档案: {safe_profile_name}\n版本: v{version}\n输出目录: {output_dir}"
            
            return (
                success_msg,
                output_files.get('markdown', ''),
                output_files.get('word', ''),
                output_files.get('html', '')
            )
            
        except Exception as e:
            return f"❌ 生成简历时出错: {str(e)}", "", "", ""
    
    def _format_resume_data(self, resume_data: Dict[str, Any]) -> str:
        """
        Format resume data into markdown when template fails
        
        Args:
            resume_data: Dictionary containing resume data
            
        Returns:
            Formatted markdown content
        """
        sections = []
        
        # Header
        if 'name' in resume_data:
            sections.append(f"# {resume_data['name']}")
        
        if 'contact' in resume_data:
            sections.append(f"## 联系信息\n{resume_data['contact']}")
        
        if 'summary' in resume_data:
            sections.append(f"## 个人简介\n{resume_data['summary']}")
        
        if 'experience' in resume_data:
            sections.append(f"## 工作经验\n{resume_data['experience']}")
        
        if 'education' in resume_data:
            sections.append(f"## 教育背景\n{resume_data['education']}")
        
        if 'skills' in resume_data:
            sections.append(f"## 技能\n{resume_data['skills']}")
        
        if 'projects' in resume_data:
            sections.append(f"## 项目经验\n{resume_data['projects']}")
        
        return "\n\n".join(sections)
    
    def list_existing_profiles(self) -> str:
        """
        List existing profiles in the system
        
        Returns:
            Formatted string of existing profiles
        """
        try:
            profiles_dir = Path("profiles")
            if not profiles_dir.exists():
                return "📁 暂无现有档案"
            
            profiles = []
            for profile_dir in profiles_dir.iterdir():
                if profile_dir.is_dir():
                    versions = []
                    for version_dir in profile_dir.iterdir():
                        if version_dir.is_dir() and version_dir.name.startswith('v'):
                            versions.append(version_dir.name)
                    
                    if versions:
                        versions.sort(reverse=True)  # Latest first
                        profiles.append(f"📋 **{profile_dir.name}**\n   版本: {', '.join(versions[:3])}")
            
            if not profiles:
                return "📁 暂无现有档案"
            
            return "📁 **现有档案:**\n\n" + "\n\n".join(profiles)
            
        except Exception as e:
            return f"❌ 获取档案列表时出错: {str(e)}"
    
    def get_default_template(self) -> str:
        """
        Get default template content
        
        Returns:
            Default template content
        """
        default_template = """# {{name}}

## 联系信息
{{contact}}

## 个人简介
{{summary}}

## 工作经验
{{experience}}

## 教育背景
{{education}}

## 技能
{{skills}}

## 项目经验
{{projects}}
"""
        return default_template
    
    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface
        
        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(
            title="EasyCV - AI简历生成器",
            theme=gr.themes.Soft(),
            css="""
            .gradio-container {
                max-width: 1200px !important;
            }
            .file-upload {
                border: 2px dashed #ccc;
                border-radius: 10px;
                text-align: center;
                padding: 20px;
            }
            """
        ) as interface:
            
            gr.Markdown("""
            # 🚀 EasyCV - AI驱动的简历生成器
            
            欢迎使用EasyCV！这是一个智能简历生成工具，可以帮助您：
            - 📄 上传现有简历、项目文档等资料
            - 🎯 根据目标职位描述优化内容
            - 📝 生成多种格式的专业简历（Markdown、Word、HTML）
            - 🎨 应用专业模板和样式
            
            **支持的文件格式:** PDF, DOCX, Markdown (.md), 纯文本 (.txt)
            """)
            
            with gr.Tabs():
                # Tab 1: Generate New Resume
                with gr.Tab("🆕 生成新简历"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            gr.Markdown("### 📋 基本信息")
                            profile_name = gr.Textbox(
                                label="个人档案名称",
                                placeholder="例如: 张三_软件工程师",
                                info="此名称将用于文件命名和组织"
                            )
                            
                            job_description = gr.Textbox(
                                label="目标职位描述",
                                placeholder="粘贴完整的工作描述，或简要描述目标职位要求...",
                                lines=5,
                                info="AI将根据此描述优化您的简历内容"
                            )
                            
                        with gr.Column(scale=1):
                            gr.Markdown("### ⚙️ 生成选项")
                            output_formats = gr.CheckboxGroup(
                                choices=["markdown", "word", "html"],
                                value=["markdown", "word", "html"],
                                label="输出格式",
                                info="选择需要生成的文件格式"
                            )
                    
                    gr.Markdown("### 📁 文档上传")
                    
                    with gr.Row():
                        with gr.Column():
                            uploaded_files = gr.File(
                                label="上传简历和相关文档",
                                file_count="multiple",
                                file_types=[".pdf", ".docx", ".md", ".txt"],
                                elem_classes="file-upload"
                            )
                            
                            file_process_btn = gr.Button("🔍 处理上传的文件", variant="secondary")
                            file_status = gr.Textbox(label="文件处理状态", interactive=False)
                            
                        with gr.Column():
                            style_reference = gr.File(
                                label="样式参考文档（可选）",
                                file_count="single",
                                file_types=[".pdf", ".docx", ".md", ".txt"],
                                info="上传一个您喜欢的简历样式作为参考"
                            )
                    
                    gr.Markdown("### 📝 模板设置")
                    template_content = gr.Textbox(
                        label="简历模板",
                        value=lambda: self.get_default_template(),
                        lines=10,
                        info="您可以修改此模板以自定义简历格式。使用 {{variable}} 语法插入AI生成的内容。"
                    )
                    
                    extracted_content = gr.Textbox(
                        label="提取的文档内容",
                        lines=8,
                        interactive=False,
                        info="这里显示从上传文档中提取的内容，您可以查看但无需编辑"
                    )
                    
                    generate_btn = gr.Button("🚀 生成简历", variant="primary", size="lg")
                    
                    with gr.Row():
                        generation_status = gr.Textbox(label="生成状态", interactive=False)
                    
                    with gr.Row():
                        with gr.Column():
                            markdown_output = gr.File(label="📄 Markdown 简历", interactive=False)
                        with gr.Column():
                            word_output = gr.File(label="📋 Word 文档", interactive=False)
                        with gr.Column():
                            html_output = gr.File(label="🌐 HTML 网站", interactive=False)
                
                # Tab 2: Manage Profiles  
                with gr.Tab("📂 管理档案"):
                    gr.Markdown("### 现有档案")
                    
                    refresh_btn = gr.Button("🔄 刷新档案列表", variant="secondary")
                    profiles_list = gr.Textbox(
                        label="档案列表",
                        value=lambda: self.list_existing_profiles(),
                        lines=10,
                        interactive=False
                    )
                    
                    gr.Markdown("""
                    ### 💡 使用提示
                    
                    1. **文件组织**: 生成的文件保存在 `profiles/` 目录下
                    2. **版本管理**: 每次生成会创建新版本（格式：v202401011200）
                    3. **跨平台**: 支持 Windows 和 macOS
                    4. **文件格式**: 
                       - **Markdown**: 易于编辑和版本控制
                       - **Word**: 可直接打印或邮件发送
                       - **HTML**: 响应式网站，可部署到 GitHub Pages
                    """)
                
                # Tab 3: Configuration
                with gr.Tab("⚙️ 设置"):
                    gr.Markdown("### 系统配置")
                    
                    platform_info = gr.Textbox(
                        label="平台信息",
                        value=lambda: f"系统: {self.platform_info['system']}\n"
                                     f"Windows: {self.platform_info['is_windows']}\n"
                                     f"macOS: {self.platform_info['is_macos']}\n"
                                     f"路径分隔符: {self.platform_info['path_separator']}",
                        interactive=False
                    )
                    
                    gr.Markdown("""
                    ### 📋 环境变量设置
                    
                    为了使用AI功能，您需要设置以下环境变量：
                    
                    ```bash
                    # 必需 - OpenAI API密钥
                    export OPENAI_API_KEY="your-api-key-here"
                    
                    # 可选配置
                    export EASYCV_OUTPUT_DIR="custom_output_directory" 
                    export EASYCV_AI_MODEL="gpt-4"
                    export EASYCV_LOG_LEVEL="INFO"
                    ```
                    
                    ### 🔧 高级功能
                    
                    如需更多控制和批处理功能，请使用命令行界面：
                    
                    ```bash
                    cd v2
                    python main.py generate --help
                    ```
                    """)
            
            # Event handlers
            file_process_btn.click(
                fn=self.process_uploaded_files,
                inputs=[uploaded_files],
                outputs=[file_status, extracted_content]
            )
            
            generate_btn.click(
                fn=self.generate_resume,
                inputs=[
                    profile_name,
                    job_description, 
                    extracted_content,
                    template_content,
                    style_reference,
                    output_formats
                ],
                outputs=[
                    generation_status,
                    markdown_output,
                    word_output, 
                    html_output
                ]
            )
            
            refresh_btn.click(
                fn=self.list_existing_profiles,
                outputs=[profiles_list]
            )
        
        return interface
    
    def launch(self, **kwargs):
        """
        Launch the Gradio application
        
        Args:
            **kwargs: Additional arguments for Gradio launch
        """
        interface = self.create_interface()
        
        # Default launch settings
        launch_args = {
            'server_name': '0.0.0.0',
            'server_port': 7860,
            'share': False,
            'debug': False,
            'show_tips': True,
            **kwargs
        }
        
        print(f"""
🚀 EasyCV Gradio界面启动中...

平台信息:
- 系统: {self.platform_info['system']}
- Windows: {self.platform_info['is_windows']}
- macOS: {self.platform_info['is_macos']}

访问地址: http://localhost:{launch_args['server_port']}
        """)
        
        interface.launch(**launch_args)


def main():
    """Main entry point for the Gradio application"""
    app = EasyCVGradioApp()
    app.launch()


if __name__ == "__main__":
    main() 
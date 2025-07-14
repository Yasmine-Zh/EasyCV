"""
Gradio Web Interface for EasyCV
Provides an easy-to-use web interface for resume generation
"""

import gradio as gr
import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

# Ensure the parent directory is in the Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Import modules with error handling
try:
    from core.document_parser import DocumentParser
    from core.ai_processor import AIProcessor
    from core.template_engine import TemplateEngine
    from core.output_generator import OutputGenerator
    from utils.file_utils import FileUtils
    from utils.version_manager import VersionManager
    from utils.path_utils import (
        normalize_path, safe_join, create_safe_directory, 
        get_valid_filename, get_temp_dir, get_platform_info
    )
    try:
        from config import ConfigManager
    except ImportError:
        # Fallback ConfigManager for testing
        class ConfigManager:
            def __init__(self):
                self.settings = {
                    'output_dir': 'profiles',
                    'template_dir': 'templates',
                    'openai_api_key': None,
                    'ai_model': 'gpt-4',
                    'ai_temperature': 0.3,
                    'keep_versions': 5,
                    'generate_all_formats': True,
                    'default_theme': 'professional',
                    'log_level': 'INFO'
                }
            
            def get(self, key: str, default=None):
                return self.settings.get(key, default)
            
            def set(self, key: str, value):
                self.settings[key] = value
            
            def get_ai_config(self):
                return {
                    'api_key': self.get('openai_api_key'),
                    'model': self.get('ai_model'),
                    'temperature': self.get('ai_temperature')
                }
    CORE_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some core modules not available: {e}")
    print("Running in limited mode - some features may not work.")
    CORE_MODULES_AVAILABLE = False
    
    # Fallback imports for testing
    class DocumentParser:
        def __init__(self, verbose=True):
            self.verbose = verbose  # 添加调试输出控制
        
        def parse_document(self, path):
            return f"测试内容来自: {Path(path).name}"
    
    class AIProcessor:
        def __init__(self, config): 
            pass
        def generate_resume_content(self, **kwargs): 
            return {
                "name": "测试用户",
                "contact": "email: test@example.com\n电话: 123-456-7890",
                "summary": "这是一个测试生成的个人简介。",
                "experience": "测试工作经验内容。",
                "education": "测试教育背景。",
                "skills": "Python, JavaScript, 机器学习",
                "projects": "测试项目经验。"
            }
    
    class TemplateEngine:
        def apply_template(self, template, data): 
            # 简单的模板替换
            result = template
            for key, value in data.items():
                result = result.replace(f"{{{{{key}}}}}", str(value))
            return result
    
    class OutputGenerator:
        def __init__(self, config): 
            pass
        def generate_word(self, content, path): 
            print(f"Word文档已保存到: {path}")
        def generate_website(self, content, dir_path, name): 
            print(f"网站已生成到: {dir_path}")
    
    class FileUtils:
        pass
    
    class VersionManager:
        def generate_version(self): 
            from datetime import datetime
            return datetime.now().strftime('%Y%m%d%H%M')
        def get_timestamp(self): 
            from datetime import datetime
            return datetime.now().strftime('%Y-%m-%d %H:%M')
    
    class ConfigManager:
        def __init__(self):
            self.settings = {
                'output_dir': 'profiles',
                'template_dir': 'templates', 
                'openai_api_key': None,
                'ai_model': 'gpt-4',
                'ai_temperature': 0.3,
                'keep_versions': 5,
                'generate_all_formats': True,
                'default_theme': 'professional',
                'log_level': 'INFO'
            }
        
        def get(self, key: str, default=None):
            return self.settings.get(key, default)
        
        def set(self, key: str, value):
            self.settings[key] = value
        
        def get_ai_config(self):
            return {
                'api_key': self.get('openai_api_key'),
                'model': self.get('ai_model'),
                'temperature': self.get('ai_temperature')
            }
    
    def get_temp_dir(): 
        return Path(tempfile.gettempdir())
    
    def get_platform_info(): 
        import platform
        return {
            "system": platform.system().lower(),
            "is_windows": platform.system() == "Windows",
            "is_macos": platform.system() == "Darwin",
            "path_separator": os.sep
        }
    
    def normalize_path(p): 
        return Path(p).resolve()
    
    def safe_join(*args): 
        return Path(os.path.join(*[str(a) for a in args]))
    
    def create_safe_directory(p): 
        path = Path(p)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def get_valid_filename(name): 
        import re
        # 移除不安全字符
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', name)
        return safe_name.strip(' .')


class EasyCVGradioApp:
    """
    Gradio application for EasyCV resume generation
    """
    
    def __init__(self):
        """Initialize the Gradio application"""
        if not CORE_MODULES_AVAILABLE:
            print("⚠️  Running in limited mode - some features may not work properly")
            print("💡 Please ensure all core modules are available for full functionality")
            
        self.config_manager = ConfigManager()
        self.temp_dir = get_temp_dir() / "easycv_temp"
        create_safe_directory(self.temp_dir)
        
        # Initialize components
        self.document_parser = DocumentParser(verbose=True)
        
        # Initialize AI processor with proper configuration
        try:
            # Try to get API key from config or environment
            api_key = None
            if hasattr(self.config_manager, 'get_ai_config'):
                ai_config = self.config_manager.get_ai_config()
                api_key = ai_config.get('openai_api_key') if ai_config else None
            
            # Fallback to environment variable
            if not api_key:
                import os
                api_key = os.getenv('OPENAI_API_KEY')
            
            if api_key:
                self.ai_processor = AIProcessor(api_key=api_key)
                print("✅ 成功初始化AI处理器（使用OpenAI API）")
            else:
                print("⚠️  未找到OpenAI API密钥，使用测试AI处理器")
                # Use fallback AIProcessor from the import failure section
                raise ImportError("No API key available")
                
        except Exception as e:
            print(f"⚠️  AI处理器初始化失败: {e}")
            print("🔄 使用测试AI处理器...")
            # Use the fallback AIProcessor class defined above
            class TestAIProcessor:
                def __init__(self, config): 
                    pass
                def generate_resume_content(self, **kwargs): 
                    return {
                        "name": "测试用户",
                        "contact": "email: test@example.com\n电话: 123-456-7890",
                        "summary": "这是一个测试生成的个人简介。",
                        "experience": "测试工作经验内容。",
                        "education": "测试教育背景。",
                        "skills": "Python, JavaScript, 机器学习",
                        "projects": "测试项目经验。",
                        "certifications": "相关认证证书",
                        "achievements": "主要成就奖项"
                    }
            self.ai_processor = TestAIProcessor(self.config_manager)
        
        self.template_engine = TemplateEngine()
        self.output_generator = OutputGenerator(self.config_manager.get('output_dir', 'profiles'))
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
            
            # Store file info for later saving
            self.uploaded_files_info = []
            
            for file in files:
                if file is None:
                    continue
                    
                # Get file path
                file_path = Path(file.name)
                
                # Store file information for later saving
                file_info = {
                    'original_path': str(file_path),
                    'name': file_path.name,
                    'size': file_path.stat().st_size if file_path.exists() else 0,
                    'extension': file_path.suffix.lower()
                }
                self.uploaded_files_info.append(file_info)
                
                # Parse document with detailed console output
                print(f"\n🔍 处理上传文件: {file_path.name}")
                content = self.document_parser.parse_document(str(file_path))
                
                if content.strip():
                    all_content.append(f"=== {file_path.name} ===\n{content}\n")
                    processed_files.append(file_path.name)
                    
                    # 在控制台显示提取的完整内容
                    print(f"\n📝 从 {file_path.name} 提取的完整内容:")
                    print("=" * 80)
                    print(content)
                    print("=" * 80)
                    print(f"✅ 文件 {file_path.name} 处理完成\n")
                else:
                    print(f"⚠️  警告: 从 {file_path.name} 未提取到任何内容\n")
                    
            if not all_content:
                return "❌ 无法从上传的文件中提取内容", ""
                
            extracted_text = "\n".join(all_content)
            success_msg = f"✅ 成功处理 {len(processed_files)} 个文件: {', '.join(processed_files)}"
            
            return success_msg, extracted_text
            
        except Exception as e:
            return f"❌ 处理文件时出错: {str(e)}", ""
    
    def show_extracted_content(self, files: List[Any]) -> str:
        """
        显示从上传文件中提取的详细内容
        
        Args:
            files: List of uploaded file objects from Gradio
            
        Returns:
            Detailed extracted content for display
        """
        if not files:
            return "❌ 请先上传文件"
            
        try:
            all_details = []
            
            for file in files:
                if file is None:
                    continue
                    
                file_path = Path(file.name)
                
                # 创建详细解析器（启用调试模式）
                detail_parser = DocumentParser(verbose=False)  # 不在这里输出控制台信息
                
                print(f"\n🔍 详细解析文件: {file_path.name}")
                content = detail_parser.extract_text_from_file(str(file_path))
                
                if content.strip():
                    file_detail = f"""
=== 📄 文件: {file_path.name} ===
📁 路径: {file_path}
📦 大小: {file_path.stat().st_size if file_path.exists() else 0} bytes
🔧 格式: {file_path.suffix.lower()}
📊 字符数: {len(content)}
📄 行数: {len(content.splitlines())}
📋 非空行数: {len([line for line in content.splitlines() if line.strip()])}

📝 完整内容:
{'-' * 80}
{content}
{'-' * 80}

"""
                    all_details.append(file_detail)
                    
                    # 在控制台也显示完整内容
                    print(f"📝 从 {file_path.name} 提取的详细内容:")
                    print("=" * 100)
                    print(content)
                    print("=" * 100)
                    print(f"✅ 文件 {file_path.name} 详细解析完成\n")
                else:
                    file_detail = f"""
=== ⚠️  文件: {file_path.name} ===
❌ 状态: 未能提取到内容
📁 路径: {file_path}
📦 大小: {file_path.stat().st_size if file_path.exists() else 0} bytes
🔧 格式: {file_path.suffix.lower()}

"""
                    all_details.append(file_detail)
                    print(f"⚠️  警告: 从 {file_path.name} 未提取到任何内容")
                    
            if all_details:
                result = "\n".join(all_details)
                print(f"\n🎉 所有文件详细解析完成！共处理 {len(all_details)} 个文件")
                return result
            else:
                return "❌ 未能从任何文件中提取到内容"
                
        except Exception as e:
            error_msg = f"❌ 显示提取内容时出错: {str(e)}"
            print(error_msg)
            return error_msg
    
    def generate_resume(self, 
                       profile_name: str,
                       job_description: str,
                       extracted_content: str,
                       template_content: str,
                       style_reference: Optional[Any] = None,
                       output_formats: List[str] = None,
                       language: str = "english") -> Tuple[str, str, str, str]:
        """
        Generate resume in multiple formats
        
        Args:
            profile_name: Name for the profile
            job_description: Target job description
            extracted_content: Extracted content from uploaded files
            template_content: Resume template content
            style_reference: Optional style reference file
            output_formats: List of desired output formats
            language: Target language for the resume (default: "english")
            
        Returns:
            Tuple of (status_message, markdown_path, word_path, html_path)
        """
        try:
            print(f"\n🚀 开始生成简历...")
            print(f"📝 档案名称: {profile_name}")
            print(f"🎯 目标语言: {language}")
            print(f"📊 输入参数验证:")
            print(f"  - 档案名称: {'✅' if profile_name.strip() else '❌'}")
            print(f"  - 职位描述: {'✅' if job_description.strip() else '❌'}")  
            print(f"  - 提取内容: {'✅' if extracted_content.strip() else '❌'}")
            
            if not profile_name.strip():
                return "❌ 请输入个人档案名称", None, None, None
                
            if not job_description.strip():
                return "❌ 请输入工作描述", None, None, None
                
            if not extracted_content.strip():
                return "❌ 请先上传并处理文档", None, None, None
            
            # Clean profile name
            safe_profile_name = get_valid_filename(profile_name.strip())
            
            # Create version
            version = self.version_manager.generate_version()
            
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
            print(f"🧠 开始AI内容生成...")
            print(f"🔍 提取内容长度: {len(extracted_content)} 字符")
            print(f"🔍 职位描述长度: {len(job_description)} 字符")
            print(f"🔍 目标语言: {language}")
            
            resume_data = self.ai_processor.generate_resume_content(
                experience_docs=extracted_content,
                job_description=job_description,
                style_reference=style_content,
                language=language
            )
            
            print(f"✅ AI生成的简历数据键: {list(resume_data.keys()) if resume_data else 'None'}")
            
            # Apply template
            if template_content.strip():
                try:
                    print(f"📝 应用自定义模板...")
                    final_content = self.template_engine.apply_template(
                        template_content, 
                        resume_data
                    )
                    print(f"✅ 模板应用成功，最终内容长度: {len(final_content)} 字符")
                except Exception as e:
                    print(f"Warning: Template application failed: {e}")
                    print(f"🔄 回退到默认格式...")
                    final_content = self._format_resume_data(resume_data)
            else:
                print(f"📝 使用默认格式（无自定义模板）...")
                final_content = self._format_resume_data(resume_data)
                
            print(f"📄 最终简历内容预览（前200字符）: {final_content[:200]}...")
            
            # Generate outputs
            output_files = {}
            
            if not output_formats:
                output_formats = ['markdown', 'word', 'html']
            
            # 修复格式不匹配问题：将界面格式转换为内部格式
            format_mapping = {
                'Markdown': 'markdown',
                'Word': 'word', 
                'Website': 'html'
            }
            
            # 转换格式并添加调试输出
            normalized_formats = []
            for fmt in output_formats:
                if fmt in format_mapping:
                    normalized_formats.append(format_mapping[fmt])
                else:
                    normalized_formats.append(fmt.lower())
            
            output_formats = normalized_formats
            print(f"🔍 标准化后的输出格式: {output_formats}")
            
            # Generate markdown
            if 'markdown' in output_formats:
                md_path = output_dir / f"{safe_profile_name}.v{version}.md"
                print(f"📄 生成Markdown文件: {md_path}")
                try:
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    print(f"✅ Markdown文件写入成功，文件大小: {md_path.stat().st_size} 字节")
                    output_files['markdown'] = str(md_path)
                except Exception as e:
                    print(f"❌ Markdown文件写入失败: {e}")
            else:
                print(f"⏭️  跳过Markdown生成（不在输出格式中）")
            
            # Generate Word document
            if 'word' in output_formats:
                word_path = output_dir / f"{safe_profile_name}.v{version}.docx"
                print(f"📋 生成Word文档: {word_path}")
                try:
                    self.output_generator.generate_word(final_content, str(word_path))
                    if word_path.exists():
                        print(f"✅ Word文档生成成功，文件大小: {word_path.stat().st_size} 字节")
                        output_files['word'] = str(word_path)
                    else:
                        print(f"❌ Word文档生成失败：文件不存在")
                except Exception as e:
                    print(f"❌ Word generation failed: {e}")
                    # 不设置word键，这样get()会返回默认值
            else:
                print(f"⏭️  跳过Word生成（不在输出格式中）")
            
            # Generate HTML website
            if 'html' in output_formats:
                html_path = output_dir / f"{safe_profile_name}.v{version}.html"
                print(f"🌐 生成HTML网站: {html_path}")
                try:
                    self.output_generator.generate_website(
                        final_content, 
                        str(output_dir),
                        f"{safe_profile_name}.v{version}"
                    )
                    if html_path.exists():
                        print(f"✅ HTML网站生成成功，文件大小: {html_path.stat().st_size} 字节")
                        output_files['html'] = str(html_path)
                    else:
                        print(f"❌ HTML网站生成失败：文件不存在")
                except Exception as e:
                    print(f"❌ HTML generation failed: {e}")
                    # 不设置html键，这样get()会返回默认值
            else:
                print(f"⏭️  跳过HTML生成（不在输出格式中）")
            
            # Save original documents if available
            source_docs_info = []
            if hasattr(self, 'uploaded_files_info') and self.uploaded_files_info:
                source_docs_dir = output_dir / "source_documents"
                create_safe_directory(source_docs_dir)
                
                for file_info in self.uploaded_files_info:
                    original_path = Path(file_info['original_path'])
                    if original_path.exists():
                        # Copy original file to source_documents directory
                        saved_filename = f"{safe_profile_name}_source_{file_info['name']}"
                        saved_path = source_docs_dir / saved_filename
                        
                        try:
                            import shutil
                            shutil.copy2(str(original_path), str(saved_path))
                            
                            # Update file info with saved location
                            file_info['saved_path'] = str(saved_path.relative_to(output_dir))
                            file_info['saved_at'] = self.version_manager.get_timestamp()
                            source_docs_info.append(file_info)
                            
                        except Exception as e:
                            print(f"Warning: Could not save source document {file_info['name']}: {e}")
            
            # Save metadata
            metadata = {
                'profile_name': safe_profile_name,
                'version': version,
                'timestamp': self.version_manager.get_timestamp(),
                'job_description': job_description,
                'output_formats': output_formats,
                'platform': self.platform_info,
                'files_generated': output_files,
                'source_documents': source_docs_info,  # 新增：源文档信息
                'total_source_files': len(source_docs_info)  # 新增：源文件数量
            }
            
            metadata_path = output_dir / "metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 生成的文件汇总:")
            for format_name, file_path in output_files.items():
                if file_path and Path(file_path).exists():
                    print(f"  ✅ {format_name}: {file_path}")
                else:
                    print(f"  ❌ {format_name}: 未生成")
            
            success_msg = f"✅ 简历生成成功！\n档案: {safe_profile_name}\n版本: v{version}\n输出目录: {output_dir}"
            
            # 确保文件路径存在，不存在则返回None而不是空字符串
            markdown_path = output_files.get('markdown', '')
            word_path = output_files.get('word', '')
            html_path = output_files.get('html', '')
            
            # 验证文件是否真实存在，如果不存在则返回None
            if markdown_path and not Path(markdown_path).exists():
                markdown_path = None
            elif not markdown_path:
                markdown_path = None
                
            if word_path and not Path(word_path).exists():
                word_path = None
            elif not word_path:
                word_path = None
                
            if html_path and not Path(html_path).exists():
                html_path = None
            elif not html_path:
                html_path = None
            
            return (
                success_msg,
                markdown_path,
                word_path,
                html_path
            )
            
        except Exception as e:
            return f"❌ 生成简历时出错: {str(e)}", None, None, None
    
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
            
            if not CORE_MODULES_AVAILABLE:
                gr.Markdown("""
                ⚠️ **警告**: 部分核心模块未正确加载，某些功能可能无法正常工作。
                💡 请确保所有依赖已正确安装并检查环境设置。
                """)
            
            with gr.Tabs():
                # Tab 1: Generate New Resume
                with gr.Tab("🆕 生成新简历"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            gr.Markdown("### 📋 基本信息")
                            profile_name = gr.Textbox(
                                label="个人档案名称（用于文件命名和组织）",
                                placeholder="例如: 张三_软件工程师"
                            )
                            
                            job_description = gr.Textbox(
                                label="目标职位描述（AI将根据此描述优化您的简历内容）",
                                placeholder="粘贴完整的工作描述，或简要描述目标职位要求...",
                                lines=5
                            )
                            
                        with gr.Column(scale=1):
                            gr.Markdown("### ⚙️ 生成选项")
                            
                            language_choice = gr.Radio(
                                choices=["English", "Chinese", "Bilingual"],
                                value="English",
                                label="简历语言 / Resume Language"
                            )
                            
                            output_formats = gr.CheckboxGroup(
                                choices=["Markdown", "Word", "Website"],
                                value=["Markdown", "Word"],
                                label="输出格式（选择需要生成的文件格式）"
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
                            
                            with gr.Row():
                                file_process_btn = gr.Button("🔍 处理上传的文件", variant="secondary")
                                show_content_btn = gr.Button("📄 显示提取内容", variant="primary")
                            
                            file_status = gr.Textbox(label="文件处理状态", interactive=False)
                            
                        with gr.Column():
                            style_reference = gr.File(
                                label="样式参考文档（可选）",
                                file_count="single",
                                file_types=[".pdf", ".docx", ".md", ".txt"]
                            )
                    
                    gr.Markdown("### 📝 模板设置")
                    template_content = gr.Textbox(
                        label="简历模板（可修改格式，使用 {{variable}} 语法插入AI生成的内容）",
                        lines=15,
                        value=self.get_default_template()
                    )
                    
                    extracted_content = gr.Textbox(
                        label="提取的文档内容（显示从上传文档中提取的内容）",
                        lines=10,
                        interactive=False
                    )
                    
                    # 详细内容显示区域
                    with gr.Accordion("📄 详细提取内容", open=False):
                        detailed_content = gr.Textbox(
                            label="完整提取内容（包含详细格式信息）",
                            lines=20,
                            interactive=False,
                            max_lines=30
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
                    
                    gr.Markdown(f"""
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
                    
                    ### 🔧 Python版本信息
                    
                    - Python版本: {sys.version}
                    - 核心模块加载: {'✅ 正常' if CORE_MODULES_AVAILABLE else '❌ 部分失败'}
                    
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
            
            show_content_btn.click(
                fn=self.show_extracted_content,
                inputs=[uploaded_files],
                outputs=[detailed_content]
            )
            
            generate_btn.click(
                fn=self.generate_resume_with_language,
                inputs=[
                    profile_name,
                    job_description, 
                    extracted_content,
                    template_content,
                    style_reference,
                    output_formats,
                    language_choice
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
            'server_port': None,  # 让Gradio自动选择可用端口
            'share': False,
            'debug': False,
            **kwargs
        }
        
        print(f"""
🚀 EasyCV Gradio界面启动中...

平台信息:
- 系统: {self.platform_info['system']}
- Windows: {self.platform_info['is_windows']}
- macOS: {self.platform_info['is_macos']}
- Python版本: {sys.version.split()[0]}
- 核心模块: {'✅ 正常' if CORE_MODULES_AVAILABLE else '⚠️  部分缺失'}

🔍 正在自动寻找可用端口...
        """)
        
        interface.launch(**launch_args)

    def convert_language_choice(self, choice: str) -> str:
        """Convert UI language choice to internal language code"""
        mapping = {
            "English": "english",
            "Chinese": "chinese", 
            "Bilingual": "bilingual"
        }
        return mapping.get(choice, "english")
    
    def generate_resume_with_language(self, profile_name: str, job_description: str, 
                                     extracted_content: str, template_content: str,
                                     style_reference: Optional[Any], output_formats: List[str],
                                     language_choice: str) -> Tuple[str, str, str, str]:
        """Wrapper for generate_resume that handles language conversion"""
        language = self.convert_language_choice(language_choice)
        return self.generate_resume(
            profile_name=profile_name,
            job_description=job_description,
            extracted_content=extracted_content,
            template_content=template_content,
            style_reference=style_reference,
            output_formats=output_formats,
            language=language
        )


def main():
    """Main entry point for the Gradio application"""
    try:
        app = EasyCVGradioApp()
        app.launch()
    except ImportError as e:
        print(f"\n❌ 模块导入错误: {e}")
        print("\n💡 解决方案:")
        print("1. 确保在v2目录下运行: cd v2")
        print("2. 安装所有依赖: pip install -r requirements.txt")
        print("3. 检查所有核心模块是否存在")
        print("4. 使用: python3 launch_ui.py")
        
        # 提供调试信息
        current_dir = Path(__file__).parent.parent
        print(f"\n🔍 当前目录: {current_dir}")
        print(f"🔍 Python路径: {sys.path[:3]}...")
        
        # 检查核心目录
        core_dir = current_dir / "core"
        utils_dir = current_dir / "utils"
        print(f"🔍 core目录存在: {core_dir.exists()}")
        print(f"🔍 utils目录存在: {utils_dir.exists()}")
        
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 
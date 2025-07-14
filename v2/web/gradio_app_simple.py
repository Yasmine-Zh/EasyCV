"""
简化的Gradio Web界面 - 确保Python 3.8兼容性
"""

import gradio as gr
import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
import platform

# 简化的工具函数
def get_platform_info():
    return {
        "system": platform.system().lower(),
        "is_windows": platform.system() == "Windows",
        "is_macos": platform.system() == "Darwin", 
        "path_separator": os.sep
    }

def get_valid_filename(name):
    import re
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return safe_name.strip(' .')

def create_safe_directory(path):
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj

class EasyCVSimpleApp:
    """
    简化的Gradio应用程序
    """
    
    def __init__(self):
        """初始化应用程序"""
        self.platform_info = get_platform_info()
        self.temp_dir = Path(tempfile.gettempdir()) / "easycv_temp"
        create_safe_directory(self.temp_dir)
        
    def process_uploaded_files(self, files):
        """处理上传的文件"""
        if not files:
            return "❌ 请至少上传一个文件", ""
            
        try:
            all_content = []
            processed_files = []
            
            if isinstance(files, list):
                file_list = files
            else:
                file_list = [files]
                
            for file in file_list:
                if file is None:
                    continue
                    
                file_path = Path(file.name)
                # 简单的文件内容读取
                try:
                    if file_path.suffix.lower() == '.txt':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    else:
                        content = f"文件类型: {file_path.suffix}\n文件名: {file_path.name}\n大小: {file_path.stat().st_size} bytes"
                    
                    if content.strip():
                        all_content.append(f"=== {file_path.name} ===\n{content}\n")
                        processed_files.append(file_path.name)
                        
                except Exception as e:
                    all_content.append(f"=== {file_path.name} ===\n无法读取文件: {str(e)}\n")
                    processed_files.append(file_path.name)
                    
            if not all_content:
                return "❌ 无法从上传的文件中提取内容", ""
                
            extracted_text = "\n".join(all_content)
            success_msg = f"✅ 成功处理 {len(processed_files)} 个文件: {', '.join(processed_files)}"
            
            return success_msg, extracted_text
            
        except Exception as e:
            return f"❌ 处理文件时出错: {str(e)}", ""
    
    def generate_resume(self, profile_name, job_description, extracted_content, template_content, language="English"):
        """生成简历"""
        try:
            if not profile_name.strip():
                return "❌ 请输入个人档案名称", "", "", ""
                
            if not job_description.strip():
                return "❌ 请输入工作描述", "", "", ""
                
            if not extracted_content.strip():
                return "❌ 请先上传并处理文档", "", "", ""
            
            # 清理档案名
            safe_profile_name = get_valid_filename(profile_name.strip())
            
            # 创建版本号
            version = datetime.now().strftime('%Y%m%d%H%M')
            
            # 创建输出目录
            output_dir = create_safe_directory(
                Path("profiles") / safe_profile_name / f"v{version}"
            )
            
            # 根据语言选择生成不同内容
            if language == "English":
                resume_content = f"""# {safe_profile_name}'s Resume

## Personal Information
Profile Name: {profile_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Target Position
{job_description}

## Extracted Experience
{extracted_content}

## Template Content
{template_content if template_content else 'No template provided'}

---
*This resume was generated using EasyCV - AI Resume Generator*
"""
            elif language == "Chinese":
                resume_content = f"""# {safe_profile_name}的简历

## 个人信息
档案名称: {profile_name}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 目标职位
{job_description}

## 提取的经验
{extracted_content}

## 模板内容
{template_content if template_content else '未提供模板'}

---
*此简历由 EasyCV - AI简历生成器 生成*
"""
            else:  # Bilingual
                resume_content = f"""# {safe_profile_name}'s Resume / {safe_profile_name}的简历

## Personal Information / 个人信息
Profile Name / 档案名称: {profile_name}
Generated / 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Target Position / 目标职位
{job_description}

## Extracted Experience / 提取的经验
{extracted_content}

## Template Content / 模板内容
{template_content if template_content else 'No template provided / 未提供模板'}

---
*This resume was generated using EasyCV - AI Resume Generator*
*此简历由 EasyCV - AI简历生成器 生成*
"""
            
            # 保存Markdown文件
            md_path = output_dir / f"{safe_profile_name}.v{version}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(resume_content)
            
            # 保存元数据
            metadata = {
                'profile_name': safe_profile_name,
                'version': version,
                'timestamp': datetime.now().isoformat(),
                'job_description': job_description,
                'platform': self.platform_info
            }
            
            metadata_path = output_dir / "metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            success_msg = f"✅ 简历生成成功！\n档案: {safe_profile_name}\nv{version}\n输出目录: {output_dir}"
            
            return success_msg, str(md_path), "", ""
            
        except Exception as e:
            return f"❌ 生成简历时出错: {str(e)}", "", "", ""
    
    def list_existing_profiles(self):
        """列出现有档案"""
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
                        versions.sort(reverse=True)
                        profiles.append(f"📋 {profile_dir.name}: {', '.join(versions[:3])}")
            
            if not profiles:
                return "📁 暂无现有档案"
            
            return "📁 现有档案:\n\n" + "\n".join(profiles)
            
        except Exception as e:
            return f"❌ 获取档案列表时出错: {str(e)}"
    
    def get_default_template(self):
        """获取默认模板"""
        return """# 个人简历

## 基本信息
姓名: [请填写]
联系方式: [请填写]

## 个人简介
[请根据职位要求填写个人简介]

## 工作经验
[请填写工作经验]

## 教育背景
[请填写教育背景]

## 技能特长
[请填写技能特长]

## 项目经验
[请填写项目经验]
"""
    
    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(
            title="EasyCV - AI简历生成器",
            theme=gr.themes.Soft()
        ) as interface:
            
            gr.Markdown("""
            # 🚀 EasyCV - AI简历生成器 (简化版)
            
            这是一个智能简历生成工具，支持：
            - 📄 上传文档资料
            - 🎯 根据职位描述生成内容
            - 📝 生成Markdown格式简历
            
            **当前版本**: 简化版（确保最大兼容性）
            """)
            
            with gr.Tabs():
                # 生成新简历
                with gr.Tab("🆕 生成新简历"):
                    with gr.Row():
                        with gr.Column():
                            profile_name = gr.Textbox(
                                label="个人档案名称",
                                placeholder="例如: 张三_软件工程师"
                            )
                            
                            job_description = gr.Textbox(
                                label="目标职位描述",
                                placeholder="粘贴工作描述或简要描述目标职位要求...",
                                lines=5
                            )
                            
                            language_choice = gr.Radio(
                                choices=["English", "Chinese", "Bilingual"],
                                value="English",
                                label="简历语言 / Resume Language"
                            )
                    
                    with gr.Row():
                        with gr.Column():
                            uploaded_files = gr.File(
                                label="上传文档",
                                file_count="multiple",
                                file_types=[".txt", ".md"]
                            )
                            
                            file_process_btn = gr.Button("🔍 处理上传的文件", variant="secondary")
                            file_status = gr.Textbox(label="文件处理状态", interactive=False)
                    
                    template_content = gr.Textbox(
                        label="简历模板",
                        value=self.get_default_template(),
                        lines=10
                    )
                    
                    extracted_content = gr.Textbox(
                        label="提取的文档内容",
                        lines=8,
                        interactive=False
                    )
                    
                    generate_btn = gr.Button("🚀 生成简历", variant="primary", size="lg")
                    
                    generation_status = gr.Textbox(label="生成状态", interactive=False)
                    
                    with gr.Row():
                        markdown_output = gr.File(label="📄 Markdown 简历", interactive=False)
                
                # 管理档案
                with gr.Tab("📂 管理档案"):
                    refresh_btn = gr.Button("🔄 刷新档案列表", variant="secondary")
                    profiles_list = gr.Textbox(
                        label="档案列表",
                        value=self.list_existing_profiles(),
                        lines=10,
                        interactive=False
                    )
                
                # 系统信息
                with gr.Tab("⚙️ 系统信息"):
                    platform_info = gr.Textbox(
                        label="平台信息",
                        value=f"系统: {self.platform_info['system']}\n"
                              f"Python版本: {sys.version.split()[0]}\n"
                              f"路径分隔符: {self.platform_info['path_separator']}",
                        interactive=False
                    )
                    
                    gr.Markdown("""
                    ### 使用说明
                    
                    1. **简化版本**: 当前为简化版本，确保在各种Python环境下的兼容性
                    2. **支持格式**: 目前主要支持TXT和Markdown文件
                    3. **输出格式**: 生成Markdown格式的简历文件
                    4. **存储位置**: 文件保存在 `profiles/` 目录下
                    """)
            
            # 事件处理
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
                    language_choice
                ],
                outputs=[
                    generation_status,
                    markdown_output
                ]
            )
            
            refresh_btn.click(
                fn=self.list_existing_profiles,
                outputs=[profiles_list]
            )
        
        return interface
    
    def launch(self, **kwargs):
        """启动应用程序"""
        interface = self.create_interface()
        
        launch_args = {
            'server_name': '0.0.0.0',
            'server_port': 7860,
            'share': False,
            'debug': False,
            **kwargs
        }
        
        print(f"""
🚀 EasyCV 简化版启动中...

平台信息:
- 系统: {self.platform_info['system']}
- Python版本: {sys.version.split()[0]}
- 界面版本: 简化版（兼容性优先）

访问地址: http://localhost:{launch_args['server_port']}
        """)
        
        interface.launch(**launch_args)


def main():
    """主函数"""
    try:
        app = EasyCVSimpleApp()
        app.launch(inbrowser=True)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 
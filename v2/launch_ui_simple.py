#!/usr/bin/env python3
"""
EasyCV 简化版启动器 - 确保Python 3.8兼容性
"""

import gradio as gr
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime

def process_files(files):
    """简单的文件处理"""
    if not files:
        return "❌ 请上传文件", ""
    
    content_list = []
    for file in files:
        if file is None:
            continue
        try:
            file_path = Path(file.name)
            if file_path.suffix.lower() in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                content_list.append(f"=== {file_path.name} ===\n{content}")
            else:
                content_list.append(f"=== {file_path.name} ===\n文件类型: {file_path.suffix}")
        except Exception as e:
            content_list.append(f"=== 文件错误 ===\n{str(e)}")
    
    if content_list:
        return f"✅ 处理了 {len(content_list)} 个文件", "\n\n".join(content_list)
    else:
        return "❌ 无法处理文件", ""

def generate_resume(name, job_desc, content, template):
    """生成简历"""
    if not name or not job_desc or not content:
        return "❌ 请填写所有必要信息", None
    
    try:
        # 创建安全的文件名
        safe_name = "".join(c for c in name if c.isalnum() or c in "._- ")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 创建输出目录
        output_dir = Path("profiles") / safe_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成简历内容
        resume_content = f"""# {name} 的简历

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 目标职位
{job_desc}

## 个人信息提取
{content}

## 模板应用
{template if template else '使用默认格式'}

---
由 EasyCV 自动生成
"""
        
        # 保存文件
        filename = f"{safe_name}_{timestamp}.md"
        file_path = output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(resume_content)
        
        return f"✅ 简历已生成: {file_path}", str(file_path)
        
    except Exception as e:
        return f"❌ 生成失败: {str(e)}", None

def list_profiles():
    """列出现有档案"""
    profiles_dir = Path("profiles")
    if not profiles_dir.exists():
        return "📁 暂无档案"
    
    profiles = []
    for item in profiles_dir.iterdir():
        if item.is_dir():
            files = list(item.glob("*.md"))
            if files:
                profiles.append(f"📋 {item.name}: {len(files)} 个文件")
    
    return "\n".join(profiles) if profiles else "📁 暂无档案"

# 创建Gradio界面
def create_app():
    with gr.Blocks(title="EasyCV 简历生成器") as app:
        gr.Markdown("# 🚀 EasyCV 简历生成器（兼容版）")
        
        with gr.Tab("生成简历"):
            name_input = gr.Textbox(label="姓名", placeholder="请输入您的姓名")
            job_input = gr.Textbox(label="目标职位", placeholder="请描述目标职位", lines=3)
            
            file_input = gr.File(label="上传文档", file_count="multiple")
            process_btn = gr.Button("处理文档")
            
            file_status = gr.Textbox(label="处理状态", interactive=False)
            content_output = gr.Textbox(label="提取内容", lines=6, interactive=False)
            
            template_input = gr.Textbox(
                label="模板（可选）", 
                lines=4,
                value="## 个人简介\n[从上传文档中提取]\n\n## 工作经验\n[详细工作经历]\n\n## 技能特长\n[技能列表]"
            )
            
            generate_btn = gr.Button("🚀 生成简历", variant="primary")
            
            result_status = gr.Textbox(label="生成状态", interactive=False)
            result_file = gr.File(label="下载简历")
        
        with gr.Tab("管理档案"):
            refresh_btn = gr.Button("刷新列表")
            profiles_list = gr.Textbox(label="现有档案", lines=8, interactive=False)
        
        with gr.Tab("系统信息"):
            gr.Textbox(
                label="系统信息",
                value=f"Python版本: {sys.version.split()[0]}\n工作目录: {Path.cwd()}",
                interactive=False
            )
        
        # 绑定事件
        process_btn.click(
            process_files,
            inputs=[file_input],
            outputs=[file_status, content_output]
        )
        
        generate_btn.click(
            generate_resume,
            inputs=[name_input, job_input, content_output, template_input],
            outputs=[result_status, result_file]
        )
        
        refresh_btn.click(
            list_profiles,
            outputs=[profiles_list]
        )
    
    return app

def main():
    """主函数"""
    print("🚀 启动 EasyCV 简化版...")
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"工作目录: {Path.cwd()}")
    
    try:
        app = create_app()
        app.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=True,  # 启用共享链接
            inbrowser=True,
            show_error=True
        )
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        # 尝试备用方案
        try:
            print("🔄 尝试备用配置...")
            app = create_app()
            app.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=True,
                inbrowser=False,
                show_error=True
            )
        except Exception as e2:
            print(f"❌ 备用方案也失败: {e2}")
            print("\n💡 手动启动建议:")
            print("1. 尝试安装较旧版本的Gradio: pip install gradio==3.50.0")
            print("2. 或者使用命令行版本: python main.py generate --help")

if __name__ == "__main__":
    main() 
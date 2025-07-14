#!/usr/bin/env python3
"""
EasyCV Gradio UI Launcher
Simple script to launch the web interface
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Launch the Gradio interface"""
    try:
        from web.gradio_app import EasyCVGradioApp
        
        print("🚀 正在启动 EasyCV Web 界面...")
        print("📝 请确保已设置 OPENAI_API_KEY 环境变量")
        print("🌐 界面将在浏览器中自动打开")
        print("⏹️  按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        app = EasyCVGradioApp()
        app.launch(
            share=False,
            debug=False,
            show_tips=True,
            inbrowser=True  # Automatically open in browser
        )
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请先安装依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
EasyCV Gradio UI Launcher
Simple script to launch the web interface
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the Gradio interface"""
    # 确保在正确的目录中运行
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    # 添加当前目录到Python路径
    sys.path.insert(0, str(current_dir))
    
    print("🚀 正在启动 EasyCV Web 界面...")
    print(f"📁 当前工作目录: {current_dir}")
    print("📝 请确保已设置 OPENAI_API_KEY 环境变量")
    print("💾 正在检查依赖...")
    
    # 检查基本依赖
    try:
        import gradio
        print("✅ Gradio 已安装")
    except ImportError:
        print("❌ Gradio 未安装")
        print("💡 请运行: pip install gradio>=4.0.0")
        sys.exit(1)
    
    # 检查核心目录
    core_dir = current_dir / "core"
    utils_dir = current_dir / "utils"
    web_dir = current_dir / "web"
    
    if not core_dir.exists():
        print(f"❌ 核心目录不存在: {core_dir}")
        sys.exit(1)
    
    if not utils_dir.exists():
        print(f"❌ 工具目录不存在: {utils_dir}")
        sys.exit(1)
        
    if not web_dir.exists():
        print(f"❌ Web目录不存在: {web_dir}")
        sys.exit(1)
    
    print("✅ 目录结构检查通过")
    
    try:
        # 尝试导入Gradio应用
        from web.gradio_app import EasyCVGradioApp
        
        print("🌐 界面将在浏览器中自动打开")
        print("⏹️  按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        app = EasyCVGradioApp()
        app.launch(
            share=False,
            debug=False,
            inbrowser=True  # Automatically open in browser
        )
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("\n💡 解决方案:")
        print("1. 确保在v2目录下运行: cd v2")
        print("2. 安装所有依赖: pip install -r requirements.txt")
        print("3. 检查环境变量: export OPENAI_API_KEY='your-key'")
        
        # 提供更多调试信息
        print(f"\n🔍 调试信息:")
        print(f"- 当前目录: {current_dir}")
        print(f"- Python版本: {sys.version}")
        print(f"- Python路径包含当前目录: {str(current_dir) in sys.path}")
        
        # 检查具体缺失的模块
        missing_modules = []
        for module_name in ['core', 'utils', 'config']:
            try:
                __import__(module_name)
            except ImportError:
                missing_modules.append(module_name)
        
        if missing_modules:
            print(f"- 缺失模块: {', '.join(missing_modules)}")
        
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        print("\n🔍 详细错误信息:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 
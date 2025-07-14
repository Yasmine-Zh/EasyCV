#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyCV 超级简化版本启动器
专为解决兼容性问题设计
"""

import os
import sys
import argparse
import webbrowser
import traceback
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="启动 EasyCV 超级简化版")
    parser.add_argument('--server-port', type=int, default=7860, help='服务器端口')
    parser.add_argument('--share', action='store_true', help='创建公共分享链接')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    print("🚀 启动 EasyCV 超级简化版...")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    print("⚠️  这是超级简化版本，功能有限但兼容性最好")
    
    try:
        # 导入并启动应用
        from web.gradio_app_minimal import EasyCVMinimalApp
        
        app = EasyCVMinimalApp()
        
        launch_kwargs = {
            'server_port': args.server_port,
            'share': args.share,
            'debug': args.debug
        }
        
        app.launch(**launch_kwargs)
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保所有依赖都已安装: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print(f"🔍 详细错误信息:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 
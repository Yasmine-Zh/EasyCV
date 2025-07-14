#!/usr/bin/env python3
"""
EasyCV launcher script
Handles module imports and provides a clean entry point
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run main function
if __name__ == "__main__":
    try:
        from main import main
        main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 
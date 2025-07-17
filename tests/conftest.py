"""
Pytest configuration file to handle imports and path setup
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Set up environment for tests
os.environ.setdefault("PYTHONPATH", str(src_path))

#!/usr/bin/env python3
"""
Convenience script to run backup functionality.
This script allows running backup.py from the root directory.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run backup functionality
from backup import *

if __name__ == "__main__":
    print("Running backup functionality...")
    # Add your backup execution code here 
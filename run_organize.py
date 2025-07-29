#!/usr/bin/env python3
"""
Main script to run the photo organization workflow.
This script orchestrates backup, duplicate detection, and tagging.
"""

import sys
import os

# Add src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the organize module
from organize import main

if __name__ == "__main__":
    print("🚀 Photo Organizer App Starting...")
    print("=" * 50)
    
    try:
        main()
        print("\n✅ Photo organization completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during photo organization: {e}")
        sys.exit(1) 
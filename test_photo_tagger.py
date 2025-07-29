#!/usr/bin/env python3
"""
Test script for the photo tagger functionality.
This script demonstrates how to use the image classification features.
"""

import os
import sys
from PIL import Image
import numpy as np

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from photo_tagger import tag_photo, tag_photo_with_confidence

def create_test_image():
    """
    Create a simple test image for demonstration purposes.
    """
    # Create a simple test image (red square)
    img = Image.new('RGB', (224, 224), color='red')
    test_path = 'test_image.jpg'
    img.save(test_path)
    return test_path

def test_photo_tagger():
    """
    Test the photo tagger functionality.
    """
    print("Testing Photo Tagger with Image Classification")
    print("=" * 50)
    
    # Create a test image
    test_image_path = create_test_image()
    
    try:
        print(f"Testing with image: {test_image_path}")
        
        # Test basic tagging
        print("\n1. Basic tagging:")
        tags = tag_photo(test_image_path)
        print(f"   Tags: {tags}")
        
        # Test tagging with confidence
        print("\n2. Tagging with confidence scores:")
        tags_with_conf = tag_photo_with_confidence(test_image_path)
        for tag, confidence in tags_with_conf[:5]:  # Show top 5
            print(f"   {tag}: {confidence:.3f}")
        
        # Test with PIL Image object
        print("\n3. Testing with PIL Image object:")
        img = Image.open(test_image_path)
        tags_pil = tag_photo(img)
        print(f"   Tags: {tags_pil}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements.txt")
    
    finally:
        # Clean up test image
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"\nCleaned up test image: {test_image_path}")

if __name__ == "__main__":
    test_photo_tagger() 
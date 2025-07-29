"""
Photo Organizer App - Source Package

This package contains the core functionality for photo organization:
- backup: Photo backup functionality
- duplicate_check: Duplicate photo detection
- photo_tagger: Image classification and tagging
- photo_ui: User interface components
- organize: Main organization workflow
"""

__version__ = "1.0.0"
__author__ = "Photo Organizer Team"

# Import main functions for easy access
from .backup import auto_backup_photos
from .duplicate_check import find_duplicate_photos, find_duplicate_photos_fast
from .photo_tagger import tag_photo, tag_photo_with_confidence

__all__ = [
    'auto_backup_photos',
    'find_duplicate_photos',
    'find_duplicate_photos_fast', 
    'tag_photo',
    'tag_photo_with_confidence'
] 
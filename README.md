# photo-organizer-app
# 사진 정리 앱 (Photo Organizer App)

이 앱은 사진을 자동으로 정리하고, 흐릿한 사진, 중복된 이미지를 감지하며, 스마트 태그로 분류하고 클라우드에 백업할 수 있도록 도와줍니다.

## Features

- **Image Classification**: Uses ResNet50 pre-trained model to automatically generate tags for photos
- **Duplicate Detection**: Find and manage duplicate photos
- **Backup System**: Cloud backup functionality
- **Smart Tagging**: AI-powered photo tagging system

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Image Classification and Tagging

The `photo_tagger.py` module provides intelligent image classification using a pre-trained ResNet50 model:

```python
from src.photo_tagger import tag_photo, tag_photo_with_confidence

# Basic tagging
tags = tag_photo("path/to/photo.jpg")
print(tags)  # ['dog', 'outdoor', 'sunny']

# Tagging with confidence scores
tags_with_conf = tag_photo_with_confidence("path/to/photo.jpg")
for tag, confidence in tags_with_conf:
    print(f"{tag}: {confidence:.3f}")
```

### Testing

Run the test script to see the image classification in action:

```bash
python test_photo_tagger.py
```

## Dependencies

- `tensorflow>=2.10.0`: Deep learning framework for image classification
- `Pillow>=9.0.0`: Image processing library
- `numpy>=1.21.0`: Numerical computing library

## Architecture

The image classification system uses:
- **ResNet50**: Pre-trained convolutional neural network
- **ImageNet**: Large-scale dataset for training
- **Confidence Thresholding**: Filters out low-confidence predictions
- **Model Caching**: Loads the model once and reuses it for efficiency

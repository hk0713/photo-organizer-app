import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the model (load once, reuse)
_model = None

def load_model():
    """
    Load the pre-trained ResNet50 model for image classification.
    Returns the model instance.
    """
    global _model
    if _model is None:
        try:
            logger.info("Loading ResNet50 model...")
            _model = ResNet50(weights='imagenet')
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    return _model

def preprocess_image(img_path, target_size=(224, 224)):
    """
    Preprocess an image for the ResNet50 model.
    
    Args:
        img_path: Path to the image file
        target_size: Target size for the image (width, height)
    
    Returns:
        Preprocessed image array
    """
    try:
        # Load and resize image
        img = Image.open(img_path)
        img = img.convert('RGB')  # Ensure RGB format
        img = img.resize(target_size)
        
        # Convert to array and preprocess
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image {img_path}: {e}")
        raise

def get_confidence_threshold():
    """
    Get the confidence threshold for tag generation.
    Tags with confidence below this threshold will be filtered out.
    """
    return 0.1  # 10% confidence threshold

def tag_photo(photo):
    """
    사진을 분석하여 적절한 태그 리스트를 반환합니다.
    
    Args:
        photo: Path to the photo file or PIL Image object
    
    Returns:
        List of tags (strings) for the photo
    """
    try:
        # Load the model
        model = load_model()
        
        # Handle different input types
        if isinstance(photo, str):
            # photo is a file path
            if not os.path.exists(photo):
                logger.error(f"Photo file not found: {photo}")
                return []
            img_array = preprocess_image(photo)
        elif hasattr(photo, 'save'):  # PIL Image object
            # Convert PIL Image to array
            img = photo.convert('RGB')
            img = img.resize((224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
        else:
            logger.error(f"Unsupported photo type: {type(photo)}")
            return []
        
        # Make prediction
        predictions = model.predict(img_array)
        
        # Decode predictions
        decoded_predictions = decode_predictions(predictions, top=10)[0]
        
        # Extract tags with confidence above threshold
        confidence_threshold = get_confidence_threshold()
        tags = []
        
        for _, label, confidence in decoded_predictions:
            if confidence > confidence_threshold:
                # Clean up the label (remove underscores, make lowercase)
                clean_label = label.replace('_', ' ').lower()
                tags.append(clean_label)
        
        # If no tags meet the threshold, return the top 3 tags
        if not tags and decoded_predictions:
            tags = [label.replace('_', ' ').lower() for _, label, _ in decoded_predictions[:3]]
        
        logger.info(f"Generated tags: {tags}")
        return tags
        
    except Exception as e:
        logger.error(f"Error tagging photo: {e}")
        return []

def tag_photo_with_confidence(photo):
    """
    Enhanced version that returns tags with confidence scores.
    
    Args:
        photo: Path to the photo file or PIL Image object
    
    Returns:
        List of tuples (tag, confidence) for the photo
    """
    try:
        model = load_model()
        
        # Handle different input types
        if isinstance(photo, str):
            if not os.path.exists(photo):
                logger.error(f"Photo file not found: {photo}")
                return []
            img_array = preprocess_image(photo)
        elif hasattr(photo, 'save'):
            img = photo.convert('RGB')
            img = img.resize((224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
        else:
            logger.error(f"Unsupported photo type: {type(photo)}")
            return []
        
        # Make prediction
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=10)[0]
        
        # Return tags with confidence scores
        tags_with_confidence = []
        for _, label, confidence in decoded_predictions:
            clean_label = label.replace('_', ' ').lower()
            tags_with_confidence.append((clean_label, float(confidence)))
        
        return tags_with_confidence
        
    except Exception as e:
        logger.error(f"Error tagging photo with confidence: {e}")
        return []

# Example usage and testing
if __name__ == "__main__":
    # Test with a sample image path
    test_image_path = "sample_image.jpg"
    if os.path.exists(test_image_path):
        tags = tag_photo(test_image_path)
        print(f"Generated tags: {tags}")
        
        tags_with_conf = tag_photo_with_confidence(test_image_path)
        print(f"Tags with confidence: {tags_with_conf}")
    else:
        print("Test image not found. Please provide a valid image path for testing.")

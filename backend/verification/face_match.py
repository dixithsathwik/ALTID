import cv2
import numpy as np
from deepface import DeepFace
import logging
from typing import Tuple, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preprocess_image(image_path: str, target_size: Tuple[int, int] = (160, 160)) -> Optional[np.ndarray]:
    """
    Load and preprocess an image for face recognition.
    Returns preprocessed image or None if loading fails.
    """
    try:
        # Read image
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None
            
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Failed to load image: {image_path}")
            return None
            
        # Convert BGR to RGB (DeepFace expects RGB)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize if needed
        if img_rgb.shape[0] != target_size[0] or img_rgb.shape[1] != target_size[1]:
            img_rgb = cv2.resize(img_rgb, target_size, interpolation=cv2.INTER_AREA)
            
        return img_rgb
        
    except Exception as e:
        logger.error(f"Error preprocessing image {image_path}: {str(e)}")
        return None

def match_faces(id_image_path: str, selfie_image_path: str, threshold: float = 0.6) -> bool:
    """
    Compare faces in two images using DeepFace.
    
    Args:
        id_image_path: Path to the ID document image
        selfie_image_path: Path to the selfie image
        threshold: Similarity threshold (0-1), lower is more strict
        
    Returns:
        bool: True if faces match, False otherwise or on error
    """
    try:
        logger.info(f"Starting face match between {id_image_path} and {selfie_image_path}")
        
        # Preprocess images
        id_img = preprocess_image(id_image_path)
        selfie_img = preprocess_image(selfie_image_path)
        
        if id_img is None or selfie_img is None:
            logger.error("Failed to preprocess one or both images")
            return False
            
        # Verify faces using DeepFace
        result = DeepFace.verify(
            img1_path=id_image_path,
            img2_path=selfie_image_path,
            model_name='Facenet',  # Good balance of speed and accuracy
            detector_backend='retinaface',  # Good at detecting faces in various conditions
            distance_metric='cosine',
            enforce_detection=True,  # Will raise exception if no face is detected
            align=True  # Align faces before comparison
        )
        
        # Log detailed results
        logger.info(f"Face match result: {result}")
        
        # Check if faces are similar enough
        is_verified = result.get('verified', False)
        distance = result.get('distance', 1.0)
        
        logger.info(f"Faces {'match' if is_verified else 'do not match'}. Distance: {distance:.4f}, Threshold: {threshold}")
        
        return is_verified
        
    except ValueError as ve:
        if 'Face could not be detected' in str(ve):
            logger.error("No face detected in one or both images")
        else:
            logger.error(f"Face detection error: {str(ve)}")
        return False
        
    except Exception as e:
        logger.error(f"Error during face matching: {str(e)}")
        return False
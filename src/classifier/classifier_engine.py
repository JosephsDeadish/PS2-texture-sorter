"""
Texture Classification Engine
Automatically classifies textures into 50+ categories using:
- Filename pattern matching
- Image analysis (color histograms, texture patterns)
- Metadata examination
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

from .categories import ALL_CATEGORIES, get_category_info


class TextureClassifier:
    """Main texture classification engine"""
    
    def __init__(self, config=None):
        self.config = config
        self.categories = ALL_CATEGORIES
        self.classification_cache = {}
    
    def classify_texture(self, file_path: Path, use_image_analysis=True) -> Tuple[str, float]:
        """
        Classify a texture file into a category
        
        Args:
            file_path: Path to the texture file
            use_image_analysis: Whether to use image analysis (slower but more accurate)
        
        Returns:
            Tuple of (category_id, confidence_score)
        """
        # Check cache first
        cache_key = str(file_path)
        if cache_key in self.classification_cache:
            return self.classification_cache[cache_key]
        
        # Try filename-based classification first (fast)
        category, confidence = self._classify_by_filename(file_path)
        
        # If confidence is low and image analysis is enabled, try image analysis
        if confidence < 0.7 and use_image_analysis and HAS_PIL:
            img_category, img_confidence = self._classify_by_image(file_path)
            if img_confidence > confidence:
                category, confidence = img_category, img_confidence
        
        # Cache the result
        self.classification_cache[cache_key] = (category, confidence)
        
        return category, confidence
    
    def _classify_by_filename(self, file_path: Path) -> Tuple[str, float]:
        """Classify based on filename patterns"""
        filename = file_path.stem.lower()
        best_match = "unclassified"
        best_score = 0.0
        
        # Check each category's keywords
        for category_id, category_info in self.categories.items():
            keywords = category_info.get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in filename:
                    # Score based on keyword match length and position
                    score = len(keyword) / len(filename)
                    # Bonus for exact matches or start of filename
                    if filename.startswith(keyword.lower()):
                        score += 0.2
                    if filename == keyword.lower():
                        score = 1.0
                    
                    if score > best_score:
                        best_score = score
                        best_match = category_id
        
        # Normalize score to 0-1 range
        confidence = min(1.0, best_score + 0.3)  # Add base confidence
        
        return best_match, confidence
    
    def _classify_by_image(self, file_path: Path) -> Tuple[str, float]:
        """Classify based on image analysis"""
        if not HAS_PIL:
            return "unclassified", 0.0
        
        try:
            # Load image
            img = Image.open(file_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Analyze image properties
            width, height = img.size
            aspect_ratio = width / height if height > 0 else 1.0
            
            # Get color histogram
            histogram = img.histogram()
            
            # Analyze dominant colors
            img_array = np.array(img)
            avg_color = np.mean(img_array, axis=(0, 1))
            
            # Simple heuristic-based classification
            category = "unclassified"
            confidence = 0.5
            
            # Check for UI elements (usually small, simple colors)
            if width <= 256 and height <= 256 and self._is_simple_image(img_array):
                category = "ui_elements"
                confidence = 0.6
            
            # Check for sky (blue dominant)
            elif avg_color[2] > avg_color[0] * 1.3 and avg_color[2] > avg_color[1] * 1.3:
                category = "sky"
                confidence = 0.65
            
            # Check for grass/plants (green dominant)
            elif avg_color[1] > avg_color[0] * 1.2 and avg_color[1] > avg_color[2] * 1.2:
                category = "grass"
                confidence = 0.65
            
            # Check for dirt/ground (brown tones)
            elif self._is_brown_tone(avg_color):
                category = "dirt"
                confidence = 0.6
            
            # Check for technical textures (patterns, symmetry)
            elif self._has_technical_pattern(img_array):
                category = "normal_maps"
                confidence = 0.7
            
            return category, confidence
            
        except Exception as e:
            print(f"Error analyzing image {file_path}: {e}")
            return "unclassified", 0.0
    
    def _is_simple_image(self, img_array: np.ndarray) -> bool:
        """Check if image has simple/flat colors (typical of UI)"""
        # Calculate color variance
        variance = np.var(img_array)
        return variance < 500  # Low variance = simple colors
    
    def _is_brown_tone(self, color: np.ndarray) -> bool:
        """Check if color is brown-ish"""
        r, g, b = color
        # Brown is typically R>G>B with moderate values
        return r > g and g > b and 50 < r < 200
    
    def _has_technical_pattern(self, img_array: np.ndarray) -> bool:
        """Check if image has technical/normal map patterns"""
        # Normal maps typically have purple/blue tones
        avg_color = np.mean(img_array, axis=(0, 1))
        # Check for bluish-purple dominant color
        if avg_color[2] > 100 and avg_color[0] > 80 and avg_color[1] < 100:
            return True
        return False
    
    def batch_classify(self, file_paths: List[Path], use_image_analysis=True, 
                      progress_callback=None) -> dict:
        """
        Classify multiple textures
        
        Args:
            file_paths: List of file paths to classify
            use_image_analysis: Whether to use image analysis
            progress_callback: Callback function for progress updates
        
        Returns:
            Dictionary mapping file paths to (category, confidence) tuples
        """
        results = {}
        total = len(file_paths)
        
        for i, file_path in enumerate(file_paths):
            category, confidence = self.classify_texture(file_path, use_image_analysis)
            results[str(file_path)] = (category, confidence)
            
            if progress_callback:
                progress_callback(i + 1, total)
        
        return results
    
    def clear_cache(self):
        """Clear the classification cache"""
        self.classification_cache.clear()

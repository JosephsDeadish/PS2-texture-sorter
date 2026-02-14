"""
AI-Based Background Remover Tool
Removes backgrounds from images using AI-powered subject isolation
Author: Dead On The Inside / JosephsDeadish
"""

import logging
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple, Callable
from dataclasses import dataclass
from PIL import Image, ImageFilter
import threading
import queue

logger = logging.getLogger(__name__)

# Check for rembg availability (AI background removal)
try:
    from rembg import remove, new_session
    HAS_REMBG = True
    logger.info("rembg available for AI background removal")
except ImportError:
    HAS_REMBG = False
    logger.warning("rembg not available - AI background removal disabled")

# Check for OpenCV availability (for edge refinement)
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    logger.warning("opencv-python not available - advanced edge refinement disabled")


@dataclass
class BackgroundRemovalResult:
    """Result of a background removal operation."""
    input_path: str
    output_path: str
    success: bool
    error_message: str = ""
    processing_time: float = 0.0
    original_size: Tuple[int, int] = (0, 0)
    output_size: Tuple[int, int] = (0, 0)


class BackgroundRemover:
    """
    AI-powered background remover with batch processing capabilities.
    """
    
    def __init__(self, model_name: str = "u2net"):
        """
        Initialize the background remover.
        
        Args:
            model_name: Model to use for background removal
                       Options: 'u2net', 'u2netp', 'u2net_human_seg', 'silueta'
        """
        self.model_name = model_name
        self.session = None
        self.processing_queue = queue.Queue()
        self.results_queue = queue.Queue()
        self.is_processing = False
        self.cancel_requested = False
        
        # Edge refinement settings
        self.edge_refinement = 0.5  # 0 = no refinement, 1 = maximum refinement
        self.feather_radius = 2  # Pixel radius for edge feathering
        
        # Initialize session if rembg available
        if HAS_REMBG:
            try:
                self.session = new_session(model_name)
                logger.info(f"Background removal session initialized with model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize background removal session: {e}")
                self.session = None
    
    def is_available(self) -> bool:
        """Check if background removal is available."""
        return HAS_REMBG and self.session is not None
    
    def set_edge_refinement(self, refinement: float):
        """
        Set edge refinement level.
        
        Args:
            refinement: Refinement level (0.0 to 1.0)
                       0.0 = no refinement (sharp edges)
                       1.0 = maximum refinement (very smooth edges)
        """
        self.edge_refinement = max(0.0, min(1.0, refinement))
        self.feather_radius = int(1 + self.edge_refinement * 5)  # 1-6 pixel radius
        logger.debug(f"Edge refinement set to {self.edge_refinement:.2f}, feather radius: {self.feather_radius}")
    
    def remove_background(
        self, 
        image: Image.Image,
        alpha_matting: bool = False,
        alpha_matting_foreground_threshold: int = 240,
        alpha_matting_background_threshold: int = 10,
        alpha_matting_erode_size: int = 10
    ) -> Optional[Image.Image]:
        """
        Remove background from a single image.
        
        Args:
            image: Input PIL Image
            alpha_matting: Enable alpha matting for better edges
            alpha_matting_foreground_threshold: Foreground threshold for alpha matting
            alpha_matting_background_threshold: Background threshold for alpha matting
            alpha_matting_erode_size: Erosion size for alpha matting
        
        Returns:
            Image with transparent background or None on failure
        """
        if not self.is_available():
            logger.error("Background removal not available")
            return None
        
        try:
            # Remove background using rembg
            output = remove(
                image,
                session=self.session,
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=alpha_matting_background_threshold,
                alpha_matting_erode_size=alpha_matting_erode_size
            )
            
            # Apply edge refinement if enabled
            if self.edge_refinement > 0.0:
                output = self._refine_edges(output)
            
            return output
            
        except Exception as e:
            logger.error(f"Background removal failed: {e}")
            return None
    
    def _refine_edges(self, image: Image.Image) -> Image.Image:
        """
        Refine edges of the transparent image for smoother results.
        
        Args:
            image: Image with alpha channel
        
        Returns:
            Image with refined edges
        """
        try:
            # Ensure image has alpha channel
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Extract alpha channel
            alpha = image.split()[-1]
            
            # Apply Gaussian blur to alpha channel for smooth edges
            if self.feather_radius > 0:
                alpha = alpha.filter(ImageFilter.GaussianBlur(radius=self.feather_radius))
            
            # Optionally use OpenCV for advanced edge refinement
            if HAS_CV2 and self.edge_refinement > 0.5:
                alpha_np = np.array(alpha)
                
                # Apply morphological operations for cleaner edges
                kernel_size = int(1 + self.edge_refinement * 3)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
                
                # Close small holes
                alpha_np = cv2.morphologyEx(alpha_np, cv2.MORPH_CLOSE, kernel)
                
                # Smooth the edges
                alpha_np = cv2.GaussianBlur(alpha_np, (0, 0), sigmaX=self.edge_refinement * 2)
                
                alpha = Image.fromarray(alpha_np)
            
            # Recombine with RGB channels
            r, g, b, _ = image.split()
            refined = Image.merge('RGBA', (r, g, b, alpha))
            
            return refined
            
        except Exception as e:
            logger.error(f"Edge refinement failed: {e}")
            return image  # Return original if refinement fails
    
    def remove_background_from_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> BackgroundRemovalResult:
        """
        Remove background from an image file.
        
        Args:
            input_path: Path to input image
            output_path: Path to output image (default: input_path with '_nobg.png' suffix)
            **kwargs: Additional arguments for remove_background
        
        Returns:
            BackgroundRemovalResult with operation details
        """
        import time
        start_time = time.time()
        
        input_path = Path(input_path)
        
        # Determine output path
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_nobg.png"
        else:
            output_path = Path(output_path)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Load image
            image = Image.open(input_path)
            original_size = image.size
            
            # Remove background
            result_image = self.remove_background(image, **kwargs)
            
            if result_image is None:
                return BackgroundRemovalResult(
                    input_path=str(input_path),
                    output_path=str(output_path),
                    success=False,
                    error_message="Background removal failed",
                    processing_time=time.time() - start_time
                )
            
            # Save as PNG with transparency
            result_image.save(output_path, 'PNG', optimize=True)
            output_size = result_image.size
            
            processing_time = time.time() - start_time
            
            logger.info(f"Background removed: {input_path.name} -> {output_path.name} ({processing_time:.2f}s)")
            
            return BackgroundRemovalResult(
                input_path=str(input_path),
                output_path=str(output_path),
                success=True,
                processing_time=processing_time,
                original_size=original_size,
                output_size=output_size
            )
            
        except Exception as e:
            logger.error(f"Failed to process {input_path}: {e}")
            return BackgroundRemovalResult(
                input_path=str(input_path),
                output_path=str(output_path),
                success=False,
                error_message=str(e),
                processing_time=time.time() - start_time
            )
    
    def batch_process(
        self,
        input_paths: List[str],
        output_dir: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        **kwargs
    ) -> List[BackgroundRemovalResult]:
        """
        Process multiple images in batch.
        
        Args:
            input_paths: List of input image paths
            output_dir: Directory for output images (default: same as input)
            progress_callback: Callback function(current, total, filename)
            **kwargs: Additional arguments for remove_background
        
        Returns:
            List of BackgroundRemovalResult objects
        """
        results = []
        total = len(input_paths)
        
        self.cancel_requested = False
        
        for i, input_path in enumerate(input_paths):
            # Check for cancellation
            if self.cancel_requested:
                logger.info("Batch processing cancelled")
                break
            
            # Determine output path
            input_path = Path(input_path)
            if output_dir:
                output_path = Path(output_dir) / f"{input_path.stem}_nobg.png"
            else:
                output_path = None
            
            # Progress callback
            if progress_callback:
                progress_callback(i + 1, total, input_path.name)
            
            # Process image
            result = self.remove_background_from_file(
                str(input_path),
                str(output_path) if output_path else None,
                **kwargs
            )
            results.append(result)
        
        # Final summary
        successful = sum(1 for r in results if r.success)
        failed = total - successful
        total_time = sum(r.processing_time for r in results)
        
        logger.info(
            f"Batch processing complete: {successful} successful, {failed} failed, "
            f"total time: {total_time:.2f}s"
        )
        
        return results
    
    def batch_process_async(
        self,
        input_paths: List[str],
        output_dir: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        completion_callback: Optional[Callable[[List[BackgroundRemovalResult]], None]] = None,
        **kwargs
    ) -> threading.Thread:
        """
        Process multiple images asynchronously in a background thread.
        
        Args:
            input_paths: List of input image paths
            output_dir: Directory for output images
            progress_callback: Callback function(current, total, filename)
            completion_callback: Callback when processing completes
            **kwargs: Additional arguments for remove_background
        
        Returns:
            Thread object (already started)
        """
        def worker():
            self.is_processing = True
            try:
                results = self.batch_process(
                    input_paths,
                    output_dir,
                    progress_callback,
                    **kwargs
                )
                if completion_callback:
                    completion_callback(results)
            finally:
                self.is_processing = False
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread
    
    def cancel_processing(self):
        """Cancel ongoing batch processing."""
        self.cancel_requested = True
        logger.info("Cancellation requested")
    
    def get_supported_models(self) -> List[str]:
        """
        Get list of supported models.
        
        Returns:
            List of model names
        """
        return [
            'u2net',          # General purpose (largest, most accurate)
            'u2netp',         # Lightweight version (faster, smaller)
            'u2net_human_seg', # Optimized for human subjects
            'silueta'         # Alternative general purpose model
        ]
    
    def change_model(self, model_name: str) -> bool:
        """
        Change the background removal model.
        
        Args:
            model_name: Name of the model to use
        
        Returns:
            True if model changed successfully
        """
        if model_name not in self.get_supported_models():
            logger.error(f"Unsupported model: {model_name}")
            return False
        
        if not HAS_REMBG:
            logger.error("rembg not available")
            return False
        
        try:
            self.model_name = model_name
            self.session = new_session(model_name)
            logger.info(f"Model changed to: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to change model: {e}")
            return False


def check_dependencies() -> dict:
    """
    Check if required dependencies are installed.
    
    Returns:
        Dict with availability status for each dependency
    """
    return {
        'rembg': HAS_REMBG,
        'opencv': HAS_CV2,
        'pil': True  # PIL/Pillow is always available in this project
    }


if __name__ == "__main__":
    # Test background remover
    print("Background Remover Test")
    print("=" * 50)
    
    deps = check_dependencies()
    print("Dependencies:")
    for dep, available in deps.items():
        status = "✓" if available else "✗"
        print(f"  {status} {dep}")
    print()
    
    if HAS_REMBG:
        print("✓ Background removal is available")
        remover = BackgroundRemover()
        print(f"  Current model: {remover.model_name}")
        print(f"  Supported models: {', '.join(remover.get_supported_models())}")
    else:
        print("✗ Background removal not available")
        print("  Install with: pip install rembg")

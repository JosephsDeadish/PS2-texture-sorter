"""
File Handler Module
Handles file operations, conversions, and integrity checks
"""

import shutil
import hashlib
from pathlib import Path
from typing import List, Optional, Tuple
import send2trash

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class FileHandler:
    """Handles file operations for texture sorting"""
    
    SUPPORTED_FORMATS = {'.dds', '.png', '.jpg', '.jpeg', '.tga', '.bmp'}
    
    def __init__(self, create_backup=True):
        self.create_backup = create_backup
        self.operations_log = []
    
    def convert_dds_to_png(self, dds_path: Path, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Convert DDS file to PNG
        
        Args:
            dds_path: Path to DDS file
            output_path: Optional output path, defaults to same location with .png extension
        
        Returns:
            Path to converted PNG file or None if conversion failed
        """
        if not HAS_PIL:
            print("PIL/Pillow not available. Cannot convert images.")
            return None
        
        try:
            # Set output path
            if output_path is None:
                output_path = dds_path.with_suffix('.png')
            
            # Open and convert
            img = Image.open(dds_path)
            img.save(output_path, 'PNG')
            
            self.operations_log.append(f"Converted {dds_path} to {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error converting {dds_path} to PNG: {e}")
            return None
    
    def convert_png_to_dds(self, png_path: Path, output_path: Optional[Path] = None, 
                          format='DXT5') -> Optional[Path]:
        """
        Convert PNG file to DDS
        
        Args:
            png_path: Path to PNG file
            output_path: Optional output path, defaults to same location with .dds extension
            format: DDS compression format (DXT1, DXT5, etc.)
        
        Returns:
            Path to converted DDS file or None if conversion failed
        """
        if not HAS_PIL:
            print("PIL/Pillow not available. Cannot convert images.")
            return None
        
        try:
            # Set output path
            if output_path is None:
                output_path = png_path.with_suffix('.dds')
            
            # Open and convert
            img = Image.open(png_path)
            
            # Note: Basic PIL/Pillow has limited DDS write support
            # For full DDS support, would need additional libraries
            img.save(output_path, 'DDS')
            
            self.operations_log.append(f"Converted {png_path} to {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error converting {png_path} to DDS: {e}")
            return None
    
    def batch_convert(self, file_paths: List[Path], target_format: str, 
                     output_dir: Optional[Path] = None, progress_callback=None) -> List[Path]:
        """
        Batch convert multiple files
        
        Args:
            file_paths: List of files to convert
            target_format: Target format ('png' or 'dds')
            output_dir: Optional output directory
            progress_callback: Callback for progress updates
        
        Returns:
            List of successfully converted file paths
        """
        converted = []
        total = len(file_paths)
        
        for i, file_path in enumerate(file_paths):
            output_path = None
            if output_dir:
                output_path = output_dir / file_path.with_suffix(f'.{target_format}').name
            
            if target_format.lower() == 'png' and file_path.suffix.lower() == '.dds':
                result = self.convert_dds_to_png(file_path, output_path)
            elif target_format.lower() == 'dds' and file_path.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                result = self.convert_png_to_dds(file_path, output_path)
            else:
                result = None
            
            if result:
                converted.append(result)
            
            if progress_callback:
                progress_callback(i + 1, total)
        
        return converted
    
    def check_file_integrity(self, file_path: Path) -> Tuple[bool, str]:
        """
        Check if file is valid and not corrupted
        
        Args:
            file_path: Path to file to check
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file exists
        if not file_path.exists():
            return False, "File does not exist"
        
        # Check file size
        if file_path.stat().st_size == 0:
            return False, "File is empty"
        
        # Try to open as image
        if HAS_PIL and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
            try:
                img = Image.open(file_path)
                img.verify()  # Verify it's a valid image
                return True, "OK"
            except Exception as e:
                return False, f"Image corrupted: {str(e)}"
        
        return True, "OK"
    
    def calculate_file_hash(self, file_path: Path, algorithm='md5') -> str:
        """
        Calculate hash of file for duplicate detection
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm ('md5', 'sha256')
        
        Returns:
            Hex string of file hash
        """
        hash_obj = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
        
        # Read file in chunks for memory efficiency
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
    
    def find_duplicates(self, file_paths: List[Path], by_hash=True) -> dict:
        """
        Find duplicate files
        
        Args:
            file_paths: List of file paths to check
            by_hash: Use hash comparison (slower but accurate) vs name+size (faster)
        
        Returns:
            Dictionary mapping original files to lists of duplicates
        """
        if by_hash:
            hash_map = {}
            duplicates = {}
            
            for file_path in file_paths:
                file_hash = self.calculate_file_hash(file_path)
                
                if file_hash in hash_map:
                    # Found duplicate
                    original = hash_map[file_hash]
                    if original not in duplicates:
                        duplicates[original] = []
                    duplicates[original].append(file_path)
                else:
                    hash_map[file_hash] = file_path
            
            return duplicates
        else:
            # Compare by name and size (faster)
            size_name_map = {}
            duplicates = {}
            
            for file_path in file_paths:
                key = (file_path.name, file_path.stat().st_size)
                
                if key in size_name_map:
                    original = size_name_map[key]
                    if original not in duplicates:
                        duplicates[original] = []
                    duplicates[original].append(file_path)
                else:
                    size_name_map[key] = file_path
            
            return duplicates
    
    def safe_copy(self, source: Path, destination: Path, overwrite=False) -> bool:
        """
        Safely copy file with backup
        
        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite existing file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create parent directory if needed
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if destination exists
            if destination.exists() and not overwrite:
                print(f"Destination {destination} already exists. Skipping.")
                return False
            
            # Create backup if enabled
            if self.create_backup and destination.exists():
                backup_path = destination.with_suffix(destination.suffix + '.backup')
                shutil.copy2(destination, backup_path)
            
            # Copy file
            shutil.copy2(source, destination)
            self.operations_log.append(f"Copied {source} to {destination}")
            return True
            
        except Exception as e:
            print(f"Error copying {source} to {destination}: {e}")
            return False
    
    def safe_move(self, source: Path, destination: Path, overwrite=False) -> bool:
        """
        Safely move file
        
        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite existing file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create parent directory if needed
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if destination exists
            if destination.exists() and not overwrite:
                print(f"Destination {destination} already exists. Skipping.")
                return False
            
            # Move file
            shutil.move(str(source), str(destination))
            self.operations_log.append(f"Moved {source} to {destination}")
            return True
            
        except Exception as e:
            print(f"Error moving {source} to {destination}: {e}")
            return False
    
    def safe_delete(self, file_path: Path, use_trash=True) -> bool:
        """
        Safely delete file (optionally to trash)
        
        Args:
            file_path: File to delete
            use_trash: Send to trash instead of permanent delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if use_trash:
                send2trash.send2trash(str(file_path))
            else:
                file_path.unlink()
            
            self.operations_log.append(f"Deleted {file_path}")
            return True
            
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            return False
    
    def get_operations_log(self) -> List[str]:
        """Get log of all operations performed"""
        return self.operations_log.copy()
    
    def clear_operations_log(self):
        """Clear the operations log"""
        self.operations_log.clear()

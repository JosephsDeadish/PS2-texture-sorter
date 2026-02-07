"""
Search and Filter System
Advanced search and filtering for PS2 textures with preset support
Author: Dead On The Inside / JosephsDeadish
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from threading import Lock

logger = logging.getLogger(__name__)


@dataclass
class FilterCriteria:
    """Represents a single filter criterion."""
    name: Optional[str] = None
    name_regex: Optional[str] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    categories: Optional[List[str]] = None
    formats: Optional[List[str]] = None
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
    is_favorite: Optional[bool] = None
    is_problematic: Optional[bool] = None
    modified_after: Optional[str] = None
    modified_before: Optional[str] = None


@dataclass
class SearchPreset:
    """Represents a saved search preset."""
    name: str
    criteria: FilterCriteria
    description: str = ""
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class SearchFilter:
    """
    Advanced search and filtering system for PS2 textures.
    
    Features:
    - Search by name, size, category, format, resolution
    - Advanced regex filtering
    - Save/load search presets
    - Quick filters (favorites, recent, problematic)
    - Combine multiple filters with AND/OR logic
    - Thread-safe operations
    """
    
    def __init__(self, presets_file: Optional[Path] = None):
        """
        Initialize search filter system.
        
        Args:
            presets_file: Path to save/load presets (defaults to config dir)
        """
        self.presets_file = presets_file or Path("config/search_presets.json")
        self.presets: Dict[str, SearchPreset] = {}
        self.recent_files: List[Path] = []
        self.favorites: Set[Path] = set()
        self.problematic: Set[Path] = set()
        self._lock = Lock()
        
        logger.debug(f"SearchFilter initialized with presets_file={self.presets_file}")
        self._load_presets()
    
    def search(
        self,
        files: List[Path],
        criteria: FilterCriteria,
        combine_mode: str = "AND",
        metadata_provider: Optional[Callable[[Path], Dict[str, Any]]] = None
    ) -> List[Path]:
        """
        Search and filter files based on criteria.
        
        Args:
            files: List of file paths to search
            criteria: Filter criteria to apply
            combine_mode: How to combine filters ("AND" or "OR")
            metadata_provider: Optional function to get file metadata
            
        Returns:
            List of file paths matching the criteria
        """
        try:
            logger.debug(f"Searching {len(files)} files with combine_mode={combine_mode}")
            results = []
            
            for file_path in files:
                if self._matches_criteria(file_path, criteria, combine_mode, metadata_provider):
                    results.append(file_path)
            
            logger.info(f"Search found {len(results)} matching files out of {len(files)}")
            return results
            
        except Exception as e:
            logger.error(f"Error during search: {e}", exc_info=True)
            return []
    
    def _matches_criteria(
        self,
        file_path: Path,
        criteria: FilterCriteria,
        combine_mode: str,
        metadata_provider: Optional[Callable[[Path], Dict[str, Any]]]
    ) -> bool:
        """
        Check if a file matches the given criteria.
        
        Args:
            file_path: Path to file
            criteria: Filter criteria
            combine_mode: "AND" or "OR"
            metadata_provider: Function to get metadata
            
        Returns:
            True if file matches criteria
        """
        matches = []
        
        try:
            # Name filter
            if criteria.name is not None:
                matches.append(criteria.name.lower() in file_path.name.lower())
            
            # Regex filter
            if criteria.name_regex is not None:
                try:
                    pattern = re.compile(criteria.name_regex, re.IGNORECASE)
                    matches.append(bool(pattern.search(file_path.name)))
                except re.error as e:
                    logger.warning(f"Invalid regex pattern '{criteria.name_regex}': {e}")
                    matches.append(False)
            
            # File size filters
            if criteria.min_size is not None or criteria.max_size is not None:
                try:
                    file_size = file_path.stat().st_size
                    if criteria.min_size is not None:
                        matches.append(file_size >= criteria.min_size)
                    if criteria.max_size is not None:
                        matches.append(file_size <= criteria.max_size)
                except OSError:
                    matches.append(False)
            
            # Format filter
            if criteria.formats is not None:
                matches.append(file_path.suffix.lower() in [f.lower() for f in criteria.formats])
            
            # Get metadata if needed for remaining filters
            metadata = None
            if metadata_provider and any([
                criteria.categories,
                criteria.min_width,
                criteria.max_width,
                criteria.min_height,
                criteria.max_height
            ]):
                metadata = metadata_provider(file_path)
            
            # Category filter
            if criteria.categories is not None and metadata:
                category = metadata.get('category', '')
                matches.append(category in criteria.categories)
            
            # Resolution filters
            if metadata:
                width = metadata.get('width', 0)
                height = metadata.get('height', 0)
                
                if criteria.min_width is not None:
                    matches.append(width >= criteria.min_width)
                if criteria.max_width is not None:
                    matches.append(width <= criteria.max_width)
                if criteria.min_height is not None:
                    matches.append(height >= criteria.min_height)
                if criteria.max_height is not None:
                    matches.append(height <= criteria.max_height)
            
            # Quick filters
            if criteria.is_favorite is not None:
                with self._lock:
                    matches.append((file_path in self.favorites) == criteria.is_favorite)
            
            if criteria.is_problematic is not None:
                with self._lock:
                    matches.append((file_path in self.problematic) == criteria.is_problematic)
            
            # Modified date filters
            if criteria.modified_after or criteria.modified_before:
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    if criteria.modified_after:
                        after = datetime.fromisoformat(criteria.modified_after)
                        matches.append(mtime >= after)
                    
                    if criteria.modified_before:
                        before = datetime.fromisoformat(criteria.modified_before)
                        matches.append(mtime <= before)
                except (OSError, ValueError):
                    matches.append(False)
            
            # Combine results
            if not matches:
                return True  # No criteria = match all
            
            if combine_mode.upper() == "OR":
                return any(matches)
            else:  # AND
                return all(matches)
                
        except Exception as e:
            logger.error(f"Error matching criteria for {file_path}: {e}")
            return False
    
    def quick_filter_favorites(self, files: List[Path]) -> List[Path]:
        """
        Quick filter to show only favorite files.
        
        Args:
            files: List of files to filter
            
        Returns:
            List of favorite files
        """
        with self._lock:
            return [f for f in files if f in self.favorites]
    
    def quick_filter_recent(self, files: List[Path], limit: int = 50) -> List[Path]:
        """
        Quick filter to show recently accessed files.
        
        Args:
            files: List of files to filter
            limit: Maximum number of recent files
            
        Returns:
            List of recent files
        """
        with self._lock:
            recent_set = set(self.recent_files[-limit:])
            return [f for f in files if f in recent_set]
    
    def quick_filter_problematic(self, files: List[Path]) -> List[Path]:
        """
        Quick filter to show problematic files.
        
        Args:
            files: List of files to filter
            
        Returns:
            List of problematic files
        """
        with self._lock:
            return [f for f in files if f in self.problematic]
    
    def mark_favorite(self, file_path: Path, is_favorite: bool = True):
        """
        Mark a file as favorite or remove favorite status.
        
        Args:
            file_path: Path to file
            is_favorite: True to mark as favorite, False to remove
        """
        with self._lock:
            if is_favorite:
                self.favorites.add(file_path)
                logger.debug(f"Marked as favorite: {file_path}")
            else:
                self.favorites.discard(file_path)
                logger.debug(f"Removed favorite: {file_path}")
    
    def mark_problematic(self, file_path: Path, is_problematic: bool = True):
        """
        Mark a file as problematic or remove problematic status.
        
        Args:
            file_path: Path to file
            is_problematic: True to mark as problematic, False to remove
        """
        with self._lock:
            if is_problematic:
                self.problematic.add(file_path)
                logger.debug(f"Marked as problematic: {file_path}")
            else:
                self.problematic.discard(file_path)
                logger.debug(f"Removed problematic: {file_path}")
    
    def add_recent(self, file_path: Path, max_recent: int = 100):
        """
        Add a file to recent files list.
        
        Args:
            file_path: Path to file
            max_recent: Maximum number of recent files to keep
        """
        with self._lock:
            if file_path in self.recent_files:
                self.recent_files.remove(file_path)
            self.recent_files.append(file_path)
            
            # Keep only the most recent files
            if len(self.recent_files) > max_recent:
                self.recent_files = self.recent_files[-max_recent:]
    
    def save_preset(self, name: str, criteria: FilterCriteria, description: str = ""):
        """
        Save a search preset.
        
        Args:
            name: Name of the preset
            criteria: Filter criteria to save
            description: Optional description
        """
        try:
            with self._lock:
                preset = SearchPreset(
                    name=name,
                    criteria=criteria,
                    description=description
                )
                self.presets[name] = preset
                self._save_presets()
                logger.info(f"Saved search preset: {name}")
        except Exception as e:
            logger.error(f"Error saving preset '{name}': {e}", exc_info=True)
    
    def load_preset(self, name: str) -> Optional[FilterCriteria]:
        """
        Load a search preset by name.
        
        Args:
            name: Name of the preset
            
        Returns:
            FilterCriteria if preset exists, None otherwise
        """
        with self._lock:
            preset = self.presets.get(name)
            if preset:
                logger.debug(f"Loaded preset: {name}")
                return preset.criteria
            else:
                logger.warning(f"Preset not found: {name}")
                return None
    
    def delete_preset(self, name: str) -> bool:
        """
        Delete a search preset.
        
        Args:
            name: Name of the preset to delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            with self._lock:
                if name in self.presets:
                    del self.presets[name]
                    self._save_presets()
                    logger.info(f"Deleted preset: {name}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting preset '{name}': {e}", exc_info=True)
            return False
    
    def list_presets(self) -> List[Dict[str, str]]:
        """
        Get list of all saved presets.
        
        Returns:
            List of preset info dictionaries
        """
        with self._lock:
            return [
                {
                    'name': name,
                    'description': preset.description,
                    'created_at': preset.created_at
                }
                for name, preset in self.presets.items()
            ]
    
    def _save_presets(self):
        """Save presets to file."""
        try:
            self.presets_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                name: {
                    'name': preset.name,
                    'description': preset.description,
                    'created_at': preset.created_at,
                    'criteria': asdict(preset.criteria)
                }
                for name, preset in self.presets.items()
            }
            
            with open(self.presets_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            logger.debug(f"Saved {len(self.presets)} presets to {self.presets_file}")
            
        except Exception as e:
            logger.error(f"Error saving presets: {e}", exc_info=True)
    
    def _load_presets(self):
        """Load presets from file."""
        try:
            if not self.presets_file.exists():
                logger.debug("Presets file does not exist, starting with empty presets")
                return
            
            with open(self.presets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.presets = {}
            for name, preset_data in data.items():
                criteria_dict = preset_data.get('criteria', {})
                criteria = FilterCriteria(**criteria_dict)
                
                preset = SearchPreset(
                    name=preset_data['name'],
                    criteria=criteria,
                    description=preset_data.get('description', ''),
                    created_at=preset_data.get('created_at', '')
                )
                self.presets[name] = preset
            
            logger.info(f"Loaded {len(self.presets)} presets from {self.presets_file}")
            
        except Exception as e:
            logger.error(f"Error loading presets: {e}", exc_info=True)
            self.presets = {}
    
    def combine_filters(
        self,
        files: List[Path],
        criteria_list: List[FilterCriteria],
        mode: str = "AND",
        metadata_provider: Optional[Callable[[Path], Dict[str, Any]]] = None
    ) -> List[Path]:
        """
        Apply multiple filter criteria with AND/OR logic.
        
        Args:
            files: List of files to filter
            criteria_list: List of FilterCriteria to apply
            mode: "AND" to match all criteria, "OR" to match any
            metadata_provider: Optional metadata provider function
            
        Returns:
            List of files matching the combined criteria
        """
        try:
            if not criteria_list:
                return files
            
            results_list = [
                self.search(files, criteria, "AND", metadata_provider)
                for criteria in criteria_list
            ]
            
            if mode.upper() == "OR":
                # Union of all results
                combined = set()
                for results in results_list:
                    combined.update(results)
                return list(combined)
            else:  # AND
                # Intersection of all results
                combined = set(results_list[0]) if results_list else set()
                for results in results_list[1:]:
                    combined.intersection_update(results)
                return list(combined)
                
        except Exception as e:
            logger.error(f"Error combining filters: {e}", exc_info=True)
            return []

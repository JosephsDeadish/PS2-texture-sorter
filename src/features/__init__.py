"""
Feature modules for Game Texture Sorter
Includes statistics tracking, texture analysis, search/filter, profiles, batch operations, LOD replacement, backups,
hotkeys, sound system, and achievements
Author: Dead On The Inside / JosephsDeadish
"""

import logging
_log = logging.getLogger(__name__)

__all__ = []

from .statistics import StatisticsTracker
__all__.append('StatisticsTracker')

from .texture_analysis import TextureAnalyzer
__all__.append('TextureAnalyzer')

from .search_filter import SearchFilter, FilterCriteria, SearchPreset
__all__.extend(['SearchFilter', 'FilterCriteria', 'SearchPreset'])

from .profile_manager import ProfileManager, OrganizationProfile, GameTemplate
__all__.extend(['ProfileManager', 'OrganizationProfile', 'GameTemplate'])

from .batch_operations import BatchQueue, Operation, OperationStatus, OperationPriority, BatchOperationHelper
__all__.extend(['BatchQueue', 'Operation', 'OperationStatus', 'OperationPriority', 'BatchOperationHelper'])

from .lod_replacement import LODReplacer, LODTexture, LODGroup
__all__.extend(['LODReplacer', 'LODTexture', 'LODGroup'])

from .backup_system import BackupManager, BackupMetadata, RestorePoint
__all__.extend(['BackupManager', 'BackupMetadata', 'RestorePoint'])

# pynput is an optional runtime dep; guard so the package is importable without it
try:
    from .hotkey_manager import HotkeyManager, Hotkey
    __all__.extend(['HotkeyManager', 'Hotkey'])
except ImportError as _e:
    _log.warning(f"HotkeyManager unavailable (pynput missing?): {_e}")
    HotkeyManager = None  # type: ignore[assignment,misc]
    Hotkey = None         # type: ignore[assignment,misc]

# pygame / sounddevice are optional audio deps
try:
    from .sound_manager import SoundManager, SoundEvent, SoundPack
    __all__.extend(['SoundManager', 'SoundEvent', 'SoundPack'])
except ImportError as _e:
    _log.warning(f"SoundManager unavailable (audio library missing?): {_e}")
    SoundManager = None  # type: ignore[assignment,misc]
    SoundEvent = None    # type: ignore[assignment,misc]
    SoundPack = None     # type: ignore[assignment,misc]

from .achievements import AchievementSystem, Achievement, AchievementTier
__all__.extend(['AchievementSystem', 'Achievement', 'AchievementTier'])

from .panda_character import PandaMood
__all__.append('PandaMood')

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

from .panda_character import PandaCharacter, PandaFacing, PandaGender, PandaMood
__all__.extend(['PandaCharacter', 'PandaFacing', 'PandaGender', 'PandaMood'])

from .panda_stats import PandaStats
__all__.append('PandaStats')

from .panda_widgets import WidgetCollection, WidgetType, WidgetRarity, PandaWidget, ItemPhysics, WidgetStats
__all__.extend(['WidgetCollection', 'WidgetType', 'WidgetRarity', 'PandaWidget', 'ItemPhysics', 'WidgetStats'])

from .shop_system import ShopSystem, ShopItem, ShopCategory
__all__.extend(['ShopSystem', 'ShopItem', 'ShopCategory'])

from .currency_system import CurrencySystem, MoneyTransaction
__all__.extend(['CurrencySystem', 'MoneyTransaction'])

from .minigame_system import (MiniGameManager, MiniGame, PandaClickGame,
                               PandaMemoryGame, PandaReflexGame,
                               GameDifficulty, GameResult)
__all__.extend(['MiniGameManager', 'MiniGame', 'PandaClickGame',
                'PandaMemoryGame', 'PandaReflexGame', 'GameDifficulty', 'GameResult'])

from .level_system import LevelSystem, UserLevelSystem, PandaLevelSystem, Level, LevelReward
__all__.extend(['LevelSystem', 'UserLevelSystem', 'PandaLevelSystem', 'Level', 'LevelReward'])

from .game_identifier import GameIdentifier, GameInfo
__all__.extend(['GameIdentifier', 'GameInfo'])

from .auto_backup import AutoBackupSystem, BackupConfig
__all__.extend(['AutoBackupSystem', 'BackupConfig'])

from .translation_manager import TranslationManager, Language
__all__.extend(['TranslationManager', 'Language'])

from .tutorial_system import (TutorialManager, TutorialStep, TooltipMode,
                               TooltipVerbosityManager)
__all__.extend(['TutorialManager', 'TutorialStep', 'TooltipMode', 'TooltipVerbosityManager'])

from .panda_mood_system import PandaMoodSystem
__all__.append('PandaMoodSystem')

from .panda_closet import (CustomizationCategory, ClothingSubCategory,
                            AccessorySubCategory, ItemRarity, CustomizationItem)
__all__.extend(['CustomizationCategory', 'ClothingSubCategory',
                'AccessorySubCategory', 'ItemRarity', 'CustomizationItem'])

from .quest_system import QuestSystem, Quest, QuestType, QuestStatus
__all__.extend(['QuestSystem', 'Quest', 'QuestType', 'QuestStatus'])

"""
PS2 Texture Sorter - AI Model System
Comprehensive AI-powered texture classification with offline and online support
Author: Dead On The Inside / JosephsDeadish
"""

from .offline_model import OfflineModel, create_default_model, get_default_model_path
from .online_model import OnlineModel, create_online_model_from_config, RateLimitConfig
from .model_manager import ModelManager
from .training import TrainingDataStore, IncrementalLearner
from .model_exporter import ModelExporter, ModelImporter, ModelPackage, validate_ps2model_file

__all__ = [
    # Offline model
    'OfflineModel',
    'create_default_model',
    'get_default_model_path',
    
    # Online model
    'OnlineModel',
    'create_online_model_from_config',
    'RateLimitConfig',
    
    # Model manager
    'ModelManager',
    
    # Training system
    'TrainingDataStore',
    'IncrementalLearner',
    
    # Export/Import
    'ModelExporter',
    'ModelImporter',
    'ModelPackage',
    'validate_ps2model_file',
]

__version__ = '1.0.0'
__author__ = 'Dead On The Inside / JosephsDeadish'

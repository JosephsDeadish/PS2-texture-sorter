"""
UI Module
Custom UI components and customization systems
"""

# Make imports optional to avoid circular dependencies
try:
    from .customization_panel import (
        ColorWheelWidget,
        CursorCustomizer,
        ThemeManager,
        CustomizationPanel,
        open_customization_dialog,
        THEME_PRESETS
    )
    __all__ = [
        'ColorWheelWidget',
        'CursorCustomizer',
        'ThemeManager',
        'CustomizationPanel',
        'open_customization_dialog',
        'THEME_PRESETS'
    ]
except ImportError:
    # Customization panel not available
    __all__ = []

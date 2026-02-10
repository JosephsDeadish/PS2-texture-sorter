"""
Tooltip System - Application tooltips with optional vulgar mode
Separate from panda character - this is a UI/UX feature
Author: Dead On The Inside / JosephsDeadish
"""

import logging
import random
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class TooltipSystem:
    """Manages application tooltips with normal and vulgar variants."""
    
    # Comprehensive tooltip system
    TOOLTIPS = {
        'sort_button': {
            'normal': [
                "Click to sort your textures into organized folders",
                "Begin the texture organization process",
                "Start sorting textures by category and LOD level",
                "Organize your textures with intelligent sorting",
                "Sort textures into their proper directories",
                "Initiate the automated texture sorting workflow"
            ],
            'vulgar': [
                "Click this to sort your damn textures. It's not rocket science, Karen.",
                "Organize these bad boys into folders. Like Marie Kondo but with more profanity.",
                "Sort this sh*t out. Literally. That's what the button does.",
                "Time to unfuck your texture directory structure.",
                "Click here unless you enjoy chaos and madness.",
                "Make your textures less of a clusterfuck with one click."
            ]
        },
        'convert_button': {
            'normal': [
                "Convert textures to different formats",
                "Transform your textures into the desired format",
                "Begin batch texture format conversion",
                "Convert texture files to supported formats",
                "Process and convert texture formats efficiently",
                "Start the texture conversion process"
            ],
            'vulgar': [
                "Turn your textures into whatever the hell format you need.",
                "Convert this sh*t. PNG, DDS, whatever floats your boat.",
                "Magic button that transforms textures. No rabbits or hats required.",
                "Because apparently your textures are in the wrong goddamn format.",
                "Click to unfuck your texture formats.",
                "Convert or die. Well, not die. But your project might."
            ]
        },
        'settings_button': {
            'normal': [
                "Open settings and preferences",
                "Configure application options",
                "Adjust your preferences and settings",
                "Access configuration options",
                "Customize your application settings",
                "Modify application behavior and appearance"
            ],
            'vulgar': [
                "Tweak sh*t. Make it yours. Go nuts.",
                "Settings, preferences, all that boring but necessary crap.",
                "Click here if you're picky about how things work. We don't judge.",
                "Configure this bad boy to your heart's content.",
                "Mess with settings until something breaks. Then undo.",
                "For control freaks and perfectionists. You know who you are."
            ]
        },
        'browse_button': {
            'normal': [
                "Browse for a folder",
                "Select a directory from your computer",
                "Choose folder location",
                "Pick a directory to work with",
            ],
            'vulgar': [
                "Click to find your damn folder.",
                "Browse for sh*t. You know, folders and stuff.",
                "Where's your stuff? Click here to tell me.",
                "Find that folder. I believe in you.",
            ]
        },
        'start_button': {
            'normal': [
                "Start the operation",
                "Begin processing",
                "Click to start",
                "Initiate the process",
            ],
            'vulgar': [
                "Let's f*cking go!",
                "Click to make sh*t happen.",
                "Do the thing. You know what thing.",
                "Start this bad boy up!",
            ]
        },
        'stop_button': {
            'normal': [
                "Stop the current operation",
                "Cancel processing",
                "Halt the operation",
            ],
            'vulgar': [
                "STOP EVERYTHING!",
                "Abort mission!",
                "Make it stop. Please.",
            ]
        },
        'undo_button': {
            'normal': [
                "Undo the last operation",
                "Reverse the previous action",
                "Go back one step",
            ],
            'vulgar': [
                "Oh f*ck, undo that!",
                "Whoops. Let's pretend that didn't happen.",
                "Control-Z this sh*t.",
            ]
        },
    }
    
    def __init__(self, vulgar_mode: bool = False):
        """
        Initialize tooltip system.
        
        Args:
            vulgar_mode: Enable vulgar/funny tooltips
        """
        self.vulgar_mode = vulgar_mode
        logger.info(f"Tooltip system initialized (vulgar mode: {vulgar_mode})")
    
    def set_vulgar_mode(self, enabled: bool):
        """Enable or disable vulgar mode."""
        self.vulgar_mode = enabled
        logger.info(f"Vulgar tooltip mode {'enabled' if enabled else 'disabled'}")
    
    def get_tooltip(self, action: str, mode: Optional[str] = None) -> str:
        """
        Get tooltip for an action.
        
        Args:
            action: Action identifier (e.g., 'sort_button')
            mode: Override mode ('normal' or 'vulgar'), uses instance setting if None
            
        Returns:
            Random tooltip string for the action
        """
        if action not in self.TOOLTIPS:
            return ""
        
        # Determine which mode to use
        use_mode = mode if mode else ('vulgar' if self.vulgar_mode else 'normal')
        
        # Get tooltip list
        tooltips = self.TOOLTIPS[action].get(use_mode, self.TOOLTIPS[action]['normal'])
        
        # Return random tooltip
        return random.choice(tooltips)
    
    def get_all_actions(self) -> List[str]:
        """Get list of all available tooltip actions."""
        return list(self.TOOLTIPS.keys())
    
    def has_tooltip(self, action: str) -> bool:
        """Check if action has tooltips defined."""
        return action in self.TOOLTIPS

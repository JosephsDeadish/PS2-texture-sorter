"""
Sound Manager - Audio feedback system
Supports customizable sound packs and volume controls (offline using winsound)
Author: Dead On The Inside / JosephsDeadish
"""

import logging
import sys
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import threading
from enum import Enum

logger = logging.getLogger(__name__)

# Platform-specific sound imports
SOUND_AVAILABLE = False
if sys.platform == 'win32':
    try:
        import winsound
        SOUND_AVAILABLE = True
    except ImportError:
        logger.warning("winsound not available on Windows")
else:
    logger.info("Non-Windows platform - sound system disabled")


class SoundEvent(Enum):
    """Sound event types."""
    COMPLETE = "complete"
    ERROR = "error"
    ACHIEVEMENT = "achievement"
    MILESTONE = "milestone"
    WARNING = "warning"
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    STOP = "stop"
    BUTTON_CLICK = "button_click"
    NOTIFICATION = "notification"


class SoundPack(Enum):
    """Available sound packs."""
    DEFAULT = "default"
    MINIMAL = "minimal"
    VULGAR = "vulgar"


@dataclass
class Sound:
    """Represents a sound configuration."""
    event: SoundEvent
    frequency: int  # Hz (for beep sounds)
    duration: int  # milliseconds
    description: str = ""


class SoundManager:
    """Manages audio feedback with customizable sound packs."""
    
    # Default sound definitions (frequency in Hz, duration in ms)
    SOUND_DEFINITIONS = {
        SoundPack.DEFAULT: {
            SoundEvent.COMPLETE: Sound(SoundEvent.COMPLETE, 800, 200, "Task complete"),
            SoundEvent.ERROR: Sound(SoundEvent.ERROR, 300, 400, "Error occurred"),
            SoundEvent.ACHIEVEMENT: Sound(SoundEvent.ACHIEVEMENT, 1000, 150, "Achievement unlocked"),
            SoundEvent.MILESTONE: Sound(SoundEvent.MILESTONE, 900, 100, "Milestone reached"),
            SoundEvent.WARNING: Sound(SoundEvent.WARNING, 500, 200, "Warning"),
            SoundEvent.START: Sound(SoundEvent.START, 600, 150, "Processing started"),
            SoundEvent.PAUSE: Sound(SoundEvent.PAUSE, 550, 100, "Processing paused"),
            SoundEvent.RESUME: Sound(SoundEvent.RESUME, 650, 100, "Processing resumed"),
            SoundEvent.STOP: Sound(SoundEvent.STOP, 450, 200, "Processing stopped"),
            SoundEvent.BUTTON_CLICK: Sound(SoundEvent.BUTTON_CLICK, 700, 50, "Button clicked"),
            SoundEvent.NOTIFICATION: Sound(SoundEvent.NOTIFICATION, 750, 100, "Notification"),
        },
        SoundPack.MINIMAL: {
            SoundEvent.COMPLETE: Sound(SoundEvent.COMPLETE, 800, 100, "Complete"),
            SoundEvent.ERROR: Sound(SoundEvent.ERROR, 400, 200, "Error"),
            SoundEvent.ACHIEVEMENT: Sound(SoundEvent.ACHIEVEMENT, 900, 80, "Achievement"),
            SoundEvent.MILESTONE: Sound(SoundEvent.MILESTONE, 850, 80, "Milestone"),
            SoundEvent.WARNING: Sound(SoundEvent.WARNING, 500, 100, "Warning"),
            SoundEvent.START: Sound(SoundEvent.START, 600, 80, "Start"),
            SoundEvent.PAUSE: Sound(SoundEvent.PAUSE, 550, 50, "Pause"),
            SoundEvent.RESUME: Sound(SoundEvent.RESUME, 650, 50, "Resume"),
            SoundEvent.STOP: Sound(SoundEvent.STOP, 450, 100, "Stop"),
            SoundEvent.BUTTON_CLICK: Sound(SoundEvent.BUTTON_CLICK, 700, 30, "Click"),
            SoundEvent.NOTIFICATION: Sound(SoundEvent.NOTIFICATION, 750, 60, "Notification"),
        },
        SoundPack.VULGAR: {
            # Vulgar pack has more aggressive/fun sounds
            SoundEvent.COMPLETE: Sound(SoundEvent.COMPLETE, 1200, 300, "Hell yeah!"),
            SoundEvent.ERROR: Sound(SoundEvent.ERROR, 200, 600, "Oh crap!"),
            SoundEvent.ACHIEVEMENT: Sound(SoundEvent.ACHIEVEMENT, 1500, 200, "You're a legend!"),
            SoundEvent.MILESTONE: Sound(SoundEvent.MILESTONE, 1100, 150, "Keep going!"),
            SoundEvent.WARNING: Sound(SoundEvent.WARNING, 400, 300, "Watch it!"),
            SoundEvent.START: Sound(SoundEvent.START, 800, 200, "Let's go!"),
            SoundEvent.PAUSE: Sound(SoundEvent.PAUSE, 500, 150, "Hold up!"),
            SoundEvent.RESUME: Sound(SoundEvent.RESUME, 900, 150, "Back at it!"),
            SoundEvent.STOP: Sound(SoundEvent.STOP, 300, 300, "Done!"),
            SoundEvent.BUTTON_CLICK: Sound(SoundEvent.BUTTON_CLICK, 800, 60, "Click!"),
            SoundEvent.NOTIFICATION: Sound(SoundEvent.NOTIFICATION, 850, 120, "Yo!"),
        }
    }
    
    def __init__(self, sound_pack: SoundPack = SoundPack.DEFAULT):
        """
        Initialize sound manager.
        
        Args:
            sound_pack: Initial sound pack to use
        """
        self.enabled = SOUND_AVAILABLE
        self.muted = False
        self.sound_pack = sound_pack
        
        # Volume controls (0.0 to 1.0)
        self.master_volume = 1.0
        self.effects_volume = 1.0
        self.notifications_volume = 1.0
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Event callbacks (for custom sound handling)
        self.event_callbacks: Dict[SoundEvent, Callable] = {}
        
        if not self.enabled:
            logger.warning("Sound system not available on this platform")
    
    def play_sound(
        self,
        event: SoundEvent,
        async_play: bool = True,
        force: bool = False
    ) -> bool:
        """
        Play a sound for the given event.
        
        Args:
            event: Sound event to play
            async_play: Whether to play asynchronously (non-blocking)
            force: Force play even if muted
            
        Returns:
            True if sound was played
        """
        if not self.enabled:
            return False
        
        if self.muted and not force:
            logger.debug(f"Sound muted, skipping: {event.value}")
            return False
        
        # Check for custom callback
        if event in self.event_callbacks:
            try:
                self.event_callbacks[event]()
                return True
            except Exception as e:
                logger.error(f"Error in sound callback for {event.value}: {e}")
        
        # Get sound definition
        sound = self._get_sound(event)
        if not sound:
            logger.warning(f"No sound defined for event: {event.value}")
            return False
        
        # Calculate effective volume
        volume_multiplier = self._get_volume_multiplier(event)
        
        try:
            if async_play:
                # Play asynchronously in a thread
                thread = threading.Thread(
                    target=self._play_beep,
                    args=(sound, volume_multiplier),
                    daemon=True
                )
                thread.start()
            else:
                # Play synchronously
                self._play_beep(sound, volume_multiplier)
            
            logger.debug(f"Played sound: {event.value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to play sound for {event.value}: {e}")
            return False
    
    def _play_beep(self, sound: Sound, volume_multiplier: float) -> None:
        """
        Play a beep sound.
        
        Args:
            sound: Sound to play
            volume_multiplier: Volume adjustment (0.0 to 1.0)
        """
        if not SOUND_AVAILABLE or sys.platform != 'win32':
            return
        
        try:
            # Adjust frequency based on volume (limited effect with beeps)
            # Note: winsound doesn't support true volume control
            frequency = int(sound.frequency * (0.7 + 0.3 * volume_multiplier))
            duration = sound.duration
            
            with self.lock:
                winsound.Beep(frequency, duration)
                
        except Exception as e:
            logger.error(f"Error playing beep: {e}")
    
    def _get_sound(self, event: SoundEvent) -> Optional[Sound]:
        """
        Get sound definition for event.
        
        Args:
            event: Sound event
            
        Returns:
            Sound object or None
        """
        pack_sounds = self.SOUND_DEFINITIONS.get(self.sound_pack, {})
        return pack_sounds.get(event)
    
    def _get_volume_multiplier(self, event: SoundEvent) -> float:
        """
        Get effective volume multiplier for event.
        
        Args:
            event: Sound event
            
        Returns:
            Volume multiplier (0.0 to 1.0)
        """
        # Determine which volume category applies
        if event in [SoundEvent.COMPLETE, SoundEvent.START, SoundEvent.PAUSE,
                     SoundEvent.RESUME, SoundEvent.STOP]:
            category_volume = self.effects_volume
        elif event in [SoundEvent.NOTIFICATION, SoundEvent.ACHIEVEMENT,
                       SoundEvent.MILESTONE]:
            category_volume = self.notifications_volume
        else:
            category_volume = self.effects_volume
        
        return self.master_volume * category_volume
    
    def set_sound_pack(self, pack: SoundPack) -> None:
        """
        Change the active sound pack.
        
        Args:
            pack: Sound pack to use
        """
        self.sound_pack = pack
        logger.info(f"Changed sound pack to: {pack.value}")
    
    def set_master_volume(self, volume: float) -> None:
        """
        Set master volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))
        logger.debug(f"Master volume set to: {self.master_volume:.2f}")
    
    def set_effects_volume(self, volume: float) -> None:
        """
        Set effects volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.effects_volume = max(0.0, min(1.0, volume))
        logger.debug(f"Effects volume set to: {self.effects_volume:.2f}")
    
    def set_notifications_volume(self, volume: float) -> None:
        """
        Set notifications volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.notifications_volume = max(0.0, min(1.0, volume))
        logger.debug(f"Notifications volume set to: {self.notifications_volume:.2f}")
    
    def mute(self) -> None:
        """Mute all sounds."""
        self.muted = True
        logger.info("Sound muted")
    
    def unmute(self) -> None:
        """Unmute all sounds."""
        self.muted = False
        logger.info("Sound unmuted")
    
    def toggle_mute(self) -> bool:
        """
        Toggle mute state.
        
        Returns:
            New muted state
        """
        self.muted = not self.muted
        logger.info(f"Sound {'muted' if self.muted else 'unmuted'}")
        return self.muted
    
    def is_muted(self) -> bool:
        """
        Check if sound is muted.
        
        Returns:
            True if muted
        """
        return self.muted
    
    def is_available(self) -> bool:
        """
        Check if sound system is available.
        
        Returns:
            True if available
        """
        return self.enabled
    
    def register_event_callback(
        self,
        event: SoundEvent,
        callback: Callable
    ) -> None:
        """
        Register custom callback for sound event.
        
        Args:
            event: Sound event
            callback: Callback function to call instead of playing sound
        """
        self.event_callbacks[event] = callback
        logger.debug(f"Registered callback for event: {event.value}")
    
    def unregister_event_callback(self, event: SoundEvent) -> None:
        """
        Unregister callback for sound event.
        
        Args:
            event: Sound event
        """
        if event in self.event_callbacks:
            del self.event_callbacks[event]
            logger.debug(f"Unregistered callback for event: {event.value}")
    
    def play_complete(self) -> None:
        """Convenience method to play completion sound."""
        self.play_sound(SoundEvent.COMPLETE)
    
    def play_error(self) -> None:
        """Convenience method to play error sound."""
        self.play_sound(SoundEvent.ERROR)
    
    def play_achievement(self) -> None:
        """Convenience method to play achievement sound."""
        self.play_sound(SoundEvent.ACHIEVEMENT)
    
    def play_milestone(self) -> None:
        """Convenience method to play milestone sound."""
        self.play_sound(SoundEvent.MILESTONE)
    
    def play_warning(self) -> None:
        """Convenience method to play warning sound."""
        self.play_sound(SoundEvent.WARNING)
    
    def play_start(self) -> None:
        """Convenience method to play start sound."""
        self.play_sound(SoundEvent.START)
    
    def play_notification(self) -> None:
        """Convenience method to play notification sound."""
        self.play_sound(SoundEvent.NOTIFICATION)
    
    def play_sequence(
        self,
        events: list[SoundEvent],
        delay_ms: int = 100
    ) -> None:
        """
        Play a sequence of sounds with delays.
        
        Args:
            events: List of sound events to play
            delay_ms: Delay between sounds in milliseconds
        """
        def play_sequence_thread():
            import time
            for event in events:
                self.play_sound(event, async_play=False)
                time.sleep(delay_ms / 1000.0)
        
        thread = threading.Thread(target=play_sequence_thread, daemon=True)
        thread.start()
    
    def test_sound_pack(self, pack: Optional[SoundPack] = None) -> None:
        """
        Test all sounds in a sound pack.
        
        Args:
            pack: Sound pack to test (uses current if None)
        """
        if pack:
            original_pack = self.sound_pack
            self.set_sound_pack(pack)
        
        import time
        
        print(f"\nTesting sound pack: {self.sound_pack.value}")
        print("=" * 50)
        
        for event in SoundEvent:
            sound = self._get_sound(event)
            if sound:
                print(f"Playing: {event.value:20s} - {sound.description}")
                self.play_sound(event, async_play=False)
                time.sleep(0.5)
        
        print("=" * 50)
        print("Test complete!\n")
        
        if pack:
            self.set_sound_pack(original_pack)
    
    def get_available_packs(self) -> list[str]:
        """
        Get list of available sound packs.
        
        Returns:
            List of sound pack names
        """
        return [pack.value for pack in SoundPack]
    
    def get_pack_info(self, pack: SoundPack) -> Dict[str, str]:
        """
        Get information about a sound pack.
        
        Args:
            pack: Sound pack
            
        Returns:
            Dictionary with pack information
        """
        pack_sounds = self.SOUND_DEFINITIONS.get(pack, {})
        
        return {
            'name': pack.value,
            'description': self._get_pack_description(pack),
            'sound_count': len(pack_sounds),
            'events': [event.value for event in pack_sounds.keys()]
        }
    
    def _get_pack_description(self, pack: SoundPack) -> str:
        """Get description for sound pack."""
        descriptions = {
            SoundPack.DEFAULT: "Standard sound effects for all events",
            SoundPack.MINIMAL: "Quiet, subtle sound effects",
            SoundPack.VULGAR: "Fun, aggressive sound effects (opt-in)"
        }
        return descriptions.get(pack, "No description available")
    
    def get_config(self) -> Dict:
        """
        Get current sound configuration.
        
        Returns:
            Configuration dictionary
        """
        return {
            'enabled': self.enabled,
            'muted': self.muted,
            'sound_pack': self.sound_pack.value,
            'master_volume': self.master_volume,
            'effects_volume': self.effects_volume,
            'notifications_volume': self.notifications_volume
        }
    
    def apply_config(self, config: Dict) -> None:
        """
        Apply sound configuration.
        
        Args:
            config: Configuration dictionary
        """
        if 'muted' in config:
            self.muted = config['muted']
        
        if 'sound_pack' in config:
            pack_name = config['sound_pack']
            try:
                pack = SoundPack(pack_name)
                self.set_sound_pack(pack)
            except ValueError:
                logger.warning(f"Invalid sound pack: {pack_name}")
        
        if 'master_volume' in config:
            self.set_master_volume(config['master_volume'])
        
        if 'effects_volume' in config:
            self.set_effects_volume(config['effects_volume'])
        
        if 'notifications_volume' in config:
            self.set_notifications_volume(config['notifications_volume'])
        
        logger.info("Applied sound configuration")


# Convenience function for quick sound playing
def play_sound(event: SoundEvent, sound_manager: Optional[SoundManager] = None) -> None:
    """
    Quick function to play a sound.
    
    Args:
        event: Sound event to play
        sound_manager: Optional sound manager instance (creates new if None)
    """
    if sound_manager is None:
        sound_manager = SoundManager()
    
    sound_manager.play_sound(event)

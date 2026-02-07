"""
Panda Mode - Fun animations and quotes during processing
Random panda facts, progress celebrations, and Easter eggs
Author: Dead On The Inside / JosephsDeadish
"""

import logging
import random
from typing import List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import threading
import time

logger = logging.getLogger(__name__)


class PandaMood(Enum):
    """Panda mood states."""
    HAPPY = "happy"
    EXCITED = "excited"
    WORKING = "working"
    TIRED = "tired"
    CELEBRATING = "celebrating"
    SLEEPING = "sleeping"


@dataclass
class PandaAnimation:
    """Represents a panda animation frame sequence."""
    name: str
    frames: List[str]
    duration_ms: int = 200
    loop: bool = False


class PandaMode:
    """Manages panda animations, facts, and Easter eggs."""
    
    # Panda ASCII art frames
    PANDA_FRAMES = {
        'idle': [
            """
    ∩＿＿∩
    |ノ　　　　ヽ
   /　●　　● |
  |　　　( _●_) ミ
 彡､　　　|∪| ､｀＼
/　＿＿ ヽノ /´>　)
(＿＿＿）　　/ (_／
 |　　　　　　　|
 | ／＼　　　　|
 | /　　　)　　　|
 ∪　　（　　　＼
　　　　　＼＿＿)
            """,
        ],
        'working': [
            """
    ∩＿＿∩
    |ノ　　　　ヽ
   /　●　　● |  💻
  |　　　( _●_) ミ
 彡､　　　|∪| ､｀＼
/　＿＿ ヽノ /´>　)
            """,
            """
    ∩＿＿∩
    |ノ　　　　ヽ  💻
   /　●　　● |
  |　　　( _●_) ミ
 彡､　　　|∪| ､｀＼
/　＿＿ ヽノ /´>　)
            """,
        ],
        'celebrating': [
            """
    ∩＿＿∩
    |ノ　　　　ヽ
   /　◕　　◕ |  🎉
  |　　　( _●_) ミ
 彡､　　　|∪| ､｀＼  ✨
/　＿＿ ヽノ /´>　)
            """,
        ],
        'sleeping': [
            """
    ∩＿＿∩
    |ノ　　　　ヽ
   /　－　　－ |  💤
  |　　　( _●_) ミ
 彡､　　　|∪| ､｀＼
/　＿＿ ヽノ /´>　)
            """,
        ],
    }
    
    # Panda facts
    PANDA_FACTS = [
        "Pandas eat for about 12 hours a day! 🎋",
        "A panda's paw has six digits—five fingers and a thumb!",
        "Giant pandas are excellent tree climbers. 🌲",
        "Pandas communicate through various vocalizations and scent marking.",
        "Baby pandas are about the size of a stick of butter when born!",
        "Pandas have been on Earth for 2-3 million years.",
        "An adult panda can eat 12-38kg of bamboo per day!",
        "Pandas spend 14-16 hours a day eating.",
        "The black patches on a panda's eyes may help them recognize each other.",
        "Pandas are solitary animals by nature. 🐼",
        "A panda's digestive system is actually designed for meat, not bamboo!",
        "Pandas can swim and have been known to enjoy water.",
        "The red panda is not actually related to the giant panda!",
        "Pandas have lived on Earth for about 8 million years.",
        "A panda's bite is almost as strong as a jaguar's!",
    ]
    
    # Regular motivational quotes
    REGULAR_QUOTES = [
        "Great progress! Keep going! 🚀",
        "You're doing amazing! ⭐",
        "Texture sorting like a pro! 💪",
        "Smooth as bamboo! 🎋",
        "Outstanding work! 🌟",
        "Almost there, keep it up! 💯",
        "Fantastic job! 🎉",
        "You're on fire! 🔥",
        "Incredible progress! 👏",
        "Master sorter in action! 👑",
        "Crushing it! 💥",
        "Stellar performance! ⭐",
        "Keep up the great work! 💪",
        "You're unstoppable! 🚀",
        "Excellent sorting! ✨",
    ]
    
    # Vulgar mode quotes (opt-in, funny but edgy)
    VULGAR_QUOTES = [
        "Holy sh*t, you're fast! 🔥",
        "Damn, you're good at this! 💯",
        "F*ck yeah, great progress! 🎉",
        "Badass sorting skills! 💪",
        "Hell yeah, keep crushing it! 💥",
        "That's f*cking impressive! ⭐",
        "Damn son, slow down! 🚀",
        "You're a f*cking legend! 👑",
        "Holy crap, almost done! 🎯",
        "Sh*t yeah, excellent work! ✨",
        "Damn right, you're killing it! 💀",
        "F*ck me, that's fast! ⚡",
        "Badass texture ninja! 🥷",
        "Goddamn professional! 💼",
        "Beast mode activated! 🦁",
    ]
    
    # Milestone messages
    MILESTONE_MESSAGES = {
        10: "10 textures sorted! You're getting started! 🌱",
        50: "50 textures! You're getting the hang of it! 💚",
        100: "100 textures! Century mark! 💯",
        500: "500 textures! Half a thousand! 🎯",
        1000: "1,000 textures! That's a milestone! 🏆",
        5000: "5,000 textures! You're unstoppable! 🚀",
        10000: "10,000 textures! TEN THOUSAND! 🌟",
        25000: "25,000 textures! Quarter way to 100K! ⭐",
        50000: "50,000 textures! FIFTY THOUSAND! 👑",
        100000: "100,000 textures! ONE HUNDRED THOUSAND! 💎",
        200000: "200,000 textures! LEGENDARY STATUS! 🏆✨",
    }
    
    # Easter egg triggers
    EASTER_EGGS = {
        'konami': '🎮 Up, Up, Down, Down, Left, Right, Left, Right, B, A, Start!',
        'bamboo': '🎋 Unlimited bamboo mode activated!',
        'ninja': '🥷 Stealth sorting engaged!',
        'turbo': '⚡ TURBO MODE ENGAGED!',
        'disco': '🕺 Disco panda mode!',
    }
    
    def __init__(self, vulgar_mode: bool = False):
        """
        Initialize panda mode.
        
        Args:
            vulgar_mode: Enable vulgar/funny quotes (opt-in)
        """
        self.enabled = True
        self.vulgar_mode = vulgar_mode
        self.current_mood = PandaMood.HAPPY
        self.animation_thread: Optional[threading.Thread] = None
        self.stop_animation = threading.Event()
        
        # Callbacks for animation updates
        self.animation_callbacks: List[Callable[[str], None]] = []
        self.message_callbacks: List[Callable[[str], None]] = []
        
        # Statistics
        self.facts_shown = 0
        self.quotes_shown = 0
        self.easter_eggs_triggered: set = set()
        
        logger.info("🐼 Panda Mode initialized" + (" [VULGAR]" if vulgar_mode else ""))
    
    def enable(self) -> None:
        """Enable panda mode."""
        self.enabled = True
        logger.info("🐼 Panda Mode enabled")
    
    def disable(self) -> None:
        """Disable panda mode."""
        self.enabled = False
        self.stop_animation.set()
        logger.info("Panda Mode disabled")
    
    def toggle(self) -> bool:
        """
        Toggle panda mode.
        
        Returns:
            New enabled state
        """
        if self.enabled:
            self.disable()
        else:
            self.enable()
        return self.enabled
    
    def set_vulgar_mode(self, enabled: bool) -> None:
        """
        Enable or disable vulgar mode.
        
        Args:
            enabled: Whether to enable vulgar mode
        """
        self.vulgar_mode = enabled
        logger.info(f"Vulgar mode {'enabled' if enabled else 'disabled'}")
    
    def set_mood(self, mood: PandaMood) -> None:
        """
        Set panda mood.
        
        Args:
            mood: Panda mood state
        """
        self.current_mood = mood
        logger.debug(f"Panda mood: {mood.value}")
    
    def get_random_fact(self) -> str:
        """
        Get a random panda fact.
        
        Returns:
            Random panda fact
        """
        if not self.enabled:
            return ""
        
        fact = random.choice(self.PANDA_FACTS)
        self.facts_shown += 1
        logger.debug("Showing panda fact")
        return fact
    
    def get_random_quote(self) -> str:
        """
        Get a random motivational quote.
        
        Returns:
            Random quote (vulgar or regular based on mode)
        """
        if not self.enabled:
            return ""
        
        if self.vulgar_mode:
            quote = random.choice(self.VULGAR_QUOTES)
        else:
            quote = random.choice(self.REGULAR_QUOTES)
        
        self.quotes_shown += 1
        return quote
    
    def get_milestone_message(self, count: int) -> Optional[str]:
        """
        Get milestone message for texture count.
        
        Args:
            count: Number of textures processed
            
        Returns:
            Milestone message or None
        """
        if not self.enabled:
            return None
        
        # Check if this count hits a milestone
        if count in self.MILESTONE_MESSAGES:
            return self.MILESTONE_MESSAGES[count]
        
        return None
    
    def get_animation_frame(self, animation_name: str = 'idle') -> str:
        """
        Get current animation frame.
        
        Args:
            animation_name: Name of animation to get
            
        Returns:
            Animation frame as string
        """
        if not self.enabled:
            return ""
        
        frames = self.PANDA_FRAMES.get(animation_name, self.PANDA_FRAMES['idle'])
        
        # For multi-frame animations, rotate through frames
        # In a real implementation, this would track frame index
        return random.choice(frames)
    
    def start_animation(
        self,
        animation_name: str = 'working',
        duration_seconds: Optional[float] = None
    ) -> None:
        """
        Start animated panda display.
        
        Args:
            animation_name: Name of animation to play
            duration_seconds: How long to animate (None for indefinite)
        """
        if not self.enabled:
            return
        
        # Stop any existing animation
        self.stop_current_animation()
        
        self.stop_animation.clear()
        
        def animate():
            frames = self.PANDA_FRAMES.get(animation_name, self.PANDA_FRAMES['idle'])
            frame_idx = 0
            start_time = time.time()
            
            while not self.stop_animation.is_set():
                # Check duration
                if duration_seconds and (time.time() - start_time) > duration_seconds:
                    break
                
                # Get current frame
                frame = frames[frame_idx % len(frames)]
                
                # Notify callbacks
                self._notify_animation_update(frame)
                
                # Next frame
                frame_idx += 1
                
                # Sleep between frames
                time.sleep(0.2)  # 200ms per frame
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def stop_current_animation(self) -> None:
        """Stop current animation."""
        if self.animation_thread and self.animation_thread.is_alive():
            self.stop_animation.set()
            self.animation_thread.join(timeout=1.0)
    
    def celebrate(self, message: Optional[str] = None) -> None:
        """
        Trigger celebration animation.
        
        Args:
            message: Optional celebration message
        """
        if not self.enabled:
            return
        
        self.set_mood(PandaMood.CELEBRATING)
        self.start_animation('celebrating', duration_seconds=3.0)
        
        if not message:
            message = self.get_random_quote()
        
        self._notify_message(f"🎉 {message}")
        logger.info(f"🐼 Celebration: {message}")
    
    def show_progress_update(self, processed: int, total: int) -> None:
        """
        Show progress update with panda.
        
        Args:
            processed: Number of textures processed
            total: Total textures to process
        """
        if not self.enabled:
            return
        
        # Check for milestones
        milestone_msg = self.get_milestone_message(processed)
        if milestone_msg:
            self.celebrate(milestone_msg)
            return
        
        # Random facts/quotes at intervals
        if processed % 100 == 0 and processed > 0:
            if random.random() < 0.3:  # 30% chance
                self._notify_message(self.get_random_fact())
            elif random.random() < 0.5:  # 50% of remaining
                self._notify_message(self.get_random_quote())
    
    def trigger_easter_egg(self, egg_name: str) -> bool:
        """
        Trigger an Easter egg.
        
        Args:
            egg_name: Name of Easter egg to trigger
            
        Returns:
            True if triggered successfully
        """
        if not self.enabled:
            return False
        
        if egg_name not in self.EASTER_EGGS:
            return False
        
        self.easter_eggs_triggered.add(egg_name)
        message = self.EASTER_EGGS[egg_name]
        
        self.celebrate(message)
        logger.info(f"🥚 Easter egg triggered: {egg_name}")
        
        return True
    
    def check_konami_code(self, input_sequence: List[str]) -> bool:
        """
        Check if input matches Konami code.
        
        Args:
            input_sequence: List of key inputs
            
        Returns:
            True if Konami code matched
        """
        konami = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a']
        
        if input_sequence[-len(konami):] == konami:
            return self.trigger_easter_egg('konami')
        
        return False
    
    def get_panda_status(self) -> str:
        """
        Get current panda status message.
        
        Returns:
            Status message with panda mood
        """
        if not self.enabled:
            return "Panda Mode: Disabled"
        
        mood_messages = {
            PandaMood.HAPPY: "🐼 Panda is happy and ready!",
            PandaMood.EXCITED: "🐼 Panda is excited to help!",
            PandaMood.WORKING: "🐼 Panda is hard at work!",
            PandaMood.TIRED: "🐼 Panda is getting tired...",
            PandaMood.CELEBRATING: "🐼 Panda is celebrating! 🎉",
            PandaMood.SLEEPING: "🐼 Panda is taking a nap... 💤",
        }
        
        return mood_messages.get(self.current_mood, "🐼 Panda is here!")
    
    def register_animation_callback(self, callback: Callable[[str], None]) -> None:
        """
        Register callback for animation frame updates.
        
        Args:
            callback: Function to call with animation frame
        """
        self.animation_callbacks.append(callback)
    
    def register_message_callback(self, callback: Callable[[str], None]) -> None:
        """
        Register callback for panda messages.
        
        Args:
            callback: Function to call with messages
        """
        self.message_callbacks.append(callback)
    
    def _notify_animation_update(self, frame: str) -> None:
        """Notify animation callbacks."""
        for callback in self.animation_callbacks:
            try:
                callback(frame)
            except Exception as e:
                logger.error(f"Error in animation callback: {e}")
    
    def _notify_message(self, message: str) -> None:
        """Notify message callbacks."""
        for callback in self.message_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in message callback: {e}")
    
    def get_statistics(self) -> dict:
        """
        Get panda mode statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            'enabled': self.enabled,
            'vulgar_mode': self.vulgar_mode,
            'current_mood': self.current_mood.value,
            'facts_shown': self.facts_shown,
            'quotes_shown': self.quotes_shown,
            'easter_eggs_triggered': len(self.easter_eggs_triggered),
            'easter_eggs_list': list(self.easter_eggs_triggered)
        }
    
    def reset_statistics(self) -> None:
        """Reset panda mode statistics."""
        self.facts_shown = 0
        self.quotes_shown = 0
        self.easter_eggs_triggered.clear()
        logger.info("Panda mode statistics reset")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop_current_animation()


# Convenience functions
def create_panda_mode(vulgar: bool = False) -> PandaMode:
    """
    Create a PandaMode instance.
    
    Args:
        vulgar: Enable vulgar mode
        
    Returns:
        PandaMode instance
    """
    return PandaMode(vulgar_mode=vulgar)


def get_random_panda_fact() -> str:
    """
    Get a random panda fact (convenience function).
    
    Returns:
        Random panda fact
    """
    return random.choice(PandaMode.PANDA_FACTS)

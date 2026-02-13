"""
Damage System - Comprehensive damage tracking with visual effects
Author: Dead On The Inside / JosephsDeadish
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set

logger = logging.getLogger(__name__)


class DamageCategory(Enum):
    """Categories of damage with distinct visual effects."""
    SHARP = "sharp"  # Swords, knives - causes bleeding and gashes
    BLUNT = "blunt"  # Hammers, clubs - causes bruising and swelling
    ARROW = "arrow"  # Arrows - stick in body
    BULLET = "bullet"  # Bullets - create holes
    FIRE = "fire"  # Fire magic
    ICE = "ice"  # Ice magic
    LIGHTNING = "lightning"  # Lightning magic
    POISON = "poison"  # Poison damage
    ACID = "acid"  # Acid damage
    HOLY = "holy"  # Holy magic
    DARK = "dark"  # Dark magic
    EXPLOSION = "explosion"  # Explosive damage


class LimbType(Enum):
    """Body parts that can be damaged or severed."""
    HEAD = "head"
    TORSO = "torso"
    LEFT_ARM = "left_arm"
    RIGHT_ARM = "right_arm"
    LEFT_LEG = "left_leg"
    RIGHT_LEG = "right_leg"


@dataclass
class DamageStage:
    """Represents a stage of damage progression (1-12)."""
    stage: int  # 1-12, higher = worse
    description: str
    visual_effect: str  # Description of visual effect
    movement_penalty: float = 0.0  # Speed reduction (0.0 = none, 1.0 = immobile)
    attack_penalty: float = 0.0  # Attack power reduction


@dataclass
class LimbDamage:
    """Tracks damage to a specific limb."""
    limb: LimbType
    category: DamageCategory
    stage: int = 0  # 0-12, 0 = no damage
    severed: bool = False
    bleeding_rate: float = 0.0  # Blood loss per second
    visual_effects: List[str] = field(default_factory=list)
    
    def get_penalty(self) -> Tuple[float, float]:
        """Get movement and attack penalties for this limb damage."""
        if self.severed:
            if self.limb in [LimbType.LEFT_LEG, LimbType.RIGHT_LEG]:
                return (0.5, 0.0)  # Severed leg = 50% slower
            elif self.limb in [LimbType.LEFT_ARM, LimbType.RIGHT_ARM]:
                return (0.0, 0.5)  # Severed arm = 50% weaker attacks
            elif self.limb == LimbType.HEAD:
                return (1.0, 1.0)  # Decapitated = dead
        
        # Progressive penalties based on stage
        movement_penalty = min(0.8, self.stage * 0.05)
        attack_penalty = min(0.8, self.stage * 0.05)
        return (movement_penalty, attack_penalty)


@dataclass
class ProjectileStuck:
    """Represents a projectile stuck in body (arrow, bolt, etc)."""
    projectile_type: str  # "arrow", "bolt", "spear"
    position: Tuple[int, int]  # X, Y position on body
    limb: LimbType
    damage_per_second: float = 0.5  # Continuous damage
    creation_time: float = field(default_factory=time.time)


@dataclass
class VisualWound:
    """Visual representation of a wound."""
    wound_type: str  # "gash", "bruise", "hole", "burn", "scar"
    position: Tuple[int, int]
    size: int  # Pixels
    severity: int  # 1-12
    color: str  # Hex color
    limb: LimbType
    creation_time: float = field(default_factory=time.time)


class DamageTracker:
    """Tracks all damage effects on an entity."""
    
    # Define visual effects for each damage type and stage
    DAMAGE_STAGES: Dict[DamageCategory, List[DamageStage]] = {
        DamageCategory.SHARP: [
            DamageStage(1, "Minor scratch", "small_cut", 0.0, 0.0),
            DamageStage(2, "Shallow cut", "cut_bleeding", 0.05, 0.0),
            DamageStage(3, "Deep cut", "deep_gash", 0.05, 0.05),
            DamageStage(4, "Severe gash", "severe_gash_bleeding", 0.10, 0.05),
            DamageStage(5, "Multiple gashes", "multiple_gashes", 0.10, 0.10),
            DamageStage(6, "Deep lacerations", "deep_lacerations", 0.15, 0.10),
            DamageStage(7, "Arterial bleeding", "arterial_bleeding", 0.20, 0.15),
            DamageStage(8, "Massive gaping wound", "massive_wound", 0.25, 0.15),
            DamageStage(9, "Exposed bone", "exposed_bone", 0.30, 0.20),
            DamageStage(10, "Limb barely attached", "limb_hanging", 0.40, 0.25),
            DamageStage(11, "Limb critical", "limb_critical", 0.50, 0.30),
            DamageStage(12, "Limb severed", "severed", 1.0, 0.5),
        ],
        DamageCategory.BLUNT: [
            DamageStage(1, "Minor bruise", "small_bruise", 0.0, 0.0),
            DamageStage(2, "Bruise", "bruise", 0.0, 0.0),
            DamageStage(3, "Large bruise", "large_bruise", 0.05, 0.0),
            DamageStage(4, "Swelling", "swelling", 0.05, 0.05),
            DamageStage(5, "Severe swelling", "severe_swelling", 0.10, 0.05),
            DamageStage(6, "Internal bleeding", "internal_bleeding", 0.15, 0.10),
            DamageStage(7, "Fractured bone", "fracture", 0.20, 0.15),
            DamageStage(8, "Broken bone", "broken_bone", 0.30, 0.20),
            DamageStage(9, "Shattered bone", "shattered_bone", 0.40, 0.25),
            DamageStage(10, "Multiple fractures", "multiple_fractures", 0.50, 0.30),
            DamageStage(11, "Crushed limb", "crushed_limb", 0.70, 0.40),
            DamageStage(12, "Pulverized", "pulverized", 1.0, 0.5),
        ],
    }
    
    def __init__(self):
        """Initialize damage tracker."""
        self.limb_damage: Dict[LimbType, List[LimbDamage]] = {
            limb: [] for limb in LimbType
        }
        self.stuck_projectiles: List[ProjectileStuck] = []
        self.visual_wounds: List[VisualWound] = []
        self.total_bleeding_rate: float = 0.0
        self.severed_limbs: Set[LimbType] = set()
        
    def apply_damage(self, limb: LimbType, category: DamageCategory, 
                    amount: int, can_sever: bool = False) -> Dict:
        """
        Apply damage to a limb.
        
        Args:
            limb: Which limb was hit
            category: Type of damage
            amount: Damage amount (influences stage progression)
            can_sever: Whether this hit can sever the limb (critical hit)
            
        Returns:
            Dict with damage info (stage, severed, etc.)
        """
        # Find existing damage on this limb of this category
        existing = None
        for dmg in self.limb_damage[limb]:
            if dmg.category == category:
                existing = dmg
                break
        
        if existing is None:
            existing = LimbDamage(limb=limb, category=category, stage=0)
            self.limb_damage[limb].append(existing)
        
        # Progress damage stage based on amount
        stage_progression = max(1, amount // 10)  # 10 damage = 1 stage
        existing.stage = min(12, existing.stage + stage_progression)
        
        # Check for severing (critical hits at high damage stages)
        if can_sever and existing.stage >= 11 and category == DamageCategory.SHARP:
            existing.severed = True
            self.severed_limbs.add(limb)
            logger.info(f"Limb {limb.value} severed!")
        
        # Update bleeding rate for sharp damage
        if category == DamageCategory.SHARP:
            existing.bleeding_rate = existing.stage * 0.5
            self._update_total_bleeding()
        
        # Add visual wound
        self._add_visual_wound(limb, category, existing.stage)
        
        return {
            'limb': limb.value,
            'category': category.value,
            'stage': existing.stage,
            'severed': existing.severed,
            'description': self._get_stage_description(category, existing.stage)
        }
    
    def add_stuck_projectile(self, projectile_type: str, position: Tuple[int, int], 
                            limb: LimbType) -> ProjectileStuck:
        """Add a projectile stuck in the body."""
        projectile = ProjectileStuck(
            projectile_type=projectile_type,
            position=position,
            limb=limb
        )
        self.stuck_projectiles.append(projectile)
        logger.info(f"{projectile_type} stuck in {limb.value}")
        return projectile
    
    def get_movement_penalty(self) -> float:
        """Calculate total movement penalty from all damage."""
        total_penalty = 0.0
        for limb_damages in self.limb_damage.values():
            for damage in limb_damages:
                move_penalty, _ = damage.get_penalty()
                total_penalty += move_penalty
        return min(1.0, total_penalty)
    
    def get_attack_penalty(self) -> float:
        """Calculate total attack penalty from all damage."""
        total_penalty = 0.0
        for limb_damages in self.limb_damage.values():
            for damage in limb_damages:
                _, attack_penalty = damage.get_penalty()
                total_penalty += attack_penalty
        return min(1.0, total_penalty)
    
    def is_limb_severed(self, limb: LimbType) -> bool:
        """Check if a limb is severed."""
        return limb in self.severed_limbs
    
    def is_decapitated(self) -> bool:
        """Check if head is severed (instant death)."""
        return LimbType.HEAD in self.severed_limbs
    
    def get_damage_stage(self, limb: LimbType, category: DamageCategory) -> int:
        """Get damage stage for specific limb and category."""
        for damage in self.limb_damage[limb]:
            if damage.category == category:
                return damage.stage
        return 0
    
    def get_all_wounds(self) -> List[VisualWound]:
        """Get all visual wounds for rendering."""
        return self.visual_wounds
    
    def get_stuck_projectiles(self) -> List[ProjectileStuck]:
        """Get all stuck projectiles for rendering."""
        return self.stuck_projectiles
    
    def _add_visual_wound(self, limb: LimbType, category: DamageCategory, stage: int):
        """Add a visual wound representation."""
        # Determine wound appearance based on category
        wound_map = {
            DamageCategory.SHARP: ("gash", "#8B0000"),
            DamageCategory.BLUNT: ("bruise", "#4B0082"),
            DamageCategory.BULLET: ("hole", "#000000"),
            DamageCategory.FIRE: ("burn", "#FF4500"),
            DamageCategory.ICE: ("frostbite", "#00BFFF"),
            DamageCategory.LIGHTNING: ("burn", "#FFD700"),
        }
        
        wound_type, color = wound_map.get(category, ("wound", "#FF0000"))
        
        # Size increases with stage
        size = 5 + (stage * 3)
        
        # Random position variation (would be based on actual hit location)
        import random
        position = (random.randint(-20, 20), random.randint(-20, 20))
        
        wound = VisualWound(
            wound_type=wound_type,
            position=position,
            size=size,
            severity=stage,
            color=color,
            limb=limb
        )
        self.visual_wounds.append(wound)
    
    def _update_total_bleeding(self):
        """Update total bleeding rate from all wounds."""
        self.total_bleeding_rate = 0.0
        for limb_damages in self.limb_damage.values():
            for damage in limb_damages:
                if damage.category == DamageCategory.SHARP:
                    self.total_bleeding_rate += damage.bleeding_rate
    
    def _get_stage_description(self, category: DamageCategory, stage: int) -> str:
        """Get description for damage stage."""
        if category in self.DAMAGE_STAGES:
            stages = self.DAMAGE_STAGES[category]
            if 0 < stage <= len(stages):
                return stages[stage - 1].description
        return f"Stage {stage} damage"
    
    def update(self, delta_time: float) -> float:
        """
        Update damage over time (bleeding, poison, etc).
        
        Args:
            delta_time: Time since last update in seconds
            
        Returns:
            Damage taken this update
        """
        damage_taken = 0.0
        
        # Apply bleeding damage
        if self.total_bleeding_rate > 0:
            damage_taken += self.total_bleeding_rate * delta_time
        
        # Apply damage from stuck projectiles
        for projectile in self.stuck_projectiles:
            damage_taken += projectile.damage_per_second * delta_time
        
        return damage_taken
    
    def clear_all(self):
        """Clear all damage (for respawn/healing)."""
        self.limb_damage = {limb: [] for limb in LimbType}
        self.stuck_projectiles.clear()
        self.visual_wounds.clear()
        self.total_bleeding_rate = 0.0
        self.severed_limbs.clear()

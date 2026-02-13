"""
Projectile System - Physics-based projectiles with collision detection
Author: Dead On The Inside / JosephsDeadish
"""

import logging
import math
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Callable, List

logger = logging.getLogger(__name__)


class ProjectileType(Enum):
    """Types of projectiles."""
    ARROW = "arrow"
    BULLET = "bullet"
    BOLT = "bolt"  # Crossbow bolt
    FIREBALL = "fireball"
    ICE_SHARD = "ice_shard"
    LIGHTNING_BOLT = "lightning_bolt"
    ROCK = "rock"
    SPEAR = "spear"


@dataclass
class ProjectilePhysics:
    """Physics properties for a projectile."""
    speed: float = 500.0  # Pixels per second
    gravity: float = 200.0  # Downward acceleration (pixels/s^2)
    air_resistance: float = 0.98  # Velocity multiplier per frame (1.0 = no resistance)
    piercing: bool = False  # Can pass through targets
    bouncy: bool = False  # Bounces off walls
    bounce_damping: float = 0.7  # Energy retained on bounce


class Projectile:
    """A physics-based projectile with collision detection."""
    
    def __init__(self, x: float, y: float, angle: float, 
                 projectile_type: ProjectileType,
                 damage: int,
                 physics: Optional[ProjectilePhysics] = None,
                 owner = None,
                 on_hit: Optional[Callable] = None,
                 icon: str = "•"):
        """
        Initialize projectile.
        
        Args:
            x: Starting X position
            y: Starting Y position
            angle: Launch angle in radians (0 = right, pi/2 = down)
            projectile_type: Type of projectile
            damage: Damage dealt on hit
            physics: Physics properties (uses defaults if None)
            owner: Who fired the projectile (for friendly fire checks)
            on_hit: Callback when projectile hits (receives target)
            icon: Visual representation (emoji or symbol)
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.projectile_type = projectile_type
        self.damage = damage
        self.physics = physics or ProjectilePhysics()
        self.owner = owner
        self.on_hit_callback = on_hit
        self.icon = icon
        
        # Velocity components
        self.vx = math.cos(angle) * self.physics.speed
        self.vy = math.sin(angle) * self.physics.speed
        
        # State
        self.active = True
        self.stuck = False  # Stuck in target
        self.stuck_target = None
        self.distance_traveled = 0.0
        self.creation_time = time.time()
        
        # Trail effect (for rendering)
        self.trail_positions: List[Tuple[float, float]] = []
        self.max_trail_length = 5
    
    def update(self, delta_time: float) -> bool:
        """
        Update projectile physics.
        
        Args:
            delta_time: Time since last update (seconds)
            
        Returns:
            True if still active, False if should be removed
        """
        if not self.active or self.stuck:
            return self.active
        
        # Store trail position
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        
        # Apply gravity
        self.vy += self.physics.gravity * delta_time
        
        # Apply air resistance
        self.vx *= self.physics.air_resistance
        self.vy *= self.physics.air_resistance
        
        # Update position
        old_x, old_y = self.x, self.y
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
        # Track distance
        dx = self.x - old_x
        dy = self.y - old_y
        self.distance_traveled += math.sqrt(dx*dx + dy*dy)
        
        # Update angle based on velocity (projectile rotates to face direction)
        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            self.angle = math.atan2(self.vy, self.vx)
        
        return self.active
    
    def check_collision_point(self, target_x: float, target_y: float, 
                              radius: float) -> bool:
        """
        Check collision with a circular target.
        
        Args:
            target_x: Target center X
            target_y: Target center Y
            radius: Target radius
            
        Returns:
            True if collision detected
        """
        dx = self.x - target_x
        dy = self.y - target_y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < radius
    
    def check_collision_rect(self, rect_x: float, rect_y: float,
                             width: float, height: float) -> bool:
        """
        Check collision with rectangular target.
        
        Args:
            rect_x: Rectangle left edge
            rect_y: Rectangle top edge
            width: Rectangle width
            height: Rectangle height
            
        Returns:
            True if collision detected
        """
        return (rect_x <= self.x <= rect_x + width and 
                rect_y <= self.y <= rect_y + height)
    
    def on_hit(self, target, limb: Optional[str] = None):
        """
        Handle hitting a target.
        
        Args:
            target: What was hit
            limb: Which limb was hit (if applicable)
        """
        logger.info(f"Projectile {self.projectile_type.value} hit target!")
        
        # Call callback if provided
        if self.on_hit_callback:
            self.on_hit_callback(target, self, limb)
        
        # Stick in target for certain projectile types
        if self.projectile_type in [ProjectileType.ARROW, ProjectileType.BOLT, 
                                    ProjectileType.SPEAR]:
            self.stuck = True
            self.stuck_target = target
            logger.info(f"{self.projectile_type.value} stuck in target!")
        else:
            # Other projectiles disappear on hit
            if not self.physics.piercing:
                self.active = False
    
    def on_wall_collision(self, wall_normal: Tuple[float, float]):
        """
        Handle collision with wall/boundary.
        
        Args:
            wall_normal: Normal vector of wall (for bounce calculation)
        """
        if self.physics.bouncy:
            # Reflect velocity
            nx, ny = wall_normal
            dot = self.vx * nx + self.vy * ny
            self.vx = (self.vx - 2 * dot * nx) * self.physics.bounce_damping
            self.vy = (self.vy - 2 * dot * ny) * self.physics.bounce_damping
            logger.debug("Projectile bounced")
        else:
            # Projectile stops on wall hit
            self.active = False
            logger.debug("Projectile hit wall")
    
    def get_position(self) -> Tuple[float, float]:
        """Get current position."""
        return (self.x, self.y)
    
    def get_velocity(self) -> Tuple[float, float]:
        """Get current velocity."""
        return (self.vx, self.vy)
    
    def deactivate(self):
        """Deactivate the projectile."""
        self.active = False


class ProjectileManager:
    """Manages multiple active projectiles."""
    
    def __init__(self):
        """Initialize projectile manager."""
        self.projectiles: List[Projectile] = []
    
    def spawn_projectile(self, x: float, y: float, angle: float,
                        projectile_type: ProjectileType, damage: int,
                        physics: Optional[ProjectilePhysics] = None,
                        owner = None, on_hit: Optional[Callable] = None,
                        icon: str = None) -> Projectile:
        """
        Spawn a new projectile.
        
        Args:
            x: Starting X
            y: Starting Y
            angle: Launch angle (radians)
            projectile_type: Type of projectile
            damage: Damage dealt
            physics: Physics properties
            owner: Who fired it
            on_hit: Hit callback
            icon: Visual representation
            
        Returns:
            The created projectile
        """
        # Default icons for projectile types
        if icon is None:
            icon_map = {
                ProjectileType.ARROW: "➤",
                ProjectileType.BULLET: "•",
                ProjectileType.BOLT: "⟶",
                ProjectileType.FIREBALL: "🔥",
                ProjectileType.ICE_SHARD: "❄️",
                ProjectileType.LIGHTNING_BOLT: "⚡",
                ProjectileType.ROCK: "🪨",
                ProjectileType.SPEAR: "🗡️",
            }
            icon = icon_map.get(projectile_type, "•")
        
        projectile = Projectile(
            x, y, angle, projectile_type, damage, physics,
            owner, on_hit, icon
        )
        self.projectiles.append(projectile)
        logger.info(f"Spawned {projectile_type.value} projectile")
        return projectile
    
    def update(self, delta_time: float):
        """Update all projectiles."""
        # Update each projectile
        for projectile in self.projectiles[:]:
            if not projectile.update(delta_time):
                # Remove inactive projectiles
                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)
    
    def check_collisions(self, targets: List, get_position_func: Callable,
                        get_radius_func: Callable, on_hit_func: Callable):
        """
        Check collisions between projectiles and targets.
        
        Args:
            targets: List of potential targets
            get_position_func: Function to get target position (x, y)
            get_radius_func: Function to get target collision radius
            on_hit_func: Function called on hit (target, projectile)
        """
        for projectile in self.projectiles[:]:
            if not projectile.active or projectile.stuck:
                continue
            
            for target in targets:
                # Skip if projectile owner is target (no self-damage)
                if projectile.owner == target:
                    continue
                
                # Get target info
                target_x, target_y = get_position_func(target)
                target_radius = get_radius_func(target)
                
                # Check collision
                if projectile.check_collision_point(target_x, target_y, target_radius):
                    # Hit detected!
                    projectile.on_hit(target)
                    on_hit_func(target, projectile)
                    
                    # Remove if not piercing
                    if not projectile.physics.piercing and projectile in self.projectiles:
                        if not projectile.stuck:  # Don't remove stuck projectiles yet
                            self.projectiles.remove(projectile)
                    break
    
    def get_active_projectiles(self) -> List[Projectile]:
        """Get list of active projectiles."""
        return [p for p in self.projectiles if p.active]
    
    def clear_all(self):
        """Remove all projectiles."""
        self.projectiles.clear()
    
    def get_projectiles_by_owner(self, owner) -> List[Projectile]:
        """Get projectiles fired by specific owner."""
        return [p for p in self.projectiles if p.owner == owner]

#!/usr/bin/env python3
"""
Test damage and projectile systems.
"""

import sys
import math
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.features.damage_system import (
    DamageCategory, DamageTracker, LimbType, DamageStage
)
from src.features.projectile_system import (
    Projectile, ProjectileType, ProjectilePhysics, ProjectileManager
)


def test_damage_tracker_creation():
    """Test creating damage tracker."""
    tracker = DamageTracker()
    assert tracker is not None
    assert len(tracker.limb_damage) == len(LimbType)
    assert tracker.total_bleeding_rate == 0.0
    print("✓ Damage tracker creation works")


def test_apply_sharp_damage():
    """Test applying sharp weapon damage."""
    tracker = DamageTracker()
    
    # Apply damage to arm
    result = tracker.apply_damage(LimbType.LEFT_ARM, DamageCategory.SHARP, 25)
    
    assert result['limb'] == 'left_arm'
    assert result['category'] == 'sharp'
    assert result['stage'] > 0
    assert result['severed'] is False
    
    # Check that bleeding started
    assert tracker.total_bleeding_rate > 0
    
    print("✓ Sharp damage application works")


def test_damage_progression():
    """Test damage stage progression."""
    tracker = DamageTracker()
    
    # Apply multiple hits to same limb
    for i in range(5):
        result = tracker.apply_damage(LimbType.RIGHT_LEG, DamageCategory.BLUNT, 20)
    
    # Should have progressed to higher stage
    stage = tracker.get_damage_stage(LimbType.RIGHT_LEG, DamageCategory.BLUNT)
    assert stage > 5, f"Stage should be > 5, got {stage}"
    
    print("✓ Damage progression works")


def test_limb_severing():
    """Test limb severing mechanic."""
    tracker = DamageTracker()
    
    # Apply massive damage to trigger severing
    result = tracker.apply_damage(LimbType.LEFT_ARM, DamageCategory.SHARP, 200, can_sever=True)
    
    assert result['stage'] == 12
    assert result['severed'] is True
    assert tracker.is_limb_severed(LimbType.LEFT_ARM)
    
    print("✓ Limb severing works")


def test_stuck_projectiles():
    """Test projectiles sticking in body."""
    tracker = DamageTracker()
    
    # Add arrow stuck in torso
    projectile = tracker.add_stuck_projectile("arrow", (10, 20), LimbType.TORSO)
    
    assert projectile.projectile_type == "arrow"
    assert projectile.limb == LimbType.TORSO
    assert len(tracker.stuck_projectiles) == 1
    
    print("✓ Stuck projectiles work")


def test_movement_penalties():
    """Test movement/attack penalties from damage."""
    tracker = DamageTracker()
    
    # No damage = no penalty
    assert tracker.get_movement_penalty() == 0.0
    assert tracker.get_attack_penalty() == 0.0
    
    # Apply some damage
    tracker.apply_damage(LimbType.LEFT_LEG, DamageCategory.BLUNT, 50)
    
    # Should have penalties now
    move_penalty = tracker.get_movement_penalty()
    attack_penalty = tracker.get_attack_penalty()
    
    assert move_penalty > 0.0, f"Should have movement penalty, got {move_penalty}"
    
    print("✓ Damage penalties work")


def test_visual_wounds():
    """Test visual wound tracking."""
    tracker = DamageTracker()
    
    # Apply damage creates visual wounds
    tracker.apply_damage(LimbType.TORSO, DamageCategory.SHARP, 30)
    
    wounds = tracker.get_all_wounds()
    assert len(wounds) > 0
    assert wounds[0].wound_type == "gash"
    assert wounds[0].limb == LimbType.TORSO
    
    print("✓ Visual wounds work")


def test_projectile_creation():
    """Test creating projectiles."""
    projectile = Projectile(
        x=100, y=100,
        angle=0,  # Pointing right
        projectile_type=ProjectileType.ARROW,
        damage=25
    )
    
    assert projectile.x == 100
    assert projectile.y == 100
    assert projectile.active is True
    assert projectile.stuck is False
    
    print("✓ Projectile creation works")


def test_projectile_physics():
    """Test projectile physics update."""
    projectile = Projectile(
        x=100, y=100,
        angle=0,  # Pointing right
        projectile_type=ProjectileType.BULLET,
        damage=30,
        physics=ProjectilePhysics(speed=100, gravity=0)
    )
    
    initial_x = projectile.x
    
    # Update physics (0.1 second)
    projectile.update(0.1)
    
    # Should have moved right
    assert projectile.x > initial_x
    
    print("✓ Projectile physics work")


def test_projectile_collision():
    """Test projectile collision detection."""
    projectile = Projectile(
        x=100, y=100,
        angle=0,
        projectile_type=ProjectileType.ARROW,
        damage=25
    )
    
    # Test collision with point
    hit = projectile.check_collision_point(105, 100, 10)
    assert hit is True, "Should detect collision"
    
    # Test no collision
    hit = projectile.check_collision_point(200, 200, 10)
    assert hit is False, "Should not detect collision"
    
    print("✓ Projectile collision detection works")


def test_projectile_manager():
    """Test projectile manager."""
    manager = ProjectileManager()
    
    # Spawn projectile
    proj = manager.spawn_projectile(
        x=100, y=100,
        angle=0,
        projectile_type=ProjectileType.ARROW,
        damage=25
    )
    
    assert len(manager.projectiles) == 1
    assert len(manager.get_active_projectiles()) == 1
    
    # Update
    manager.update(0.1)
    
    # Still active
    assert len(manager.get_active_projectiles()) == 1
    
    print("✓ Projectile manager works")


def test_projectile_types():
    """Test different projectile types."""
    types_to_test = [
        ProjectileType.ARROW,
        ProjectileType.BULLET,
        ProjectileType.FIREBALL,
        ProjectileType.ICE_SHARD,
    ]
    
    for proj_type in types_to_test:
        projectile = Projectile(
            x=0, y=0, angle=0,
            projectile_type=proj_type,
            damage=10
        )
        assert projectile.projectile_type == proj_type
    
    print("✓ All projectile types work")


def test_damage_categories():
    """Test all damage categories."""
    tracker = DamageTracker()
    
    categories = [
        DamageCategory.SHARP,
        DamageCategory.BLUNT,
        DamageCategory.FIRE,
        DamageCategory.ICE,
        DamageCategory.LIGHTNING,
    ]
    
    for i, category in enumerate(categories):
        limb = list(LimbType)[i % len(LimbType)]
        result = tracker.apply_damage(limb, category, 20)
        assert result['category'] == category.value
    
    print("✓ All damage categories work")


if __name__ == "__main__":
    print("Testing Damage & Projectile Systems...")
    print("-" * 50)
    
    try:
        test_damage_tracker_creation()
        test_apply_sharp_damage()
        test_damage_progression()
        test_limb_severing()
        test_stuck_projectiles()
        test_movement_penalties()
        test_visual_wounds()
        test_projectile_creation()
        test_projectile_physics()
        test_projectile_collision()
        test_projectile_manager()
        test_projectile_types()
        test_damage_categories()
        
        print("-" * 50)
        print("✅ All damage & projectile tests passed!")
        sys.exit(0)
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
Test weapon positioning system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Direct import to avoid __init__ issues
import importlib.util
spec = importlib.util.spec_from_file_location(
    "weapon_positioning",
    str(Path(__file__).parent / "src/ui/weapon_positioning.py")
)
wp_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wp_module)
WeaponPositioning = wp_module.WeaponPositioning


def test_weapon_positioning_creation():
    """Test creating weapon positioning helper."""
    # Should have class methods
    assert hasattr(WeaponPositioning, 'get_weapon_position')
    assert hasattr(WeaponPositioning, 'draw_melee_weapon')
    assert hasattr(WeaponPositioning, 'draw_ranged_weapon')
    
    print("✓ WeaponPositioning class exists with methods")


def test_position_offsets_defined():
    """Test that position offsets are defined for all directions."""
    required_directions = [
        'front', 'front_right', 'front_left',
        'right', 'left',
        'back', 'back_right', 'back_left'
    ]
    
    for direction in required_directions:
        assert direction in WeaponPositioning.POSITION_OFFSETS, \
            f"Direction {direction} should have position offset"
    
    print("✓ All direction offsets defined")


def test_get_weapon_position_front():
    """Test getting weapon position for front facing."""
    pos_info = WeaponPositioning.get_weapon_position(
        facing_direction='front',
        center_x=100,
        center_y=100,
        body_y=50,
        scale_x=1.0,
        scale_y=1.0
    )
    
    assert 'x' in pos_info
    assert 'y' in pos_info
    assert 'flip_horizontal' in pos_info
    assert 'rotation' in pos_info
    assert 'scale_x' in pos_info
    assert 'scale_y' in pos_info
    
    # Front should not flip
    assert pos_info['flip_horizontal'] is False
    
    print("✓ Front facing weapon position works")


def test_get_weapon_position_left():
    """Test getting weapon position for left facing (should flip)."""
    pos_info = WeaponPositioning.get_weapon_position(
        facing_direction='left',
        center_x=100,
        center_y=100,
        body_y=50,
        scale_x=1.0,
        scale_y=1.0
    )
    
    # Left should flip
    assert pos_info['flip_horizontal'] is True
    
    # Scale should be negative when flipped
    assert pos_info['scale_x'] < 0
    
    print("✓ Left facing weapon position flips correctly")


def test_attack_animation_positions():
    """Test weapon positions during attack animation."""
    # Wind up phase (0-0.5)
    pos_wind_up = WeaponPositioning.get_weapon_position(
        facing_direction='front',
        center_x=100,
        center_y=100,
        body_y=50,
        scale_x=1.0,
        scale_y=1.0,
        is_attacking=True,
        attack_frame=0.25  # Mid wind-up
    )
    
    # Strike phase (0.5-1.0)
    pos_strike = WeaponPositioning.get_weapon_position(
        facing_direction='front',
        center_x=100,
        center_y=100,
        body_y=50,
        scale_x=1.0,
        scale_y=1.0,
        is_attacking=True,
        attack_frame=0.75  # Mid strike
    )
    
    # Positions should be different during attack
    assert pos_wind_up['x'] != pos_strike['x'] or pos_wind_up['y'] != pos_strike['y']
    
    print("✓ Attack animation modifies weapon position")


def test_all_directions_work():
    """Test that all directions return valid position info."""
    directions = ['front', 'front_right', 'front_left', 'right', 'left', 
                  'back', 'back_right', 'back_left']
    
    for direction in directions:
        pos_info = WeaponPositioning.get_weapon_position(
            facing_direction=direction,
            center_x=100,
            center_y=100,
            body_y=50,
            scale_x=1.0,
            scale_y=1.0
        )
        
        assert pos_info is not None
        assert isinstance(pos_info, dict)
        assert 'x' in pos_info
        assert 'y' in pos_info
    
    print("✓ All directions produce valid positions")


def test_drawing_methods_exist():
    """Test that drawing methods have correct signatures."""
    # These should not crash when called with mock objects
    class MockCanvas:
        def create_polygon(self, *args, **kwargs): pass
        def create_rectangle(self, *args, **kwargs): pass
        def create_arc(self, *args, **kwargs): pass
        def create_line(self, *args, **kwargs): pass
    
    class MockWeapon:
        pass
    
    canvas = MockCanvas()
    weapon = MockWeapon()
    pos_info = {
        'x': 100, 'y': 100,
        'flip_horizontal': False,
        'rotation': 0,
        'scale_x': 1.0,
        'scale_y': 1.0
    }
    
    # Should not crash
    WeaponPositioning.draw_melee_weapon(canvas, weapon, pos_info)
    WeaponPositioning.draw_ranged_weapon(canvas, weapon, pos_info)
    
    print("✓ Drawing methods work with mock objects")


def test_flip_affects_scale():
    """Test that flip horizontal affects scale_x."""
    pos_normal = WeaponPositioning.get_weapon_position(
        facing_direction='right',
        center_x=100,
        center_y=100,
        body_y=50,
        scale_x=1.0,
        scale_y=1.0
    )
    
    pos_flipped = WeaponPositioning.get_weapon_position(
        facing_direction='left',
        center_x=100,
        center_y=100,
        body_y=50,
        scale_x=1.0,
        scale_y=1.0
    )
    
    # Flipped should have negative scale_x
    if pos_normal['flip_horizontal'] is False:
        assert pos_normal['scale_x'] > 0
    
    if pos_flipped['flip_horizontal'] is True:
        assert pos_flipped['scale_x'] < 0
    
    print("✓ Flip horizontal correctly affects scale_x")


if __name__ == "__main__":
    print("Testing Weapon Positioning System...")
    print("-" * 50)
    
    try:
        test_weapon_positioning_creation()
        test_position_offsets_defined()
        test_get_weapon_position_front()
        test_get_weapon_position_left()
        test_attack_animation_positions()
        test_all_directions_work()
        test_drawing_methods_exist()
        test_flip_affects_scale()
        
        print("-" * 50)
        print("✅ All weapon positioning tests passed!")
        sys.exit(0)
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

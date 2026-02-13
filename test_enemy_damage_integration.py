#!/usr/bin/env python3
"""
Test enemy damage integration.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Direct imports to avoid __init__ issues
import importlib.util

# Load enemy_widget
spec = importlib.util.spec_from_file_location(
    "enemy_widget",
    str(Path(__file__).parent / "src/ui/enemy_widget.py")
)
enemy_widget_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(enemy_widget_module)

# Load damage_system
spec = importlib.util.spec_from_file_location(
    "damage_system",
    str(Path(__file__).parent / "src/features/damage_system.py")
)
damage_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(damage_module)

DamageCategory = damage_module.DamageCategory
LimbType = damage_module.LimbType


def test_enemy_has_damage_tracker():
    """Test that enemy widget has damage tracking integrated."""
    # Can't fully test GUI without display, but we can check the class structure
    EnemyWidget = enemy_widget_module.EnemyWidget
    
    # Check that take_damage method exists
    assert hasattr(EnemyWidget, 'take_damage'), "EnemyWidget should have take_damage method"
    
    print("✓ EnemyWidget has damage tracking methods")


def test_damage_imports_work():
    """Test that damage system imports work in enemy_widget."""
    # Check imports
    assert hasattr(enemy_widget_module, 'DamageTracker'), "DamageTracker should be imported"
    assert hasattr(enemy_widget_module, 'DamageCategory'), "DamageCategory should be imported"
    assert hasattr(enemy_widget_module, 'LimbType'), "LimbType should be imported"
    assert hasattr(enemy_widget_module, 'VisualEffectsRenderer'), "VisualEffectsRenderer should be imported"
    
    print("✓ All damage system imports present in enemy_widget")


def test_take_damage_signature():
    """Test that take_damage has correct signature."""
    EnemyWidget = enemy_widget_module.EnemyWidget
    
    import inspect
    sig = inspect.signature(EnemyWidget.take_damage)
    params = list(sig.parameters.keys())
    
    assert 'self' in params
    assert 'amount' in params
    assert 'category' in params
    assert 'limb' in params
    assert 'can_sever' in params
    
    print("✓ take_damage method has correct signature")


def test_damage_categories_available():
    """Test that damage categories are accessible."""
    categories = [
        DamageCategory.SHARP,
        DamageCategory.BLUNT,
        DamageCategory.ARROW,
        DamageCategory.BULLET,
        DamageCategory.FIRE,
        DamageCategory.ICE,
        DamageCategory.LIGHTNING,
        DamageCategory.POISON
    ]
    
    for cat in categories:
        assert cat is not None
    
    print("✓ All damage categories accessible")


def test_limb_types_available():
    """Test that limb types are accessible."""
    limbs = [
        LimbType.HEAD,
        LimbType.TORSO,
        LimbType.LEFT_ARM,
        LimbType.RIGHT_ARM,
        LimbType.LEFT_LEG,
        LimbType.RIGHT_LEG
    ]
    
    for limb in limbs:
        assert limb is not None
    
    print("✓ All limb types accessible")


if __name__ == "__main__":
    print("Testing Enemy Damage Integration...")
    print("-" * 50)
    
    try:
        test_enemy_has_damage_tracker()
        test_damage_imports_work()
        test_take_damage_signature()
        test_damage_categories_available()
        test_limb_types_available()
        
        print("-" * 50)
        print("✅ All enemy damage integration tests passed!")
        sys.exit(0)
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

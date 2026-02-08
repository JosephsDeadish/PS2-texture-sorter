"""
Test script to verify bug fixes implementation
Tests: Tooltip system, Sound Manager, Customization Panel
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_tooltip_modes():
    """Test that TooltipMode enum has correct values"""
    print("\n=== Testing Tooltip Modes ===")
    from src.features.tutorial_system import TooltipMode
    
    expected_modes = ['normal', 'dumbed-down', 'vulgar_panda']
    actual_modes = [mode.value for mode in TooltipMode]
    
    print(f"Expected modes: {expected_modes}")
    print(f"Actual modes: {actual_modes}")
    
    assert set(actual_modes) == set(expected_modes), "TooltipMode values don't match expected"
    print("✓ TooltipMode enum updated correctly")


def test_panda_tooltips():
    """Test that PandaMode has comprehensive tooltips"""
    print("\n=== Testing PandaMode Tooltips ===")
    from src.features.panda_mode import PandaMode
    
    # Check that TOOLTIPS dictionary exists
    assert hasattr(PandaMode, 'TOOLTIPS'), "PandaMode missing TOOLTIPS"
    
    tooltips = PandaMode.TOOLTIPS
    print(f"Number of tooltip categories: {len(tooltips)}")
    
    # Check a few key categories
    expected_categories = ['sort_button', 'convert_button', 'settings_button', 'theme_selector']
    for category in expected_categories:
        assert category in tooltips, f"Missing tooltip category: {category}"
        assert 'normal' in tooltips[category], f"Missing 'normal' mode in {category}"
        assert 'vulgar' in tooltips[category], f"Missing 'vulgar' mode in {category}"
    
    print(f"✓ PandaMode has comprehensive tooltips with {len(tooltips)} categories")
    print(f"✓ All tooltips have 'normal' and 'vulgar' modes")


def test_panda_get_tooltip():
    """Test PandaMode get_tooltip method"""
    print("\n=== Testing PandaMode.get_tooltip() ===")
    from src.features.panda_mode import PandaMode
    
    # Create PandaMode instance
    panda = PandaMode(enabled=True, vulgar_mode=False)
    
    # Test getting a tooltip in normal mode
    tooltip = panda.get_tooltip('sort_button', mode='normal')
    print(f"Normal tooltip: {tooltip[:50]}...")
    assert tooltip and len(tooltip) > 0, "Tooltip should not be empty"
    
    # Test getting a tooltip in vulgar mode
    tooltip_vulgar = panda.get_tooltip('sort_button', mode='vulgar')
    print(f"Vulgar tooltip: {tooltip_vulgar[:50]}...")
    assert tooltip_vulgar and len(tooltip_vulgar) > 0, "Vulgar tooltip should not be empty"
    
    print("✓ PandaMode.get_tooltip() works correctly")


def test_sound_manager_methods():
    """Test that SoundManager has volume control methods"""
    print("\n=== Testing SoundManager Volume Methods ===")
    from src.features.sound_manager import SoundManager
    
    sound_mgr = SoundManager()
    
    # Test get_volume
    assert hasattr(sound_mgr, 'get_volume'), "SoundManager missing get_volume()"
    volume = sound_mgr.get_volume()
    print(f"Current volume: {volume}")
    assert 0.0 <= volume <= 1.0, "Volume should be between 0.0 and 1.0"
    
    # Test set_volume
    assert hasattr(sound_mgr, 'set_volume'), "SoundManager missing set_volume()"
    sound_mgr.set_volume(0.5)
    assert sound_mgr.get_volume() == 0.5, "set_volume() didn't work"
    
    # Test enabled/disabled flag
    assert hasattr(sound_mgr, 'enabled'), "SoundManager missing 'enabled' flag"
    assert hasattr(sound_mgr, 'muted'), "SoundManager missing 'muted' flag"
    
    print("✓ SoundManager has get_volume() and set_volume()")
    print("✓ SoundManager has enabled/muted flags")


def test_tooltip_verbosity_manager():
    """Test TooltipVerbosityManager with new modes"""
    print("\n=== Testing TooltipVerbosityManager ===")
    from src.features.tutorial_system import TooltipVerbosityManager, TooltipMode
    from src.config import config
    
    # Create manager
    manager = TooltipVerbosityManager(config)
    
    # Test that it has all three modes
    assert TooltipMode.NORMAL in manager.tooltips, "Missing NORMAL mode tooltips"
    assert TooltipMode.DUMBED_DOWN in manager.tooltips, "Missing DUMBED_DOWN mode tooltips"
    assert TooltipMode.VULGAR_PANDA in manager.tooltips, "Missing VULGAR_PANDA mode tooltips"
    
    # Check that tooltips are loaded from PandaMode
    normal_tooltips = manager.tooltips[TooltipMode.NORMAL]
    print(f"Normal mode tooltips count: {len(normal_tooltips)}")
    
    # Check for comprehensive tooltips (should have more than just the basic ones)
    assert len(normal_tooltips) >= 10, "Should have at least 10 tooltip categories"
    
    print("✓ TooltipVerbosityManager has all three modes")
    print("✓ Tooltips loaded from PandaMode")


def test_customization_imports():
    """Test that customization_panel.py imports are working"""
    print("\n=== Testing Customization Panel Imports ===")
    
    try:
        from src.ui.customization_panel import (
            CustomizationPanel,
            SettingsPanel,
            ColorWheelWidget,
            ThemeManager
        )
        print("✓ All customization panel classes imported successfully")
        
        # Check that SettingsPanel exists and has expected methods
        import inspect
        methods = [m[0] for m in inspect.getmembers(SettingsPanel, predicate=inspect.isfunction)]
        expected_methods = ['get_settings', 'set_settings']
        for method in expected_methods:
            assert method in methods, f"SettingsPanel missing {method}()"
        
        print("✓ SettingsPanel has required methods")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        raise


def main():
    """Run all tests"""
    print("=" * 60)
    print("Bug Fixes Implementation Test Suite")
    print("=" * 60)
    
    tests = [
        test_tooltip_modes,
        test_panda_tooltips,
        test_panda_get_tooltip,
        test_sound_manager_methods,
        test_tooltip_verbosity_manager,
        test_customization_imports
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

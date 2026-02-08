"""
Simple test script to verify core bug fixes (no GUI required)
Tests: PandaMode tooltips, Sound Manager methods
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_panda_tooltips():
    """Test that PandaMode has comprehensive tooltips"""
    print("\n=== Testing PandaMode Tooltips ===")
    from src.features.panda_mode import PandaMode
    
    # Check that TOOLTIPS dictionary exists
    assert hasattr(PandaMode, 'TOOLTIPS'), "PandaMode missing TOOLTIPS"
    
    tooltips = PandaMode.TOOLTIPS
    print(f"✓ Number of tooltip categories: {len(tooltips)}")
    
    # Check a few key categories
    expected_categories = ['sort_button', 'convert_button', 'settings_button', 'theme_selector', 
                          'sound_settings', 'tutorial_button', 'help_button']
    for category in expected_categories:
        assert category in tooltips, f"Missing tooltip category: {category}"
        assert 'normal' in tooltips[category], f"Missing 'normal' mode in {category}"
        assert 'vulgar' in tooltips[category], f"Missing 'vulgar' mode in {category}"
        assert isinstance(tooltips[category]['normal'], list), f"'normal' tooltips should be a list"
        assert isinstance(tooltips[category]['vulgar'], list), f"'vulgar' tooltips should be a list"
    
    print(f"✓ PandaMode has comprehensive tooltips with {len(tooltips)} categories")
    print(f"✓ All tested categories have 'normal' and 'vulgar' modes")
    print(f"✓ Tooltips are stored as lists for random selection")


def test_panda_get_tooltip_method():
    """Test PandaMode get_tooltip method exists and works"""
    print("\n=== Testing PandaMode.get_tooltip() Method ===")
    from src.features.panda_mode import PandaMode
    
    # Create PandaMode instance (correct initialization)
    panda = PandaMode(vulgar_mode=False)
    
    # Verify method exists
    assert hasattr(panda, 'get_tooltip'), "PandaMode missing get_tooltip method"
    
    # Test getting a tooltip in normal mode
    tooltip = panda.get_tooltip('sort_button', mode='normal')
    print(f"✓ Normal tooltip sample: '{tooltip[:60]}...'")
    assert tooltip and len(tooltip) > 0, "Tooltip should not be empty"
    
    # Test getting a tooltip in vulgar mode
    tooltip_vulgar = panda.get_tooltip('sort_button', mode='vulgar')
    print(f"✓ Vulgar tooltip sample: '{tooltip_vulgar[:60]}...'")
    assert tooltip_vulgar and len(tooltip_vulgar) > 0, "Vulgar tooltip should not be empty"
    
    # Verify tooltips are different
    assert tooltip != tooltip_vulgar or len(PandaMode.TOOLTIPS['sort_button']['normal']) > 1, \
        "Should have different tooltips or multiple options"
    
    print("✓ PandaMode.get_tooltip() works correctly with 'normal' and 'vulgar' modes")


def test_sound_manager_volume_methods():
    """Test that SoundManager has volume control methods"""
    print("\n=== Testing SoundManager Volume Methods ===")
    from src.features.sound_manager import SoundManager
    
    sound_mgr = SoundManager()
    
    # Test get_volume
    assert hasattr(sound_mgr, 'get_volume'), "SoundManager missing get_volume()"
    volume = sound_mgr.get_volume()
    print(f"✓ get_volume() returns: {volume}")
    assert 0.0 <= volume <= 1.0, "Volume should be between 0.0 and 1.0"
    
    # Test set_volume
    assert hasattr(sound_mgr, 'set_volume'), "SoundManager missing set_volume()"
    sound_mgr.set_volume(0.5)
    assert sound_mgr.get_volume() == 0.5, "set_volume() didn't work correctly"
    print(f"✓ set_volume(0.5) works, new volume: {sound_mgr.get_volume()}")
    
    # Test volume clamping
    sound_mgr.set_volume(1.5)  # Should clamp to 1.0
    assert sound_mgr.get_volume() == 1.0, "Volume should be clamped to 1.0"
    sound_mgr.set_volume(-0.5)  # Should clamp to 0.0
    assert sound_mgr.get_volume() == 0.0, "Volume should be clamped to 0.0"
    print(f"✓ Volume clamping works correctly (0.0 to 1.0)")
    
    # Test enabled/disabled flag
    assert hasattr(sound_mgr, 'enabled'), "SoundManager missing 'enabled' flag"
    assert hasattr(sound_mgr, 'muted'), "SoundManager missing 'muted' flag"
    print(f"✓ SoundManager has 'enabled' and 'muted' flags")
    
    print("✓ All SoundManager volume methods work correctly")


def test_tooltip_categories_comprehensive():
    """Verify we have tooltips for all major UI elements"""
    print("\n=== Testing Tooltip Category Coverage ===")
    from src.features.panda_mode import PandaMode
    
    tooltips = PandaMode.TOOLTIPS
    
    # Expected comprehensive categories
    expected_categories = [
        'sort_button', 'convert_button', 'settings_button', 
        'file_selection', 'category_selection', 'lod_detection',
        'batch_operations', 'export_button', 'preview_button',
        'search_button', 'analysis_button', 'favorites_button',
        'recent_files', 'theme_selector', 'cursor_selector',
        'sound_settings', 'tutorial_button', 'help_button',
        'about_button', 'undo_button', 'redo_button'
    ]
    
    found_categories = []
    missing_categories = []
    
    for category in expected_categories:
        if category in tooltips:
            found_categories.append(category)
        else:
            missing_categories.append(category)
    
    print(f"✓ Found {len(found_categories)}/{len(expected_categories)} expected categories")
    
    if missing_categories:
        print(f"  Missing categories: {', '.join(missing_categories)}")
    
    # We should have most of them
    assert len(found_categories) >= 18, f"Should have at least 18 categories, found {len(found_categories)}"
    
    print(f"✓ Tooltip coverage is comprehensive ({len(tooltips)} total categories)")


def main():
    """Run all tests"""
    print("=" * 70)
    print("Bug Fixes Implementation Test Suite (Core Features)")
    print("=" * 70)
    
    tests = [
        test_panda_tooltips,
        test_panda_get_tooltip_method,
        test_sound_manager_volume_methods,
        test_tooltip_categories_comprehensive
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
    
    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("\n✓✓✓ All core bug fixes implemented and working! ✓✓✓")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

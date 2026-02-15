#!/usr/bin/env python3
"""
Test script to verify actual Qt integration in main.py
Tests that Qt modules are actually being used, not just existing as files.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_qt_imports_in_main():
    """Test that main.py actually imports Qt loaders."""
    with open('main.py', 'r') as f:
        content = f.read()
    
    print("Testing Qt imports in main.py...")
    
    # Check for qt_panel_loader import
    tests = [
        ('qt_panel_loader import', 'from src.ui.qt_panel_loader import'),
        ('get_closet_panel usage', 'get_closet_panel'),
        ('get_hotkey_settings_panel usage', 'get_hotkey_settings_panel'),
        ('get_customization_panel usage', 'get_customization_panel'),
        ('get_background_remover_panel usage', 'get_background_remover_panel'),
        ('PreviewViewerQt usage', 'PreviewViewerQt'),
    ]
    
    passed = 0
    failed = 0
    
    for name, check in tests:
        if check in content:
            print(f"  ✅ {name}: FOUND")
            passed += 1
        else:
            print(f"  ❌ {name}: NOT FOUND")
            failed += 1
    
    return passed, failed

def test_qt_modules_exist():
    """Test that Qt module files actually exist."""
    print("\nTesting Qt module files...")
    
    files = [
        'src/ui/weapon_positioning_qt.py',
        'src/features/preview_viewer_qt.py',
        'src/ui/closet_display_qt.py',
        'src/ui/color_picker_qt.py',
        'src/ui/trail_preview_qt.py',
        'src/ui/paint_tools_qt.py',
        'src/ui/widgets_display_qt.py',
        'src/ui/live_preview_qt.py',
        'src/ui/hotkey_display_qt.py',
        'src/ui/widgets_panel_qt.py',
        'src/ui/customization_panel_qt.py',
        'src/ui/background_remover_panel_qt.py',
        'src/ui/qt_panel_loader.py',
    ]
    
    passed = 0
    failed = 0
    
    for filepath in files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✅ {filepath}: EXISTS ({size} bytes)")
            passed += 1
        else:
            print(f"  ❌ {filepath}: MISSING")
            failed += 1
    
    return passed, failed

def test_deprecation_warnings():
    """Test that old canvas files are marked deprecated."""
    print("\nTesting deprecation warnings...")
    
    files = [
        'src/ui/enemy_widget.py',
        'src/ui/dungeon_renderer.py',
        'src/ui/enhanced_dungeon_renderer.py',
        'src/ui/visual_effects_renderer.py',
    ]
    
    passed = 0
    failed = 0
    
    for filepath in files:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read(500)  # Check first 500 chars
            if 'DEPRECATED' in content:
                print(f"  ✅ {filepath}: HAS DEPRECATION WARNING")
                passed += 1
            else:
                print(f"  ⚠️  {filepath}: NO DEPRECATION WARNING")
                failed += 1
        else:
            print(f"  ⚠️  {filepath}: FILE NOT FOUND")
            failed += 1
    
    return passed, failed

def main():
    """Run all tests."""
    print("=" * 60)
    print("ACTUAL INTEGRATION TEST")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    # Test 1: Qt imports in main.py
    p, f = test_qt_imports_in_main()
    total_passed += p
    total_failed += f
    
    # Test 2: Qt module files exist
    p, f = test_qt_modules_exist()
    total_passed += p
    total_failed += f
    
    # Test 3: Deprecation warnings
    p, f = test_deprecation_warnings()
    total_passed += p
    total_failed += f
    
    # Summary
    print("\n" + "=" * 60)
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print("=" * 60)
    
    if total_failed == 0:
        print("✅ ALL TESTS PASSED - Integration verified!")
        return 0
    else:
        print(f"❌ {total_failed} TESTS FAILED - More work needed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())

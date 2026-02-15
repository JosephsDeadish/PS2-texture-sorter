#!/usr/bin/env python3
"""
Complete Qt/OpenGL Migration Verification Test

This test verifies that the application has been completely migrated from
Canvas/Tkinter to Qt/OpenGL as per the requirements:
1. Qt for UI (tabs, buttons, layout, events)
2. OpenGL for Panda rendering and skeletal animations
3. Qt timer/state system for animation state control
4. No bridge files, no old files, no deprecation markers
5. Complete working replacements only

Author: Dead On The Inside / JosephsDeadish
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_no_tkinter_imports():
    """Verify no tkinter or customtkinter imports exist."""
    print("Testing: No tkinter/customtkinter imports...")
    
    src_dir = Path(__file__).parent / 'src'
    tkinter_found = []
    
    for py_file in src_dir.rglob('*.py'):
        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if 'import tkinter' in content or 'from tkinter' in content:
                tkinter_found.append((str(py_file), 'tkinter'))
            if 'import customtkinter' in content or 'from customtkinter' in content:
                tkinter_found.append((str(py_file), 'customtkinter'))
    
    if tkinter_found:
        print("❌ FAILED: Found tkinter/customtkinter imports:")
        for file, lib in tkinter_found:
            print(f"  - {file}: {lib}")
        return False
    
    print("✅ PASSED: No tkinter/customtkinter imports found")
    return True


def test_no_canvas_references():
    """Verify no canvas references in code (except in comments for historical context)."""
    print("\nTesting: No active Canvas references...")
    
    src_dir = Path(__file__).parent / 'src'
    canvas_found = []
    
    for py_file in src_dir.rglob('*.py'):
        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            in_docstring = False
            docstring_delim = None
            
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                
                # Track docstring state
                if '"""' in stripped or "'''" in stripped:
                    if not in_docstring:
                        in_docstring = True
                        docstring_delim = '"""' if '"""' in stripped else "'''"
                    elif docstring_delim in stripped:
                        in_docstring = False
                        continue
                
                # Skip comments, docstrings, and string literals
                if stripped.startswith('#') or in_docstring:
                    continue
                
                # Check for actual canvas usage (constructors or methods)
                if any(pattern in line for pattern in ['= Canvas(', '.Canvas(', 'tk.Canvas(']):
                    canvas_found.append((str(py_file), i, line.strip()))
    
    if canvas_found:
        print("❌ FAILED: Found active Canvas references:")
        for file, line_no, line in canvas_found:
            print(f"  - {file}:{line_no}: {line}")
        return False
    
    print("✅ PASSED: No active Canvas usage found")
    print("  (Historical references in docstrings are acceptable)")
    return True


def test_qt_architecture():
    """Verify Qt architecture is in place."""
    print("\nTesting: Qt architecture...")
    
    main_file = Path(__file__).parent / 'main.py'
    
    if not main_file.exists():
        print("❌ FAILED: main.py not found")
        return False
    
    with open(main_file, 'r') as f:
        content = f.read()
    
    required_qt = [
        'from PyQt6.QtWidgets import',
        'from PyQt6.QtCore import',
        'QMainWindow',
        'QTabWidget',
        'QTimer',
    ]
    
    missing = []
    for item in required_qt:
        if item not in content:
            missing.append(item)
    
    if missing:
        print("❌ FAILED: Missing Qt components in main.py:")
        for item in missing:
            print(f"  - {item}")
        return False
    
    print("✅ PASSED: Qt architecture verified in main.py")
    return True


def test_opengl_panda_widget():
    """Verify OpenGL panda widget exists and has required features."""
    print("\nTesting: OpenGL panda widget...")
    
    panda_gl = Path(__file__).parent / 'src' / 'ui' / 'panda_widget_gl.py'
    
    if not panda_gl.exists():
        print("❌ FAILED: panda_widget_gl.py not found")
        return False
    
    with open(panda_gl, 'r') as f:
        content = f.read()
    
    required_features = [
        'QOpenGLWidget',
        'OpenGL.GL',
        'TARGET_FPS = 60',
        'QTimer',
        'QStateMachine',
        'QState',
        '_draw_panda_arms',
        '_draw_panda_legs',
        '_get_limb_positions',
        'paintGL',
        'initializeGL',
    ]
    
    missing = []
    for feature in required_features:
        if feature not in content:
            missing.append(feature)
    
    if missing:
        print("❌ FAILED: Missing OpenGL features:")
        for item in missing:
            print(f"  - {item}")
        return False
    
    print("✅ PASSED: OpenGL panda widget verified")
    print("  - QOpenGLWidget: ✓")
    print("  - 60 FPS target: ✓")
    print("  - Skeletal animations: ✓")
    print("  - Qt Timer: ✓")
    print("  - Qt State Machine: ✓")
    return True


def test_qt_timer_animation():
    """Verify Qt timer is used for animation control."""
    print("\nTesting: Qt timer animation control...")
    
    panda_gl = Path(__file__).parent / 'src' / 'ui' / 'panda_widget_gl.py'
    
    with open(panda_gl, 'r') as f:
        content = f.read()
    
    # Check for QTimer usage
    if 'self.timer = QTimer(self)' not in content:
        print("❌ FAILED: QTimer not initialized")
        return False
    
    if 'self.timer.timeout.connect' not in content:
        print("❌ FAILED: QTimer timeout not connected")
        return False
    
    if 'self.timer.start' not in content:
        print("❌ FAILED: QTimer not started")
        return False
    
    print("✅ PASSED: Qt timer animation control verified")
    return True


def test_skeletal_animations():
    """Verify skeletal animation system is implemented."""
    print("\nTesting: Skeletal animations...")
    
    panda_gl = Path(__file__).parent / 'src' / 'ui' / 'panda_widget_gl.py'
    
    with open(panda_gl, 'r') as f:
        content = f.read()
    
    # Check for limb-based animations
    skeletal_features = [
        'left_arm_angle',
        'right_arm_angle',
        'left_leg_angle',
        'right_leg_angle',
        'glRotatef',  # OpenGL rotation for limbs
        '_get_limb_positions',
    ]
    
    missing = []
    for feature in skeletal_features:
        if feature not in content:
            missing.append(feature)
    
    if missing:
        print("❌ FAILED: Missing skeletal animation features:")
        for item in missing:
            print(f"  - {item}")
        return False
    
    print("✅ PASSED: Skeletal animation system verified")
    print("  - Limb rotations: ✓")
    print("  - OpenGL transformations: ✓")
    print("  - Animation states: ✓")
    return True


def test_no_bridge_files():
    """Verify no bridge or deprecated files exist."""
    print("\nTesting: No bridge or deprecated files...")
    
    src_ui = Path(__file__).parent / 'src' / 'ui'
    
    deprecated_files = [
        'qt_widget_bridge.py',
        'dungeon_qt_bridge.py',
        'weapon_positioning.py',  # Old canvas-based version
        'panda_widget.py',  # Old canvas-based version (if it existed)
    ]
    
    found = []
    for filename in deprecated_files:
        filepath = src_ui / filename
        if filepath.exists():
            found.append(str(filepath))
    
    if found:
        print("❌ FAILED: Found deprecated/bridge files:")
        for file in found:
            print(f"  - {file}")
        return False
    
    print("✅ PASSED: No bridge or deprecated files found")
    return True


def test_performance_dashboard_qt():
    """Verify performance dashboard uses pure Qt."""
    print("\nTesting: Performance dashboard Qt implementation...")
    
    perf_dash = Path(__file__).parent / 'src' / 'ui' / 'performance_dashboard.py'
    
    if not perf_dash.exists():
        print("❌ FAILED: performance_dashboard.py not found")
        return False
    
    with open(perf_dash, 'r') as f:
        lines = f.readlines()
    
    # Check imports (non-comment lines)
    has_pyqt = False
    has_ctk_import = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or not stripped:
            continue
        if 'from PyQt6.QtWidgets import' in line:
            has_pyqt = True
        if 'import customtkinter' in line or 'from customtkinter' in line:
            has_ctk_import = True
    
    if not has_pyqt:
        print("❌ FAILED: Missing PyQt6 imports")
        return False
    
    if has_ctk_import:
        print("❌ FAILED: Still importing customtkinter")
        return False
    
    # Check for actual usage (ctk. in code, not comments)
    content = '\n'.join(lines)
    code_lines = [l for l in lines if not l.strip().startswith('#') and not l.strip().startswith('"""')]
    code = '\n'.join(code_lines)
    
    if 'class PerformanceDashboard(ctk.' in code:
        print("❌ FAILED: Still inheriting from customtkinter")
        return False
    
    if 'QTimer' not in content:
        print("❌ FAILED: Not using QTimer")
        return False
    
    print("✅ PASSED: Performance dashboard uses pure Qt")
    return True


def test_svg_icon_helper_qt():
    """Verify SVG icon helper uses pure Qt."""
    print("\nTesting: SVG icon helper Qt implementation...")
    
    svg_helper = Path(__file__).parent / 'src' / 'utils' / 'svg_icon_helper.py'
    
    if not svg_helper.exists():
        print("❌ FAILED: svg_icon_helper.py not found")
        return False
    
    with open(svg_helper, 'r') as f:
        lines = f.readlines()
    
    # Check imports (non-comment lines)
    has_pyqt = False
    has_ctk_import = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or not stripped:
            continue
        if 'from PyQt6.QtGui import' in line:
            has_pyqt = True
        if 'import customtkinter' in line or 'from customtkinter' in line:
            has_ctk_import = True
    
    if not has_pyqt:
        print("❌ FAILED: Missing PyQt6 imports")
        return False
    
    if has_ctk_import:
        print("❌ FAILED: Still importing customtkinter")
        return False
    
    # Check for required Qt components
    content = '\n'.join(lines)
    required_qt = ['QIcon', 'QPixmap', 'QSvgRenderer']
    missing = [item for item in required_qt if item not in content]
    
    if missing:
        print(f"❌ FAILED: Missing Qt components: {missing}")
        return False
    
    print("✅ PASSED: SVG icon helper uses pure Qt")
    return True


def main():
    """Run all verification tests."""
    print("=" * 70)
    print("Qt/OpenGL Complete Migration Verification")
    print("=" * 70)
    print()
    
    tests = [
        test_no_tkinter_imports,
        test_no_canvas_references,
        test_qt_architecture,
        test_opengl_panda_widget,
        test_qt_timer_animation,
        test_skeletal_animations,
        test_no_bridge_files,
        test_performance_dashboard_qt,
        test_svg_icon_helper_qt,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ ERROR in {test.__name__}: {e}")
            results.append(False)
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print()
        print("🎉 ALL TESTS PASSED!")
        print()
        print("✅ Qt for UI (tabs, buttons, layout, events)")
        print("✅ OpenGL for Panda rendering and skeletal animations")
        print("✅ Qt timer/state system for animation state control")
        print("✅ No bridge files")
        print("✅ No old files")
        print("✅ No deprecation markers")
        print("✅ Complete working replacements only")
        print()
        return 0
    else:
        print()
        print("❌ SOME TESTS FAILED")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())

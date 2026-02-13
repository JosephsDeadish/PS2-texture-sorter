#!/usr/bin/env python3
"""
Cairo DLL Setup Script for Game Texture Sorter
Author: Dead On The Inside / JosephsDeadish

This script helps set up Cairo DLLs for building the application with SVG support.

Features:
- Detects existing Cairo installations
- Verifies all required DLLs are present
- Copies DLLs to local cairo_dlls/ folder for portable builds
- Provides installation instructions if DLLs are missing
- Generates a detailed report
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Required Cairo DLLs
REQUIRED_DLLS = [
    'libcairo-2.dll',
    'libcairo-gobject-2.dll',
    'libpng16.dll',
    'zlib1.dll',
    'libfreetype-6.dll',
    'libfontconfig-1.dll',
    'libexpat-1.dll',
    'libbz2-1.dll',
    'libharfbuzz-0.dll',
    'libglib-2.0-0.dll',
    'libintl-8.dll',
    'libiconv-2.dll',
    'libpixman-1-0.dll',
]

# Alternative DLL names
ALTERNATIVE_DLLS = {
    'libffi-8.dll': 'libffi-7.dll',
}

# Common installation paths
SEARCH_PATHS = [
    r'C:\Program Files\GTK3-Runtime Win64\bin',
    r'C:\msys64\mingw64\bin',
    r'C:\msys64\ucrt64\bin',
    r'C:\msys64\clang64\bin',
    os.environ.get('CAIRO_DLL_PATH', ''),
]


def print_header(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70 + "\n")


def print_status(status: str, message: str):
    """Print a status message with icon."""
    icons = {
        'success': '✓',
        'warning': '⚠',
        'error': '✗',
        'info': 'ℹ',
    }
    icon = icons.get(status, '•')
    print(f"{icon} {message}")


def detect_cairo_installations() -> List[Path]:
    """
    Detect Cairo installations on the system.
    Returns list of paths where Cairo DLLs were found.
    """
    installations = []
    
    for path_str in SEARCH_PATHS:
        if not path_str:
            continue
        
        path = Path(path_str)
        if not path.exists():
            continue
        
        # Check if this path contains libcairo-2.dll (main indicator)
        if (path / 'libcairo-2.dll').exists():
            installations.append(path)
    
    return installations


def find_dlls_in_path(search_path: Path) -> Tuple[Dict[str, Path], List[str]]:
    """
    Find all required DLLs in a given path.
    Returns tuple of (found_dlls_dict, missing_dll_names).
    """
    found = {}
    missing = []
    
    for dll_name in REQUIRED_DLLS:
        dll_path = search_path / dll_name
        if dll_path.exists():
            found[dll_name] = dll_path
        else:
            missing.append(dll_name)
    
    # Check for alternatives
    for primary, alternative in ALTERNATIVE_DLLS.items():
        if primary not in found:
            alt_path = search_path / alternative
            if alt_path.exists():
                found[primary] = alt_path
                if primary in missing:
                    missing.remove(primary)
    
    return found, missing


def copy_dlls_to_local(found_dlls: Dict[str, Path], target_dir: Path) -> bool:
    """
    Copy DLLs to local cairo_dlls/ directory.
    Returns True if successful.
    """
    try:
        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)
        
        print_status('info', f"Copying {len(found_dlls)} DLLs to: {target_dir}")
        
        for dll_name, dll_path in found_dlls.items():
            target_path = target_dir / dll_name
            shutil.copy2(dll_path, target_path)
            print_status('success', f"Copied: {dll_name}")
        
        return True
        
    except Exception as e:
        print_status('error', f"Failed to copy DLLs: {e}")
        return False


def print_installation_instructions():
    """Print instructions for installing Cairo on Windows."""
    print_header("Cairo Installation Instructions")
    
    print("Option 1: GTK3 Runtime (Recommended for most users)")
    print("-" * 70)
    print("1. Download GTK3 runtime installer:")
    print("   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases")
    print("2. Run the installer with default settings")
    print("3. Re-run this setup script")
    print()
    
    print("Option 2: MSYS2 (For developers)")
    print("-" * 70)
    print("1. Install MSYS2 from: https://www.msys2.org/")
    print("2. Open MSYS2 MINGW64 terminal")
    print("3. Run: pacman -S mingw-w64-x86_64-gtk3")
    print("4. Re-run this setup script")
    print()
    
    print("Option 3: Portable Installation")
    print("-" * 70)
    print("1. Download Cairo DLLs from a working GTK3 installation")
    print("2. Create a folder: cairo_dlls/")
    print("3. Copy all required DLLs to cairo_dlls/")
    print("4. Set environment variable: CAIRO_DLL_PATH=<path_to_cairo_dlls>")
    print()


def verify_cairo_python_package():
    """Check if cairosvg Python package is installed."""
    print_header("Python Package Check")
    
    try:
        import cairosvg
        print_status('success', f"cairosvg {cairosvg.__version__} is installed")
        return True
    except ImportError:
        print_status('warning', "cairosvg Python package is NOT installed")
        print("\nTo install:")
        print("  pip install cairosvg cairocffi")
        return False


def main():
    """Main execution function."""
    script_dir = Path(__file__).parent.parent
    cairo_dlls_dir = script_dir / 'cairo_dlls'
    
    print_header("Cairo DLL Setup for Game Texture Sorter")
    print("This script will help you set up Cairo DLLs for SVG support.")
    
    # Step 1: Detect installations
    print_header("Step 1: Detecting Cairo Installations")
    
    installations = detect_cairo_installations()
    
    if not installations:
        print_status('warning', "No Cairo installations found on this system")
        print_installation_instructions()
        return 1
    
    print_status('success', f"Found {len(installations)} Cairo installation(s):")
    for path in installations:
        print(f"  • {path}")
    
    # Step 2: Find DLLs
    print_header("Step 2: Verifying DLLs")
    
    best_installation = None
    best_found = {}
    min_missing = len(REQUIRED_DLLS)
    
    for install_path in installations:
        found, missing = find_dlls_in_path(install_path)
        
        print(f"\nChecking: {install_path}")
        print_status('success', f"Found: {len(found)}/{len(REQUIRED_DLLS)} DLLs")
        
        if missing:
            print_status('warning', f"Missing: {len(missing)} DLLs")
            for dll in missing[:5]:  # Show first 5
                print(f"    - {dll}")
            if len(missing) > 5:
                print(f"    ... and {len(missing) - 5} more")
        
        if len(missing) < min_missing:
            min_missing = len(missing)
            best_installation = install_path
            best_found = found
    
    # Step 3: Copy DLLs if found
    if best_found:
        print_header("Step 3: Setting Up Portable DLLs")
        
        if len(best_found) == len(REQUIRED_DLLS):
            print_status('success', "All required DLLs found!")
            
            print(f"\nDo you want to copy DLLs to: {cairo_dlls_dir}?")
            print("This creates a portable installation for building.")
            response = input("Copy DLLs? (y/N): ").strip().lower()
            
            if response in ['y', 'yes']:
                if copy_dlls_to_local(best_found, cairo_dlls_dir):
                    print_status('success', "DLLs copied successfully!")
                    print(f"\nPortable Cairo installation created at: {cairo_dlls_dir}")
                else:
                    print_status('error', "Failed to copy DLLs")
                    return 1
            else:
                print_status('info', "Skipped copying DLLs")
                print(f"Build will use DLLs from: {best_installation}")
        else:
            print_status('warning', "Some DLLs are missing from all installations")
            print("\nMissing DLLs may cause SVG support to fail.")
            print("Please install the complete GTK3 runtime or MSYS2 package.")
    
    # Step 4: Verify Python packages
    verify_cairo_python_package()
    
    # Step 5: Summary
    print_header("Setup Summary")
    
    if len(best_found) == len(REQUIRED_DLLS):
        print_status('success', "Cairo DLLs are ready for building with SVG support!")
        print("\nNext steps:")
        print("  1. Install Python packages: pip install cairosvg cairocffi")
        print("  2. Build with SVG support: python scripts/build_with_svg.py")
        print("  3. Or directly: pyinstaller build_spec_with_svg.spec")
        return 0
    else:
        print_status('warning', "Setup incomplete - some DLLs are missing")
        print("\nPlease install Cairo using one of the methods above,")
        print("then re-run this script.")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

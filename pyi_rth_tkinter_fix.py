"""
PyInstaller Runtime Hook to Fix TCL/Tk Library Path Issues

This runtime hook ensures that tkinter can find the TCL and TK libraries
when running from a PyInstaller bundle. It fixes the error:
"failed to execute script pyi_rth_tkinter due to unhandled exception: 
tcl data directory not found"

This hook runs before the main application starts and sets up the proper
environment variables for TCL/Tk to work correctly.
"""

import os
import sys
from pathlib import Path


def fix_tkinter_paths():
    """
    Set up TCL_LIBRARY and TK_LIBRARY environment variables for PyInstaller bundles.
    
    This function locates the tcl and tk directories within the PyInstaller bundle
    and sets the appropriate environment variables so that tkinter can find them.
    """
    # Only run this fix when frozen (running from PyInstaller bundle)
    if not getattr(sys, 'frozen', False):
        return
    
    # Get the base directory where PyInstaller extracts files
    # For one-folder builds: this is the directory containing the .exe
    # For one-file builds: this is sys._MEIPASS (temporary extraction directory)
    if hasattr(sys, '_MEIPASS'):
        # One-file build: files are extracted to a temporary directory
        base_dir = Path(sys._MEIPASS)
    else:
        # One-folder build: files are in the same directory as the executable
        base_dir = Path(sys.executable).parent
    
    # Try to find tcl and tk directories in common locations
    tcl_paths = [
        base_dir / 'tcl',
        base_dir / '_internal' / 'tcl',
        base_dir / 'tcl86',
        base_dir / '_internal' / 'tcl86',
        base_dir / 'tcl8.6',
        base_dir / '_internal' / 'tcl8.6',
    ]
    
    tk_paths = [
        base_dir / 'tk',
        base_dir / '_internal' / 'tk',
        base_dir / 'tk86',
        base_dir / '_internal' / 'tk86',
        base_dir / 'tk8.6',
        base_dir / '_internal' / 'tk8.6',
    ]
    
    # Find the first existing TCL directory
    tcl_dir = None
    for path in tcl_paths:
        if path.exists() and path.is_dir():
            tcl_dir = path
            break
    
    # Find the first existing TK directory
    tk_dir = None
    for path in tk_paths:
        if path.exists() and path.is_dir():
            tk_dir = path
            break
    
    # Set environment variables if directories were found
    if tcl_dir:
        os.environ['TCL_LIBRARY'] = str(tcl_dir)
        print(f"[Tkinter Fix] Set TCL_LIBRARY to: {tcl_dir}")
    else:
        print(f"[Tkinter Fix] Warning: Could not find TCL directory in: {base_dir}")
    
    if tk_dir:
        os.environ['TK_LIBRARY'] = str(tk_dir)
        print(f"[Tkinter Fix] Set TK_LIBRARY to: {tk_dir}")
    else:
        print(f"[Tkinter Fix] Warning: Could not find TK directory in: {base_dir}")
    
    # Additional fix: Ensure _tkinter can find the tcl/tk DLLs on Windows
    if sys.platform == 'win32':
        # Add the base directory and _internal to PATH so DLLs can be found
        internal_dir = base_dir / '_internal'
        if internal_dir.exists():
            os.environ['PATH'] = str(internal_dir) + os.pathsep + os.environ.get('PATH', '')
        os.environ['PATH'] = str(base_dir) + os.pathsep + os.environ.get('PATH', '')


# Run the fix immediately when this hook is imported
fix_tkinter_paths()

"""
Runtime hook: set QT_QPA_PLATFORM=offscreen on headless Linux.

PyInstaller runs this file BEFORE application code starts.  On a headless
Linux host (CI runner, Docker, server) PyQt6 needs either a live X11/Wayland
display or QT_QPA_PLATFORM=offscreen.  Without it the first
``from PyQt6.QtWidgets import …`` raises an ImportError (libEGL / xcb not
found) and the entire UI falls back to stub mode.

This hook is a no-op on Windows and macOS, and a no-op on Linux when the
caller has already set QT_QPA_PLATFORM or a real display is available.
"""

import os
import sys


def _setup_qt_platform() -> None:
    """Set QT_QPA_PLATFORM=offscreen on headless Linux when not already set."""
    if not sys.platform.startswith('linux'):
        return
    if 'QT_QPA_PLATFORM' in os.environ:
        return
    display = os.environ.get('DISPLAY', '')
    wayland = os.environ.get('WAYLAND_DISPLAY', '')
    if not display and not wayland:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'


_setup_qt_platform()

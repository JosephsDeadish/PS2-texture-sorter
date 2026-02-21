"""
Shared PyQt6 fallback stubs — used by all UI modules in their
``except ImportError`` blocks when PyQt6 is not installed.

Import pattern in each UI file::

    try:
        from PyQt6.QtWidgets import QWidget, ...
        from PyQt6.QtCore import pyqtSignal, ...
        PYQT_AVAILABLE = True
    except ImportError:
        PYQT_AVAILABLE = False
        from ui._pyqt_stubs import (
            QWidget, QDialog, QThread, QObject,
            pyqtSignal, Qt, QTimer, QColor, QFont, QPixmap, QIcon,
        )
"""
from __future__ import annotations


class _SignalStub:
    """Stub signal — active only when PyQt6 is absent."""

    def __init__(self, *a): pass
    def connect(self, *a): pass
    def disconnect(self, *a): pass
    def emit(self, *a): pass


def pyqtSignal(*a, **kw) -> _SignalStub:  # noqa: N802
    """Return a _SignalStub so ``MyClass.my_signal = pyqtSignal(str)`` works."""
    return _SignalStub()


# ---------------------------------------------------------------------------
# Minimal Qt class stubs
# ---------------------------------------------------------------------------

class QWidget:  # noqa: E301
    def __init__(self, *a, **kw): pass


class QDialog(QWidget): pass  # noqa: E301


class QFrame(QWidget): pass  # noqa: E301


class QThread:  # noqa: E301
    def __init__(self, *a, **kw): pass
    def start(self, *a): pass
    def quit(self, *a): pass
    def wait(self, *a): pass


class QObject:  # noqa: E301
    def __init__(self, *a, **kw): pass


class QGraphicsView(QWidget): pass  # noqa: E301
class QGraphicsScene:  # noqa: E301
    def __init__(self, *a, **kw): pass


class QOpenGLWidget(QWidget): pass  # noqa: E301


class Qt:  # noqa: E301
    AlignCenter = 0; AlignLeft = 0; AlignRight = 0  # noqa: E702
    LeftButton = 0; RightButton = 0; MiddleButton = 0  # noqa: E702
    Horizontal = 0; Vertical = 0  # noqa: E702
    SmoothTransformation = 0  # noqa: E702
    KeepAspectRatio = 0  # noqa: E702
    transparent = 0  # noqa: E702
    WindowType = type('WindowType', (), {'FramelessWindowHint': 0, 'WindowStaysOnTopHint': 0})  # noqa: E501


class QTimer:  # noqa: E301
    timeout = _SignalStub()

    def __init__(self, *a, **kw): pass
    def start(self, *a): pass
    def stop(self): pass
    def setInterval(self, *a): pass

    @staticmethod
    def singleShot(ms, callback): pass


class QColor:  # noqa: E301
    def __init__(self, *a, **kw): pass
    def name(self): return '#000000'
    def isValid(self): return True


class QFont:  # noqa: E301
    def __init__(self, *a, **kw): pass


class QPixmap:  # noqa: E301
    def __init__(self, *a, **kw): pass
    def isNull(self): return True
    def scaled(self, *a, **kw): return self


class QIcon:  # noqa: E301
    def __init__(self, *a, **kw): pass

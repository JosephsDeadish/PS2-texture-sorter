# Qt/OpenGL Architecture Visualization

## Application Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                 Qt6 Main Application                         │
│              (QApplication + QMainWindow)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    UI Layer (Qt6)                            │
├─────────────────────────────────────────────────────────────┤
│  • QTabWidget          → Tabs for different sections         │
│  • QPushButton         → All buttons                         │
│  • QLabel              → Text labels                         │
│  • QTextEdit           → Log display                         │
│  • QProgressBar        → Progress indicators                 │
│  • QVBoxLayout         → Vertical layouts                    │
│  • QHBoxLayout         → Horizontal layouts                  │
│  • QFileDialog         → File selection                      │
│  • QMessageBox         → Error/info dialogs                  │
│  • QMenuBar/QMenu      → Application menus                   │
│  • QStatusBar          → Status messages                     │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌───────────────────────────┐  ┌───────────────────────────┐
│  Qt Panel Loader          │  │  3D Rendering (OpenGL)    │
│  (qt_panel_loader.py)     │  │  (panda_widget_gl.py)     │
├───────────────────────────┤  ├───────────────────────────┤
│  • widgets_panel_qt       │  │  QOpenGLWidget            │
│  • closet_display_qt      │  │  ┌────────────────────┐   │
│  • hotkey_display_qt      │  │  │ OpenGL Context     │   │
│  • customization_panel_qt │  │  │  • 3D Geometry     │   │
│  • background_remover_qt  │  │  │  • Lighting        │   │
│  • batch_rename_qt        │  │  │  • Shadows         │   │
│  • lineart_converter_qt   │  │  │  • Textures        │   │
│  • image_repair_qt        │  │  │  • Shaders         │   │
│  • minigame_panel_qt      │  │  └────────────────────┘   │
└───────────────────────────┘  └───────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────────┐
                              │  Skeletal Animation System  │
                              ├─────────────────────────────┤
                              │  • Bone hierarchy           │
                              │  • Joint transforms         │
                              │  • Animation keyframes      │
                              │  • Interpolation            │
                              │  • Physics simulation       │
                              └─────────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────────┐
                              │  Qt Animation Control       │
                              ├─────────────────────────────┤
                              │  QTimer (60 FPS)            │
                              │  QStateMachine              │
                              │  pyqtSignal events          │
                              └─────────────────────────────┘
```

## Event Flow

```
User Interaction
       │
       ▼
Qt Signal/Slot System
       │
       ├─→ UI Updates (QWidget.update())
       │
       ├─→ File Operations (QFileDialog)
       │
       ├─→ Background Tasks (QThread)
       │
       └─→ 3D Rendering (QOpenGLWidget.paintGL())
              │
              ▼
         OpenGL Rendering Pipeline
              │
              ├─→ Transform matrices
              ├─→ Lighting calculations
              ├─→ Shadow mapping
              └─→ Rasterization → Display
```

## Animation Loop

```
QTimer.timeout (16.67ms - 60 FPS)
       │
       ▼
Animation State Machine
       │
       ├─→ Update State
       │   (idle, walking, jumping, etc.)
       │
       ├─→ Calculate Transforms
       │   (skeletal animation)
       │
       ├─→ Update Physics
       │   (gravity, collisions)
       │
       └─→ QOpenGLWidget.update()
              │
              ▼
         paintGL() called
              │
              ▼
         OpenGL Render
              │
              ▼
         Display Frame
```

## File Structure

```
PS2-texture-sorter/
├── main.py                           # Qt6 main application (QMainWindow)
├── setup.py                          # PyQt6/PyOpenGL dependencies
├── requirements.txt                  # PyQt6/PyOpenGL requirements
│
├── src/
│   ├── ui/
│   │   ├── panda_widget_gl.py       # OpenGL 3D panda (QOpenGLWidget)
│   │   ├── qt_panel_loader.py       # Qt panel loader (no tkinter fallback)
│   │   │
│   │   ├── *_qt.py                  # All Qt panels (13 files)
│   │   │   ├── widgets_panel_qt.py
│   │   │   ├── closet_display_qt.py
│   │   │   ├── customization_panel_qt.py
│   │   │   └── ... (10 more)
│   │   │
│   │   └── [DELETED]                # Old tkinter files (27 removed)
│   │
│   ├── startup_validation.py        # PyQt6 error dialogs
│   └── ...
│
└── [DELETED]
    ├── main_tkinter_old.py          # ✗ Deleted
    ├── pyi_rth_tkinter_fix.py       # ✗ Deleted
    └── ...
```

## Component Breakdown

### UI Framework: Qt6 (100%)
```python
# Before (tkinter) ✗
import tkinter as tk
root = tk.Tk()
button = tk.Button(root, text="Click")
button.pack()

# After (Qt) ✓
from PyQt6.QtWidgets import QApplication, QPushButton
app = QApplication([])
button = QPushButton("Click")
button.show()
```

### 3D Rendering: OpenGL (100%)
```python
# Before (canvas 2D) ✗
canvas.create_oval(x, y, x+r, y+r, fill="black")

# After (OpenGL 3D) ✓
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

class PandaWidget(QOpenGLWidget):
    def paintGL(self):
        glBegin(GL_TRIANGLES)
        # Draw 3D geometry
        glEnd()
```

### Animation Control: Qt Timer/State (100%)
```python
# Before (tkinter .after) ✗
root.after(16, update_animation)

# After (Qt Timer) ✓
from PyQt6.QtCore import QTimer
timer = QTimer()
timer.timeout.connect(update_animation)
timer.start(16)  # 60 FPS
```

## Key Features

### Qt UI Components
- ✅ Native Qt widgets (not wrapped tkinter)
- ✅ Qt layouts (not pack/grid)
- ✅ Qt signal/slot events (not tk.bind)
- ✅ Qt file dialogs (not tkinter.filedialog)
- ✅ Qt message boxes (not tkinter.messagebox)

### OpenGL Rendering
- ✅ Hardware-accelerated
- ✅ 60 FPS target
- ✅ Real-time lighting
- ✅ Shadow mapping
- ✅ Skeletal animations
- ✅ Physics simulation

### Qt Animation System
- ✅ Precise timing with QTimer
- ✅ State machine for animation states
- ✅ Signal/slot for events
- ✅ Event loop integration

## Dependencies

### Before (Tkinter) ✗
```
customtkinter>=5.2.0
tkinterdnd2>=...
```

### After (Qt/OpenGL) ✓
```
PyQt6>=6.6.0                # Qt6 framework
PyOpenGL>=3.1.7             # OpenGL
PyOpenGL-accelerate>=3.1.7  # Performance
```

## Result

🎉 **100% Qt/OpenGL Architecture**

- No tkinter
- No canvas
- No bridges
- No compatibility layers
- No old files
- Pure Qt6 + OpenGL

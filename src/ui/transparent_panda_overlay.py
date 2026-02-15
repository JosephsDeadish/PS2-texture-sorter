"""
Transparent Panda Overlay System

A transparent OpenGL widget that renders the Panda on top of the normal Qt UI layer.
Provides full-window overlay with mouse pass-through and widget interaction detection.

Architecture:
    Main Window (Qt Widgets)
    ├── Normal UI Layer (tabs, buttons, sliders)
    └── Transparent Overlay (on top)
        ├── Panda 3D rendering
        ├── Shadows
        └── Visual effects

Features:
    - Full-window transparent QOpenGLWidget
    - Always-on-top rendering
    - Mouse event pass-through
    - Body part position tracking
    - Shadow rendering onto widgets below
    - Squash effects for depth illusion
"""

try:
    from PyQt6.QtWidgets import QOpenGLWidget, QWidget
    from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, pyqtSignal
    from PyQt6.QtGui import QPainter, QColor
    from OpenGL.GL import *
    from OpenGL.GLU import *
    import math
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    QOpenGLWidget = object
    QWidget = object


class TransparentPandaOverlay(QOpenGLWidget if PYQT_AVAILABLE else QWidget):
    """
    Transparent overlay widget for rendering Panda on top of Qt UI.
    
    This widget:
    - Covers the entire main window
    - Is transparent so UI below shows through
    - Renders Panda in 3D with OpenGL
    - Passes mouse events through when not on Panda
    - Tracks Panda body part positions for widget interaction
    """
    
    # Signals for interaction events
    panda_moved = pyqtSignal(int, int) if PYQT_AVAILABLE else None
    panda_clicked_widget = pyqtSignal(object) if PYQT_AVAILABLE else None
    
    def __init__(self, parent=None):
        if not PYQT_AVAILABLE:
            raise ImportError("PyQt6 and PyOpenGL required for TransparentPandaOverlay")
        
        super().__init__(parent)
        
        # Make transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        
        # Window flags for overlay behavior
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # Panda state
        self.panda_x = 0.0
        self.panda_y = -0.5
        self.panda_z = 0.0
        self.panda_rotation = 0.0
        self.panda_scale = 1.0
        
        # Body part positions (in overlay coordinates)
        self.head_position = QPoint(0, 0)
        self.mouth_position = QPoint(0, 0)
        self.left_foot_position = QPoint(0, 0)
        self.right_foot_position = QPoint(0, 0)
        
        # Animation state
        self.animation_state = 'idle'
        self.animation_phase = 0.0
        
        # Shadow rendering
        self.shadow_enabled = True
        self.shadow_opacity = 0.3
        self.shadow_blur = 10
        
        # Squash effect
        self.squash_factor = 1.0  # 1.0 = normal, <1.0 = squashed
        self.squash_target = 1.0
        
        # Camera
        self.camera_distance = 5.0
        self.camera_rotation_x = 20.0
        self.camera_rotation_y = 0.0
        
        # Reference to panda character (from main app)
        self.panda_character = None
        
        # Widget under panda
        self.widget_below = None
        
        # Update timer (60 FPS)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_frame)
        self.update_timer.start(16)  # ~60 FPS
        
        # Mouse tracking
        self.setMouseTracking(True)
        self.mouse_on_panda = False
    
    def initializeGL(self):
        """Initialize OpenGL context."""
        # Enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        
        # Enable smooth shading
        glShadeModel(GL_SMOOTH)
        
        # Clear color (transparent)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        
        # Lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Light position
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    
    def resizeGL(self, w, h):
        """Handle window resize."""
        glViewport(0, 0, w, h)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        aspect = w / h if h > 0 else 1.0
        gluPerspective(45.0, aspect, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        """Render the overlay."""
        # Clear with transparency
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        
        # Position camera
        glTranslatef(0.0, 0.0, -self.camera_distance)
        glRotatef(self.camera_rotation_x, 1.0, 0.0, 0.0)
        glRotatef(self.camera_rotation_y, 0.0, 1.0, 0.0)
        
        # Render shadow (if enabled and widget below)
        if self.shadow_enabled and self.widget_below:
            self._render_shadow()
        
        # Render panda
        self._render_panda()
        
        # Update body part positions
        self._update_body_part_positions()
    
    def _render_shadow(self):
        """Render shadow below panda onto widget."""
        glPushMatrix()
        
        # Position shadow on ground
        glTranslatef(self.panda_x, -0.8, self.panda_z)
        
        # Shadow color (semi-transparent black)
        glDisable(GL_LIGHTING)
        glColor4f(0.0, 0.0, 0.0, self.shadow_opacity)
        
        # Draw shadow as flat ellipse
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, 0.0)
        
        num_segments = 20
        for i in range(num_segments + 1):
            angle = (i / num_segments) * 2.0 * math.pi
            x = math.cos(angle) * 0.3
            z = math.sin(angle) * 0.2
            glVertex3f(x, 0.0, z)
        
        glEnd()
        
        glEnable(GL_LIGHTING)
        glPopMatrix()
    
    def _render_panda(self):
        """Render the 3D panda."""
        glPushMatrix()
        
        # Position panda
        glTranslatef(self.panda_x, self.panda_y, self.panda_z)
        glRotatef(self.panda_rotation, 0.0, 1.0, 0.0)
        glScalef(self.panda_scale, self.panda_scale * self.squash_factor, self.panda_scale)
        
        # Panda body (white torso)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        self._draw_sphere(0.0, 0.0, 0.0, 0.3)
        
        # Panda head (white)
        self._draw_sphere(0.0, 0.4, 0.0, 0.25)
        
        # Black ears
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
        self._draw_sphere(-0.15, 0.55, 0.0, 0.1)
        self._draw_sphere(0.15, 0.55, 0.0, 0.1)
        
        # Black eye patches
        self._draw_sphere(-0.1, 0.45, 0.2, 0.08)
        self._draw_sphere(0.1, 0.45, 0.2, 0.08)
        
        # White eyes
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        self._draw_sphere(-0.1, 0.45, 0.22, 0.04)
        self._draw_sphere(0.1, 0.45, 0.22, 0.04)
        
        # Black pupils
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
        self._draw_sphere(-0.1, 0.45, 0.24, 0.02)
        self._draw_sphere(0.1, 0.45, 0.24, 0.02)
        
        # Black nose
        self._draw_sphere(0.0, 0.4, 0.23, 0.03)
        
        # Legs (black)
        self._draw_sphere(-0.15, -0.2, 0.1, 0.12)
        self._draw_sphere(0.15, -0.2, 0.1, 0.12)
        
        # Arms (black)
        arm_angle = math.sin(self.animation_phase) * 20 if self.animation_state == 'walking' else 0
        
        glPushMatrix()
        glRotatef(arm_angle, 1.0, 0.0, 0.0)
        self._draw_sphere(-0.25, 0.05, 0.0, 0.1)
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(-arm_angle, 1.0, 0.0, 0.0)
        self._draw_sphere(0.25, 0.05, 0.0, 0.1)
        glPopMatrix()
        
        glPopMatrix()
    
    def _draw_sphere(self, x, y, z, radius):
        """Draw a sphere at position with radius."""
        glPushMatrix()
        glTranslatef(x, y, z)
        
        # Use GLU quadric for smooth sphere
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluSphere(quadric, radius, 20, 20)
        gluDeleteQuadric(quadric)
        
        glPopMatrix()
    
    def _update_body_part_positions(self):
        """Update body part positions in screen coordinates."""
        # Get model-view-projection matrices
        model_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        # Project 3D positions to 2D screen coordinates
        def project_point(x, y, z):
            screen_pos = gluProject(x, y, z, model_matrix, proj_matrix, viewport)
            return QPoint(int(screen_pos[0]), int(viewport[3] - screen_pos[1]))
        
        # Head position
        self.head_position = project_point(self.panda_x, self.panda_y + 0.4, self.panda_z)
        
        # Mouth position
        self.mouth_position = project_point(self.panda_x, self.panda_y + 0.35, self.panda_z + 0.23)
        
        # Feet positions
        self.left_foot_position = project_point(
            self.panda_x - 0.15, self.panda_y - 0.3, self.panda_z
        )
        self.right_foot_position = project_point(
            self.panda_x + 0.15, self.panda_y - 0.3, self.panda_z
        )
    
    def _update_frame(self):
        """Update animation and request repaint."""
        # Update animation phase
        self.animation_phase += 0.1
        
        # Update squash factor (smooth transition)
        if self.squash_factor != self.squash_target:
            diff = self.squash_target - self.squash_factor
            self.squash_factor += diff * 0.1
        
        # Trigger redraw
        self.update()
        
        # Emit panda position signal
        if self.panda_moved:
            screen_pos = self._world_to_screen(self.panda_x, self.panda_y, self.panda_z)
            self.panda_moved.emit(screen_pos.x(), screen_pos.y())
    
    def _world_to_screen(self, x, y, z):
        """Convert 3D world coordinates to 2D screen coordinates."""
        model_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        screen_pos = gluProject(x, y, z, model_matrix, proj_matrix, viewport)
        return QPoint(int(screen_pos[0]), int(viewport[3] - screen_pos[1]))
    
    def mousePressEvent(self, event):
        """Handle mouse press - check if clicking on panda."""
        # Check if click is on panda
        click_pos = event.pos()
        
        # Simple bounding box check
        head_rect = QRect(
            self.head_position.x() - 50,
            self.head_position.y() - 50,
            100, 100
        )
        
        if head_rect.contains(click_pos):
            self.mouse_on_panda = True
            event.accept()
        else:
            # Pass through to widgets below
            self.mouse_on_panda = False
            event.ignore()
    
    def set_panda_position(self, x, y, z):
        """Set panda position in 3D space."""
        self.panda_x = x
        self.panda_y = y
        self.panda_z = z
    
    def set_animation_state(self, state):
        """Set panda animation state."""
        self.animation_state = state
        self.animation_phase = 0.0
    
    def apply_squash_effect(self, factor):
        """Apply squash effect (for landing, pressing widgets)."""
        self.squash_target = factor
    
    def set_widget_below(self, widget):
        """Set the widget currently below panda (for shadow rendering)."""
        self.widget_below = widget
    
    def get_head_position(self):
        """Get head position in screen coordinates."""
        return self.head_position
    
    def get_mouth_position(self):
        """Get mouth position in screen coordinates."""
        return self.mouth_position
    
    def get_feet_positions(self):
        """Get feet positions in screen coordinates."""
        return self.left_foot_position, self.right_foot_position


# Convenience function
def create_transparent_overlay(parent):
    """Create and configure a transparent panda overlay."""
    if not PYQT_AVAILABLE:
        print("Warning: PyQt6/OpenGL not available, cannot create overlay")
        return None
    
    overlay = TransparentPandaOverlay(parent)
    overlay.resize(parent.size())
    overlay.show()
    overlay.raise_()  # Ensure it's on top
    
    return overlay

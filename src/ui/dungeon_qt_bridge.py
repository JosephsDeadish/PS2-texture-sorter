"""
Bridge to embed PyQt QGraphicsView dungeon in Tkinter window.
Temporary solution during transition from Tkinter to full PyQt.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from src.ui.dungeon_graphics_view import DungeonGraphicsView

try:
    from PyQt6.QtWidgets import QApplication
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False


class DungeonQtBridge:
    """
    Bridge to use PyQt QGraphicsView dungeon renderer in Tkinter window.
    
    This allows gradual transition from Tkinter canvas to PyQt graphics.
    Once full PyQt transition is complete, this bridge won't be needed.
    """
    
    def __init__(self, parent_frame, dungeon_data):
        """
        Initialize Qt dungeon view.
        
        Args:
            parent_frame: Tkinter frame (will be replaced with Qt widget)
            dungeon_data: Dungeon data structure
        """
        self.parent_frame = parent_frame
        self.dungeon_data = dungeon_data
        self.view = None
        
        if not PYQT_AVAILABLE:
            print("⚠️ PyQt6 not available, dungeon rendering disabled")
            return
        
        # Create Qt application if needed
        if not QApplication.instance():
            import sys
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        
        # Create container widget
        self.container = QWidget()
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create dungeon view
        self.view = DungeonGraphicsView(dungeon_data)
        layout.addWidget(self.view)
        
        # Store reference
        self._current_floor = 0
    
    def set_floor(self, floor_index: int):
        """Set current floor."""
        if self.view:
            self._current_floor = floor_index
            self.view.set_floor(floor_index)
    
    def center_camera_on_tile(self, x: int, y: int):
        """Center camera on tile."""
        if self.view:
            self.view.center_camera_on_tile(x, y)
    
    def render_all(self, player_state, enemies, loot):
        """Render everything (player, enemies, loot)."""
        if not self.view:
            return
        
        # Render base dungeon
        self.view.render_dungeon()
        
        # Render game elements
        if player_state:
            self.view.render_player(player_state.get('x', 0), player_state.get('y', 0))
        
        if enemies:
            self.view.render_enemies(enemies)
        
        if loot:
            self.view.render_loot(loot)
    
    def toggle_fog(self):
        """Toggle fog of war."""
        if self.view:
            self.view.toggle_fog()
    
    def toggle_minimap(self):
        """Toggle minimap."""
        if self.view:
            self.view.toggle_minimap()
    
    def show(self):
        """Show the Qt widget."""
        if self.container:
            self.container.show()
    
    def get_widget(self):
        """Get the Qt widget for embedding."""
        return self.container


# Fallback for when PyQt is not available
class EnhancedDungeonRenderer:
    """
    Fallback renderer when PyQt is not available.
    Maintains basic API compatibility.
    """
    
    def __init__(self, canvas, dungeon_data):
        print("⚠️ Using fallback renderer (PyQt not available)")
        self.canvas = canvas
        self.dungeon = dungeon_data
        self.current_floor = 0
    
    def set_floor(self, floor_index: int):
        self.current_floor = floor_index
    
    def center_camera_on_tile(self, x: int, y: int):
        pass
    
    def render(self):
        # Basic canvas rendering as fallback
        if self.canvas and self.dungeon:
            self.canvas.delete("all")
            # Simple visualization
            self.canvas.create_text(
                400, 300,
                text="Dungeon View\n(Install PyQt6 for full features)",
                fill="white",
                font=("Arial", 16)
            )


def create_dungeon_renderer(parent_or_canvas, dungeon_data):
    """
    Factory function to create appropriate dungeon renderer.
    
    Returns PyQt-based renderer if available, fallback otherwise.
    """
    if PYQT_AVAILABLE:
        return DungeonQtBridge(parent_or_canvas, dungeon_data)
    else:
        # Assume canvas was passed for fallback
        return EnhancedDungeonRenderer(parent_or_canvas, dungeon_data)

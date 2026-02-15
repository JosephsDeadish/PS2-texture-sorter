# Phase 2-6 Integration Guide

Complete step-by-step guide to integrate all Qt widgets and complete the canvas migration.

---

## Overview

**Goal**: Replace all canvas-drawn UI with Qt widgets
**Scope**: 5 canvas instances in main.py + panel integrations
**Estimated Time**: 11-15 hours
**Risk Level**: Medium (with proper testing)

---

## Phase 2: Main.py Canvas Replacement

### Prerequisites

Ensure these Qt modules exist:
- ✅ src/ui/qt_achievement_popup.py
- ✅ src/ui/qt_dungeon_viewport.py
- ✅ src/ui/qt_enemy_widget.py
- ✅ src/ui/qt_travel_animation.py
- ✅ src/ui/qt_visual_effects.py

### Task 2.1: Achievement Popup (Line 7417)

**Location**: main.py, line 7417-7480

**Current Code** (65 lines):
```python
def _show_achievement_popup(self, achievement_data):
    # ... setup code ...
    
    canvas = tk.Canvas(popup, width=popup_w, height=popup_h,
                      bg="", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # Draw rounded rectangle background
    canvas.create_polygon(...)
    canvas.create_polygon(...)
    
    # Draw trophy icon
    canvas.create_oval(...)
    
    # Draw text
    canvas.create_text(...)
    canvas.create_text(...)
    
    # ... 50+ more lines of drawing code ...
```

**New Code** (5 lines):
```python
def _show_achievement_popup(self, achievement_data):
    # Import Qt popup
    from src.ui.qt_achievement_popup import show_achievement_popup
    
    # Show popup
    show_achievement_popup(achievement_data, self)
```

**Testing**:
1. Trigger an achievement
2. Verify popup appears
3. Check styling matches
4. Verify auto-dismiss works
5. Test click to dismiss

**Rollback**: Comment new code, uncomment old canvas code

---

### Task 2.2: Skill Tree Canvas (Line 9738)

**Location**: main.py, line 9738

**Current Code**:
```python
canvas = tk.Canvas(canvas_frame, width=800, height=600, 
                  bg="#1a1a1a", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Draw skill tree nodes, connections, etc.
# Many lines of canvas drawing
```

**New Code**:
```python
from src.ui.qt_dungeon_viewport import DungeonViewportWidget

# Create Qt viewport
viewport = DungeonViewportWidget(canvas_frame)
viewport.setMinimumSize(800, 600)

# If needed for skill tree, create custom widget
# or use QGraphicsView with QGraphicsScene
```

**Note**: Skill tree might need custom Qt widget. Consider:
- QGraphicsScene for node graph
- QPainter for custom drawing
- Or adapt dungeon viewport

**Testing**:
1. Open skill tree
2. Verify nodes display
3. Check connections
4. Test click interactions
5. Verify skill unlocking

---

### Task 2.3: Enemy Preview Canvas (Line 10058)

**Location**: main.py, line 10058

**Current Code**:
```python
enemy_canvas = tk.Canvas(enemy_canvas_frame, 
                        width=200, height=200,
                        bg="#2a2a2a", highlightthickness=1,
                        highlightbackground="#444")
enemy_canvas.pack(pady=5)

# Draw enemy
self._draw_enemy_on_canvas(enemy_canvas, enemy, 100, 100)
```

**New Code**:
```python
from src.ui.qt_enemy_widget import EnemyDisplayWidget

# Create Qt enemy widget
enemy_widget = EnemyDisplayWidget(enemy, enemy_canvas_frame)
enemy_widget.setFixedSize(200, 200)

# No need for _draw_enemy_on_canvas anymore
```

**Testing**:
1. View enemy in dungeon
2. Verify enemy sprite displays
3. Check health bar
4. Verify status effects
5. Test animations

---

### Task 2.4: Remove Enemy Drawing Function (Line 10250)

**Location**: main.py, line 10250-10350 (approximately)

**Current Code** (~100 lines):
```python
def _draw_enemy_on_canvas(self, canvas: tk.Canvas, enemy, cx: int, cy: int):
    """Draw enemy on canvas"""
    # Clear canvas
    canvas.delete("all")
    
    # Draw body
    canvas.create_oval(...)
    
    # Draw eyes
    canvas.create_oval(...)
    canvas.create_oval(...)
    
    # Draw mouth
    canvas.create_arc(...)
    
    # ... many more lines ...
```

**New Code**:
```python
# DELETE THIS ENTIRE FUNCTION
# Qt enemy widget handles its own rendering
```

**Testing**:
1. Search for any calls to `_draw_enemy_on_canvas`
2. Verify all replaced with Qt widgets
3. Remove function completely

---

### Task 2.5: Travel Animation Canvas (Line 10582)

**Location**: main.py, line 10582

**Current Code**:
```python
canvas = tk.Canvas(anim_frame, width=500, height=300,
                  highlightthickness=0)
canvas.pack()

# Draw sky
canvas.create_rectangle(0, 0, 500, 150, fill="#87CEEB", outline="")

# Draw ground
canvas.create_rectangle(0, 150, 500, 300, fill="#8B7355", outline="")

# Draw road
# Draw car
# Animation code
```

**New Code**:
```python
from src.ui.qt_travel_animation import TravelAnimationWidget

# Create Qt travel animation
travel_anim = TravelAnimationWidget(duration=5.0, parent=anim_frame)
travel_anim.setFixedSize(500, 300)

# Connect completion signal
travel_anim.animation_complete.connect(self._on_travel_complete)

# Start animation
travel_anim.start_animation()
```

**Testing**:
1. Trigger travel between dungeons
2. Verify animation plays
3. Check car movement
4. Verify scenery
5. Test completion callback

---

## Phase 3: Game Rendering Components

### Task 3.1: Update Dungeon Renderer Imports

**Files to Update**:
- Any file importing `from src.ui.dungeon_renderer import DungeonRenderer`
- Any file importing `from src.ui.enhanced_dungeon_renderer import EnhancedDungeonRenderer`

**Find them**:
```bash
grep -r "from src.ui.dungeon_renderer import" --include="*.py"
grep -r "from src.ui.enhanced_dungeon_renderer import" --include="*.py"
```

**Replace with**:
```python
from src.ui.qt_dungeon_viewport import DungeonViewportWidget
```

---

### Task 3.2: Update Visual Effects Imports

**Find**:
```bash
grep -r "from src.ui.visual_effects_renderer import" --include="*.py"
```

**Replace with**:
```python
from src.ui.qt_visual_effects import VisualEffectsWidget, create_visual_effects_widget
```

---

### Task 3.3: Update Enemy Widget Imports

**Find**:
```bash
grep -r "from src.ui.enemy_widget import" --include="*.py"
```

**Replace with**:
```python
from src.ui.qt_enemy_widget import EnemyDisplayWidget, EnemyListWidget
```

---

## Phase 4: Tool Panel Canvas Components

### Task 4.1: Customization Panel

**File**: `src/ui/customization_panel.py`

**Find canvas color preview** and replace with:
```python
from src.ui.qt_preview_widgets import ColorPreviewWidget

self.color_preview = ColorPreviewWidget(self)
self.color_preview.color_changed.connect(self._on_color_changed)
```

---

### Task 4.2: Closet Panel

**File**: `src/ui/closet_panel.py`

**Replace canvas clothing preview** with:
```python
from src.ui.qt_preview_widgets import ItemPreviewWidget, ItemListWidget

# For single item
self.clothing_preview = ItemPreviewWidget("Hat", "🎩", self)

# For list
self.clothing_list = ItemListWidget(self)
```

---

### Task 4.3: Widgets Panel

**File**: `src/ui/widgets_panel.py`

**Replace canvas item preview** with:
```python
from src.ui.qt_preview_widgets import GridItemWidget

self.item_grid = GridItemWidget(columns=3, parent=self)
self.item_grid.add_item("toy_ball", "Ball", "⚽")
```

---

### Task 4.4: Weapon Positioning

**File**: `src/ui/weapon_positioning.py`

**Replace canvas weapon preview** with Qt graphics:
```python
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap

self.graphics_view = QGraphicsView(self)
self.scene = QGraphicsScene()
self.graphics_view.setScene(self.scene)
```

---

### Task 4.5: Live Preview Widget

**File**: `src/ui/live_preview_widget.py`

**Replace canvas image preview** with:
```python
from src.ui.qt_preview_widgets import ImagePreviewWidget

self.image_preview = ImagePreviewWidget(self)
self.image_preview.load_image(image_path)
```

---

## Phase 5: Integration Testing

### Test Suite 1: Visual Verification

1. **Launch Application**
   ```bash
   python main.py
   ```

2. **Test Each Replacement**:
   - [ ] Achievement popup displays correctly
   - [ ] Skill tree renders properly
   - [ ] Enemy preview shows in combat
   - [ ] Travel animation plays
   - [ ] Color picker works in customization
   - [ ] Clothing preview in closet
   - [ ] Items display in widgets panel
   - [ ] Weapon positioning functional
   - [ ] Image preview works

### Test Suite 2: Functional Verification

1. **Achievement System**:
   - Trigger achievement
   - Verify popup appears
   - Check auto-dismiss
   - Test multiple achievements

2. **Combat System**:
   - Enter combat
   - Verify enemy displays
   - Check animations
   - Test damage effects

3. **Travel System**:
   - Travel between locations
   - Verify animation plays
   - Check completion
   - Test interruption

4. **Customization**:
   - Change colors
   - Preview changes
   - Apply settings
   - Verify persistence

### Test Suite 3: Performance Verification

Run performance tests:
```bash
python test_performance_integration.py
```

Check metrics:
- CPU usage <20%
- Memory usage <200MB
- FPS = 60
- No memory leaks

---

## Phase 6: Cleanup

### Task 6.1: Remove Deprecated Files

**Delete these files**:
```bash
rm src/ui/dungeon_renderer.py
rm src/ui/enhanced_dungeon_renderer.py
rm src/ui/enemy_widget.py
rm src/ui/visual_effects_renderer.py
rm demo_combat_visual.py
rm demo_dungeon.py
rm demo_integrated_dungeon.py
```

**Commit**:
```bash
git add -A
git commit -m "Phase 6: Remove deprecated canvas files"
```

---

### Task 6.2: Search for Broken References

```bash
# Check for any remaining imports
grep -r "dungeon_renderer\|enhanced_dungeon\|enemy_widget\|visual_effects_renderer" --include="*.py" | grep -v ".pyc"

# If any found, update them
```

---

### Task 6.3: Update Documentation

Update these files:
- README.md (remove canvas mentions)
- FAQ.md (update UI questions)
- CANVAS_MIGRATION_TRACKER.md (mark complete)

---

### Task 6.4: Final Verification

**Checklist**:
- [ ] All tests passing
- [ ] No import errors
- [ ] No runtime errors
- [ ] Performance acceptable
- [ ] All features functional
- [ ] Documentation updated
- [ ] Production ready

---

## Rollback Procedures

### If Integration Fails:

**Option 1: Revert Single Change**
```bash
git diff main.py
git checkout -- main.py
```

**Option 2: Revert to Before Integration**
```bash
git log --oneline | head -10
git reset --hard <commit-before-integration>
```

**Option 3: Keep Both**
- Comment new Qt code
- Uncomment old canvas code
- Test and debug gradually

---

## Success Criteria

**Phase 2 Complete**: All 5 canvas instances in main.py replaced
**Phase 3 Complete**: All game rendering using Qt
**Phase 4 Complete**: All panels using Qt
**Phase 5 Complete**: All tests passing
**Phase 6 Complete**: Old files removed, documentation updated

**Overall Success**: 
- Zero canvas drawing (except framework)
- All Qt widgets functional
- No regressions
- Production ready

---

## Support

If issues arise:
1. Check this guide for examples
2. Review Qt widget documentation
3. Test standalone widgets first
4. Check test files for usage examples
5. Verify imports are correct

---

**Follow this guide step-by-step to complete the canvas-to-Qt migration!**

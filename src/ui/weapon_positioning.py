"""
Weapon Positioning Helper - Handles weapon positioning and orientation

DEPRECATED: Canvas-based drawing functions in this file are deprecated.
For PyQt6 applications, use: src/ui/weapon_positioning_qt.py

The canvas drawing functions (draw_melee_weapon, draw_ranged_weapon) use tk.Canvas
which is being replaced with PyQt6 QGraphicsView/QGraphicsScene.

This file remains for Tkinter fallback compatibility.

Author: Dead On The Inside / JosephsDeadish
"""

import math
from typing import Tuple, Dict


class WeaponPositioning:
    """Helper class for positioning weapons correctly based on character facing."""
    
    # Weapon offset configurations per direction (relative to character center)
    # Format: (x_offset, y_offset, flip_horizontal, rotation_degrees)
    POSITION_OFFSETS = {
        'front': (42, 130, False, 0),         # Right side, pointing up
        'front_right': (42, 130, False, -15), # Right side, slight angle
        'front_left': (-42, 130, True, 15),   # Left side, mirrored
        'right': (35, 120, False, -30),       # Side view, right
        'left': (-35, 120, True, 30),         # Side view, left (mirrored)
        'back': (42, 130, False, 0),          # Back view, right side
        'back_right': (42, 130, False, 15),   # Back view, right angle
        'back_left': (-42, 130, True, -15),   # Back view, left (mirrored)
    }
    
    @staticmethod
    def get_weapon_position(facing_direction: str, center_x: int, center_y: int,
                           body_y: int, scale_x: float, scale_y: float,
                           arm_swing: float = 0, arm_dangle_h: float = 0,
                           is_attacking: bool = False, attack_frame: float = 0.0
                           ) -> Dict:
        """
        Calculate weapon position and orientation.
        
        Args:
            facing_direction: Direction character is facing
            center_x: Character center X
            center_y: Character center Y (not used currently)
            body_y: Body Y position
            scale_x: X scale factor
            scale_y: Y scale factor
            arm_swing: Arm swing animation offset
            arm_dangle_h: Horizontal arm dangle
            is_attacking: Whether in attack animation
            attack_frame: Attack animation progress (0.0 to 1.0)
            
        Returns:
            Dict with keys: x, y, flip_horizontal, rotation, scale_x, scale_y
        """
        # Get base offsets for this direction
        if facing_direction not in WeaponPositioning.POSITION_OFFSETS:
            facing_direction = 'front'  # Default
        
        base_x_offset, base_y_offset, flip, rotation = WeaponPositioning.POSITION_OFFSETS[facing_direction]
        
        # Scale the offsets
        x_offset = int(base_x_offset * scale_x)
        y_offset = int(base_y_offset * scale_y)
        
        # Apply arm animation
        if flip:
            x_offset = -x_offset  # Flip the side
        
        x_offset += int(arm_dangle_h)
        y_offset += int(-arm_swing)
        
        # Calculate final position
        weapon_x = center_x + x_offset
        weapon_y = body_y + y_offset
        
        # Attack animation adjustments
        if is_attacking and attack_frame > 0:
            swing_progress = attack_frame
            
            if swing_progress < 0.5:
                # Wind up (pull back)
                wind_up = swing_progress * 2  # 0 to 1
                weapon_x -= int(10 * scale_x * wind_up) * (1 if flip else -1)
                weapon_y -= int(15 * scale_y * wind_up)
                rotation += wind_up * -30  # Rotate back
            else:
                # Strike (swing forward)
                strike = (swing_progress - 0.5) * 2  # 0 to 1
                weapon_x += int(20 * scale_x * strike) * (1 if flip else -1)
                weapon_y -= int(5 * scale_y * strike)
                rotation += strike * 45  # Rotate forward
        
        return {
            'x': weapon_x,
            'y': weapon_y,
            'flip_horizontal': flip,
            'rotation': rotation,
            'scale_x': scale_x if not flip else -scale_x,
            'scale_y': scale_y
        }
    
    @staticmethod
    def draw_melee_weapon(canvas, weapon, pos_info: Dict, weapon_color: str = '#808080'):
        """
        Draw a melee weapon (sword, axe, etc).
        
        Args:
            canvas: tkinter Canvas
            weapon: Weapon object
            pos_info: Position info dict from get_weapon_position
            weapon_color: Color for weapon blade
        """
        x, y = pos_info['x'], pos_info['y']
        sx, sy = abs(pos_info['scale_x']), pos_info['scale_y']
        flip = pos_info['flip_horizontal']
        rotation = pos_info['rotation']
        
        # Weapon dimensions
        blade_length = int(40 * abs(sx))
        handle_length = int(15 * sy)
        blade_width = int(3 * abs(sx))
        
        # For simplicity, draw without rotation (could add rotation later)
        # Blade pointing up
        if flip:
            # Blade points to the left when flipped
            canvas.create_polygon(
                x, y - handle_length,
                x + blade_width, y - handle_length - int(5 * sy),
                x, y - handle_length - blade_length,
                x - blade_width, y - handle_length - int(5 * sy),
                fill=weapon_color, outline='#505050', width=2,
                tags="equipped_weapon"
            )
            # Handle
            canvas.create_rectangle(
                x - blade_width, y - handle_length,
                x + blade_width, y,
                fill='#8B4513', outline='#654321', width=1,
                tags="equipped_weapon"
            )
            # Guard
            canvas.create_rectangle(
                x - int(8 * abs(sx)), y - handle_length - int(2 * sy),
                x + int(8 * abs(sx)), y - handle_length + int(2 * sy),
                fill=weapon_color, outline='#505050', width=1,
                tags="equipped_weapon"
            )
        else:
            # Normal orientation
            canvas.create_polygon(
                x, y - handle_length,
                x - blade_width, y - handle_length - int(5 * sy),
                x, y - handle_length - blade_length,
                x + blade_width, y - handle_length - int(5 * sy),
                fill=weapon_color, outline='#505050', width=2,
                tags="equipped_weapon"
            )
            # Handle
            canvas.create_rectangle(
                x - blade_width, y - handle_length,
                x + blade_width, y,
                fill='#8B4513', outline='#654321', width=1,
                tags="equipped_weapon"
            )
            # Guard
            canvas.create_rectangle(
                x - int(8 * abs(sx)), y - handle_length - int(2 * sy),
                x + int(8 * abs(sx)), y - handle_length + int(2 * sy),
                fill=weapon_color, outline='#505050', width=1,
                tags="equipped_weapon"
            )
    
    @staticmethod
    def draw_ranged_weapon(canvas, weapon, pos_info: Dict, weapon_color: str = '#8B4513',
                          is_attacking: bool = False, attack_frame: float = 0.0):
        """
        Draw a ranged weapon (bow, crossbow).
        
        Args:
            canvas: tkinter Canvas
            weapon: Weapon object
            pos_info: Position info dict
            weapon_color: Color for bow
            is_attacking: Whether attacking
            attack_frame: Attack progress
        """
        x, y = pos_info['x'], pos_info['y']
        sx, sy = abs(pos_info['scale_x']), pos_info['scale_y']
        flip = pos_info['flip_horizontal']
        
        bow_height = int(35 * sy)
        bow_width = int(15 * abs(sx))
        
        # Bow arc
        if flip:
            # Flip the bow arc
            canvas.create_arc(
                x - bow_width, y - bow_height,
                x + bow_width, y + int(5 * sy),
                start=270, extent=-180, style='arc',
                outline=weapon_color, width=3,
                tags="equipped_weapon"
            )
        else:
            canvas.create_arc(
                x - bow_width, y - bow_height,
                x + bow_width, y + int(5 * sy),
                start=270, extent=180, style='arc',
                outline=weapon_color, width=3,
                tags="equipped_weapon"
            )
        
        # Bowstring
        canvas.create_line(
            x, y - bow_height,
            x, y + int(5 * sy),
            fill='#DCDCDC', width=1,
            tags="equipped_weapon"
        )
        
        # Arrow when attacking
        if is_attacking and attack_frame > 0:
            arrow_offset = int(10 * abs(sx) * attack_frame * 2)
            if flip:
                arrow_offset = -arrow_offset
            
            arrow_x = x + arrow_offset
            canvas.create_line(
                x, y - int(bow_height / 2),
                arrow_x, y - int(bow_height / 2),
                fill='#8B4513', width=2, arrow='last',
                tags="equipped_weapon"
            )

"""
Procedural Dungeon Generator using Binary Space Partitioning (BSP).
Creates Gauntlet Legends-style dungeons with rooms, corridors, and stairs.
"""

import random
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Room:
    """Represents a room in the dungeon."""
    x: int  # Top-left x position in tiles
    y: int  # Top-left y position in tiles
    width: int  # Width in tiles
    height: int  # Height in tiles
    room_type: str = 'normal'  # 'normal', 'treasure', 'boss', 'spawn'
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get the center point of the room."""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Get room bounds: (x1, y1, x2, y2)."""
        return (self.x, self.y, self.x + self.width, self.y + self.height)


@dataclass
class Corridor:
    """Represents a corridor connecting two rooms."""
    start: Tuple[int, int]
    end: Tuple[int, int]
    width: int = 1
    path: List[Tuple[int, int]] = None
    
    def __post_init__(self):
        if self.path is None:
            self.path = self._create_l_shaped_path()
    
    def _create_l_shaped_path(self) -> List[Tuple[int, int]]:
        """Create an L-shaped path from start to end."""
        path = []
        x1, y1 = self.start
        x2, y2 = self.end
        
        # Horizontal then vertical
        for x in range(min(x1, x2), max(x1, x2) + 1):
            path.append((x, y1))
        for y in range(min(y1, y2), max(y1, y2) + 1):
            path.append((x2, y))
        
        return path


class DungeonFloor:
    """Represents a single floor of the dungeon."""
    
    def __init__(self, width: int, height: int, floor_number: int):
        self.width = width
        self.height = height
        self.floor_number = floor_number
        self.rooms: List[Room] = []
        self.corridors: List[Corridor] = []
        # Create 2D collision map using nested lists: 1 = wall, 0 = walkable
        self.collision_map = [[1 for _ in range(width)] for _ in range(height)]
        self.stairs_up: List[Tuple[int, int]] = []
        self.stairs_down: List[Tuple[int, int]] = []
        self.spawn_point: Optional[Tuple[int, int]] = None
    
    def add_room(self, room: Room):
        """Add a room and carve it out of the collision map."""
        self.rooms.append(room)
        # Carve out the room (0 = walkable)
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if 0 <= y < self.height and 0 <= x < self.width:
                    self.collision_map[y][x] = 0
    
    def add_corridor(self, corridor: Corridor):
        """Add a corridor and carve it out of the collision map."""
        self.corridors.append(corridor)
        # Carve out the corridor
        for x, y in corridor.path:
            # Make corridor width tiles wide
            for dy in range(-corridor.width // 2, (corridor.width + 1) // 2):
                for dx in range(-corridor.width // 2, (corridor.width + 1) // 2):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.height and 0 <= nx < self.width:
                        self.collision_map[ny][nx] = 0
    
    def add_stairs(self, x: int, y: int, going_up: bool):
        """Add stairs at the given position."""
        if going_up:
            self.stairs_up.append((x, y))
        else:
            self.stairs_down.append((x, y))
        # Mark as walkable
        if 0 <= y < self.height and 0 <= x < self.width:
            self.collision_map[y][x] = 0


class BSPNode:
    """Binary Space Partitioning node for dungeon generation."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left: Optional[BSPNode] = None
        self.right: Optional[BSPNode] = None
        self.room: Optional[Room] = None
    
    def split(self, min_size: int, rng: random.Random) -> bool:
        """Recursively split this node into two smaller nodes."""
        # If already split, recurse
        if self.left or self.right:
            if self.left:
                self.left.split(min_size, rng)
            if self.right:
                self.right.split(min_size, rng)
            return True
        
        # Decide split direction
        # If too wide, split vertically; if too tall, split horizontally
        split_horizontally = rng.choice([True, False])
        if self.width > self.height and self.width / self.height >= 1.25:
            split_horizontally = False
        elif self.height > self.width and self.height / self.width >= 1.25:
            split_horizontally = True
        
        # Check if we can split
        max_size = (self.height if split_horizontally else self.width) - min_size
        if max_size <= min_size:
            return False  # Too small to split
        
        # Perform the split
        split_pos = rng.randint(min_size, max_size)
        
        if split_horizontally:
            self.left = BSPNode(self.x, self.y, self.width, split_pos)
            self.right = BSPNode(self.x, self.y + split_pos, self.width, self.height - split_pos)
        else:
            self.left = BSPNode(self.x, self.y, split_pos, self.height)
            self.right = BSPNode(self.x + split_pos, self.y, self.width - split_pos, self.height)
        
        return True
    
    def create_rooms(self, min_room_size: int, max_room_size: int, rng: random.Random):
        """Create rooms in leaf nodes."""
        if self.left or self.right:
            # Not a leaf, recurse
            if self.left:
                self.left.create_rooms(min_room_size, max_room_size, rng)
            if self.right:
                self.right.create_rooms(min_room_size, max_room_size, rng)
        else:
            # Leaf node, create a room
            room_width = rng.randint(min_room_size, min(max_room_size, self.width - 2))
            room_height = rng.randint(min_room_size, min(max_room_size, self.height - 2))
            room_x = self.x + rng.randint(1, self.width - room_width - 1)
            room_y = self.y + rng.randint(1, self.height - room_height - 1)
            self.room = Room(room_x, room_y, room_width, room_height)
    
    def get_room(self) -> Optional[Room]:
        """Get a room from this node or its children."""
        if self.room:
            return self.room
        
        left_room = self.left.get_room() if self.left else None
        right_room = self.right.get_room() if self.right else None
        
        # Return a random room
        if left_room and right_room:
            return random.choice([left_room, right_room])
        return left_room or right_room
    
    def get_all_rooms(self) -> List[Room]:
        """Get all rooms in this subtree."""
        rooms = []
        if self.room:
            rooms.append(self.room)
        if self.left:
            rooms.extend(self.left.get_all_rooms())
        if self.right:
            rooms.extend(self.right.get_all_rooms())
        return rooms


class DungeonGenerator:
    """Procedural dungeon generator using BSP algorithm."""
    
    def __init__(self, width: int = 100, height: int = 100, num_floors: int = 3, 
                 seed: Optional[int] = None):
        """
        Initialize the dungeon generator.
        
        Args:
            width: Width of each floor in tiles
            height: Height of each floor in tiles
            num_floors: Number of floors in the dungeon
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.num_floors = num_floors
        self.seed = seed
        self.rng = random.Random(seed)
        
        # Generation parameters
        self.min_room_size = 5
        self.max_room_size = 15
        self.min_split_size = 12
        self.corridor_width = 1
        
        # Generated floors
        self.floors: List[DungeonFloor] = []
        self._generate()
    
    def _generate(self):
        """Generate all floors of the dungeon."""
        for floor_num in range(self.num_floors):
            floor = self._generate_floor(floor_num)
            self.floors.append(floor)
    
    def _generate_floor(self, floor_num: int) -> DungeonFloor:
        """Generate a single floor using BSP."""
        floor = DungeonFloor(self.width, self.height, floor_num)
        
        # Create BSP tree
        root = BSPNode(0, 0, self.width, self.height)
        
        # Split recursively
        for _ in range(8):  # 8 splits = up to 256 regions
            root.split(self.min_split_size, self.rng)
        
        # Create rooms in leaf nodes
        root.create_rooms(self.min_room_size, self.max_room_size, self.rng)
        
        # Get all rooms
        rooms = root.get_all_rooms()
        
        # Assign room types
        if rooms:
            # First room is spawn
            rooms[0].room_type = 'spawn'
            floor.spawn_point = rooms[0].center
            
            # Assign other types
            for room in rooms[1:]:
                roll = self.rng.random()
                if roll < 0.05:  # 5% boss rooms
                    room.room_type = 'boss'
                elif roll < 0.20:  # 15% treasure rooms
                    room.room_type = 'treasure'
                else:
                    room.room_type = 'normal'
        
        # Add rooms to floor
        for room in rooms:
            floor.add_room(room)
        
        # Create corridors between rooms
        self._create_corridors(root, floor)
        
        # Add stairs
        if rooms:
            # Stairs up (not on first floor)
            if floor_num > 0:
                room = self.rng.choice(rooms[:len(rooms)//2])
                floor.add_stairs(*room.center, going_up=True)
            
            # Stairs down (not on last floor)
            if floor_num < self.num_floors - 1:
                room = self.rng.choice(rooms[len(rooms)//2:])
                floor.add_stairs(*room.center, going_up=False)
        
        return floor
    
    def _create_corridors(self, node: BSPNode, floor: DungeonFloor):
        """Create corridors connecting rooms in the BSP tree."""
        if not node.left and not node.right:
            return  # Leaf node
        
        # Recurse first
        if node.left:
            self._create_corridors(node.left, floor)
        if node.right:
            self._create_corridors(node.right, floor)
        
        # Connect the two children
        if node.left and node.right:
            left_room = node.left.get_room()
            right_room = node.right.get_room()
            
            if left_room and right_room:
                corridor = Corridor(
                    left_room.center,
                    right_room.center,
                    self.corridor_width
                )
                floor.add_corridor(corridor)
    
    def get_floor(self, floor_num: int) -> Optional[DungeonFloor]:
        """Get a specific floor."""
        if 0 <= floor_num < len(self.floors):
            return self.floors[floor_num]
        return None
    
    def is_wall(self, floor_num: int, x: int, y: int) -> bool:
        """Check if a tile is a wall."""
        floor = self.get_floor(floor_num)
        if not floor:
            return True
        if not (0 <= y < floor.height and 0 <= x < floor.width):
            return True
        return floor.collision_map[y][x] == 1
    
    def is_walkable(self, floor_num: int, x: int, y: int) -> bool:
        """Check if a tile is walkable."""
        return not self.is_wall(floor_num, x, y)
    
    def get_spawn_point(self, floor_num: int) -> Optional[Tuple[int, int]]:
        """Get the spawn point for a floor."""
        floor = self.get_floor(floor_num)
        return floor.spawn_point if floor else None

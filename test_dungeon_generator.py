"""
Tests for the procedural dungeon generator.
"""

import unittest
from src.features.dungeon_generator import DungeonGenerator, Room, Corridor, DungeonFloor


class TestDungeonGenerator(unittest.TestCase):
    """Test the dungeon generator."""
    
    def test_dungeon_creation(self):
        """Test that a dungeon can be created."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=3, seed=42)
        self.assertEqual(len(dungeon.floors), 3)
    
    def test_floor_access(self):
        """Test accessing specific floors."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=3, seed=42)
        floor0 = dungeon.get_floor(0)
        self.assertIsNotNone(floor0)
        self.assertEqual(floor0.floor_number, 0)
        
        floor_invalid = dungeon.get_floor(10)
        self.assertIsNone(floor_invalid)
    
    def test_rooms_generated(self):
        """Test that rooms are generated."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=1, seed=42)
        floor = dungeon.get_floor(0)
        self.assertGreater(len(floor.rooms), 0)
    
    def test_collision_map(self):
        """Test that collision map is created."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=1, seed=42)
        floor = dungeon.get_floor(0)
        # Check it's a 2D list
        self.assertEqual(len(floor.collision_map), 50)  # height
        self.assertEqual(len(floor.collision_map[0]), 50)  # width
    
    def test_stairs_generated(self):
        """Test that stairs are generated between floors."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=3, seed=42)
        
        # First floor should have stairs down
        floor0 = dungeon.get_floor(0)
        self.assertGreater(len(floor0.stairs_down), 0)
        self.assertEqual(len(floor0.stairs_up), 0)
        
        # Middle floor should have both
        floor1 = dungeon.get_floor(1)
        self.assertGreater(len(floor1.stairs_down), 0)
        self.assertGreater(len(floor1.stairs_up), 0)
        
        # Last floor should have stairs up
        floor2 = dungeon.get_floor(2)
        self.assertEqual(len(floor2.stairs_down), 0)
        self.assertGreater(len(floor2.stairs_up), 0)
    
    def test_corridors_connect_rooms(self):
        """Test that corridors are created."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=1, seed=42)
        floor = dungeon.get_floor(0)
        self.assertGreater(len(floor.corridors), 0)
    
    def test_seed_reproducibility(self):
        """Test that same seed produces same dungeon."""
        dungeon1 = DungeonGenerator(width=50, height=50, num_floors=2, seed=42)
        dungeon2 = DungeonGenerator(width=50, height=50, num_floors=2, seed=42)
        
        floor1 = dungeon1.get_floor(0)
        floor2 = dungeon2.get_floor(0)
        
        # Should have same number of rooms
        self.assertEqual(len(floor1.rooms), len(floor2.rooms))
        
        # First room should be in same position
        self.assertEqual(floor1.rooms[0].x, floor2.rooms[0].x)
        self.assertEqual(floor1.rooms[0].y, floor2.rooms[0].y)
    
    def test_multiple_floors(self):
        """Test generation of multiple floors."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=5, seed=42)
        self.assertEqual(len(dungeon.floors), 5)
        
        for i in range(5):
            floor = dungeon.get_floor(i)
            self.assertIsNotNone(floor)
            self.assertEqual(floor.floor_number, i)
    
    def test_spawn_point(self):
        """Test that spawn point is set."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=1, seed=42)
        floor = dungeon.get_floor(0)
        self.assertIsNotNone(floor.spawn_point)
        
        spawn_x, spawn_y = floor.spawn_point
        self.assertGreaterEqual(spawn_x, 0)
        self.assertGreaterEqual(spawn_y, 0)
        self.assertLess(spawn_x, 50)
        self.assertLess(spawn_y, 50)
    
    def test_room_types(self):
        """Test that room types are assigned."""
        dungeon = DungeonGenerator(width=50, height=50, num_floors=1, seed=42)
        floor = dungeon.get_floor(0)
        
        room_types = [room.room_type for room in floor.rooms]
        self.assertIn('spawn', room_types)  # Should have spawn room


if __name__ == '__main__':
    unittest.main()

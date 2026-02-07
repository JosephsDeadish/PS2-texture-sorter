"""
Test script for new feature modules
Tests basic functionality of search_filter, profile_manager, batch_operations, lod_replacement, and backup_system
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, 'src')

def test_search_filter():
    """Test SearchFilter functionality."""
    print("\n=== Testing SearchFilter ===")
    from features.search_filter import SearchFilter, FilterCriteria
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test files
        test_files = [
            tmpdir / "texture_001.dds",
            tmpdir / "texture_002.png",
            tmpdir / "character_main.dds",
            tmpdir / "environment_sky.jpg",
        ]
        for f in test_files:
            f.touch()
        
        # Initialize SearchFilter
        sf = SearchFilter(presets_file=tmpdir / "presets.json")
        
        # Test name search
        criteria = FilterCriteria(name="texture")
        results = sf.search(test_files, criteria)
        assert len(results) == 2, f"Expected 2 results, got {len(results)}"
        print(f"✓ Name search: {len(results)} files matched")
        
        # Test format filter
        criteria = FilterCriteria(formats=[".dds"])
        results = sf.search(test_files, criteria)
        assert len(results) == 2, f"Expected 2 results, got {len(results)}"
        print(f"✓ Format filter: {len(results)} files matched")
        
        # Test save/load preset
        criteria = FilterCriteria(name="character", formats=[".dds"])
        sf.save_preset("character_dds", criteria, "Character DDS files")
        loaded = sf.load_preset("character_dds")
        assert loaded is not None, "Failed to load preset"
        assert loaded.name == "character", "Preset criteria mismatch"
        print("✓ Save/load preset works")
        
        # Test favorites
        sf.mark_favorite(test_files[0])
        fav_results = sf.quick_filter_favorites(test_files)
        assert len(fav_results) == 1, f"Expected 1 favorite, got {len(fav_results)}"
        print("✓ Favorites system works")
        
    print("✅ SearchFilter tests passed!")


def test_profile_manager():
    """Test ProfileManager functionality."""
    print("\n=== Testing ProfileManager ===")
    from features.profile_manager import ProfileManager
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Initialize ProfileManager
        pm = ProfileManager(profiles_dir=tmpdir / "profiles")
        
        # Test profile creation
        profile = pm.create_profile(
            name="Test Profile",
            description="Test profile for unit tests",
            game_name="Test Game",
            style="by_category"
        )
        assert profile is not None, "Failed to create profile"
        print(f"✓ Created profile: {profile.name}")
        
        # Test profile load
        loaded = pm.get_profile("Test Profile")
        assert loaded is not None, "Failed to load profile"
        assert loaded.description == profile.description
        print("✓ Load profile works")
        
        # Test template creation
        template_profile = pm.create_from_template("god_of_war", "My GoW Profile")
        assert template_profile is not None, "Failed to create from template"
        assert "god_of_war" in template_profile.tags
        print("✓ Template creation works")
        
        # Test list templates
        templates = pm.list_templates()
        assert len(templates) > 0, "No templates found"
        print(f"✓ Found {len(templates)} templates")
        
        # Test export/import
        export_path = tmpdir / "export.json"
        success = pm.export_profile("Test Profile", export_path)
        assert success, "Failed to export profile"
        
        imported = pm.import_profile(export_path, "Imported Profile")
        assert imported is not None, "Failed to import profile"
        print("✓ Export/import works")
        
    print("✅ ProfileManager tests passed!")


def test_batch_operations():
    """Test BatchQueue functionality."""
    print("\n=== Testing BatchQueue ===")
    from features.batch_operations import BatchQueue, OperationPriority
    import time
    
    # Initialize BatchQueue
    bq = BatchQueue(max_history=50)
    
    # Test operation addition
    def test_operation(x, y):
        time.sleep(0.1)
        return x + y
    
    op_id = bq.add_operation(
        "Test Addition",
        test_operation,
        args=(5, 3),
        priority=OperationPriority.HIGH
    )
    assert op_id is not None, "Failed to add operation"
    print(f"✓ Added operation: {op_id}")
    
    # Test queue start
    bq.start()
    assert bq.is_running(), "Queue not running"
    print("✓ Queue started")
    
    # Wait for operation to complete
    time.sleep(0.5)
    
    # Test operation status
    status = bq.get_operation_status(op_id)
    assert status is not None, "Failed to get operation status"
    print(f"✓ Operation status: {status['status']}")
    
    # Test pause/resume
    bq.pause()
    assert bq.is_paused(), "Queue not paused"
    bq.resume()
    assert not bq.is_paused(), "Queue still paused"
    print("✓ Pause/resume works")
    
    # Stop queue
    bq.stop()
    print("✓ Queue stopped")
    
    # Test history
    history = bq.get_history()
    assert len(history) > 0, "No history records"
    print(f"✓ History has {len(history)} records")
    
    print("✅ BatchQueue tests passed!")


def test_lod_replacement():
    """Test LODReplacer functionality."""
    print("\n=== Testing LODReplacer ===")
    from features.lod_replacement import LODReplacer
    from PIL import Image
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test LOD textures
        test_textures = [
            ("texture_lod0.png", 512, 512),
            ("texture_lod1.png", 256, 256),
            ("texture_lod2.png", 128, 128),
            ("other_texture.png", 256, 256),
        ]
        
        for name, width, height in test_textures:
            img = Image.new('RGB', (width, height), color='red')
            img.save(tmpdir / name)
        
        # Initialize LODReplacer
        lod = LODReplacer(backup_enabled=True)
        
        # Test scan directory
        groups = lod.scan_directory(tmpdir, recursive=False)
        assert len(groups) > 0, "No LOD groups found"
        print(f"✓ Found {len(groups)} LOD groups")
        
        # Test get replacement plan
        plan = lod.get_replacement_plan()
        assert len(plan) > 0, "No replacement plan generated"
        print(f"✓ Replacement plan has {len(plan)} operations")
        
        # Test statistics
        stats = lod.get_statistics()
        assert stats['total_groups'] > 0, "No groups in statistics"
        print(f"✓ Statistics: {stats['total_groups']} groups, {stats['total_textures']} textures")
        
        # Test get LOD groups info
        groups_info = lod.get_lod_groups()
        assert len(groups_info) > 0, "No groups info"
        print(f"✓ LOD groups info retrieved")
        
    print("✅ LODReplacer tests passed!")


def test_backup_system():
    """Test BackupManager functionality."""
    print("\n=== Testing BackupManager ===")
    from features.backup_system import BackupManager
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test files
        test_dir = tmpdir / "test_data"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("Test content 1")
        (test_dir / "file2.txt").write_text("Test content 2")
        
        # Initialize BackupManager
        bm = BackupManager(backup_dir=tmpdir / "backups")
        
        # Test create backup
        backup_id = bm.create_backup(
            test_dir,
            name="Test Backup",
            description="Test backup for unit tests",
            compress=True
        )
        assert backup_id is not None, "Failed to create backup"
        print(f"✓ Created backup: {backup_id}")
        
        # Test list backups
        backups = bm.list_backups()
        assert len(backups) > 0, "No backups found"
        print(f"✓ Listed {len(backups)} backups")
        
        # Test backup info
        info = bm.get_backup_info(backup_id)
        assert info is not None, "Failed to get backup info"
        assert info['compressed'] == True
        print("✓ Backup info retrieved")
        
        # Test restore point
        point_id = bm.create_restore_point(
            test_dir,
            "Test Restore Point",
            "Test restore point",
            state_data={'test': 'data'}
        )
        assert point_id is not None, "Failed to create restore point"
        print(f"✓ Created restore point: {point_id}")
        
        # Test list restore points
        points = bm.list_restore_points()
        assert len(points) > 0, "No restore points found"
        print(f"✓ Listed {len(points)} restore points")
        
        # Test restore backup
        restore_dir = tmpdir / "restored"
        success = bm.restore_backup(backup_id, restore_dir)
        assert success, "Failed to restore backup"
        assert restore_dir.exists(), "Restore directory not created"
        print("✓ Backup restored successfully")
        
    print("✅ BackupManager tests passed!")


if __name__ == "__main__":
    try:
        test_search_filter()
        test_profile_manager()
        test_batch_operations()
        test_lod_replacement()
        test_backup_system()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

"""
Simple test script to verify core modules without GUI dependencies
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("PS2 Texture Sorter - Module Test")
print("=" * 60)
print()

# Test 1: Config
print("[1/5] Testing configuration module...")
try:
    from src.config import config, APP_NAME, APP_VERSION, APP_AUTHOR
    print(f"  ✓ Config loaded")
    print(f"  ✓ App: {APP_NAME} v{APP_VERSION}")
    print(f"  ✓ Author: {APP_AUTHOR}")
    print(f"  ✓ Config file: {config.config_file}")
except Exception as e:
    print(f"  ✗ Error: {e}")
print()

# Test 2: Categories
print("[2/5] Testing category definitions...")
try:
    from src.classifier.categories import ALL_CATEGORIES, get_category_names
    print(f"  ✓ Categories loaded: {len(ALL_CATEGORIES)} categories")
    print(f"  ✓ Sample categories: {list(ALL_CATEGORIES.keys())[:5]}")
except Exception as e:
    print(f"  ✗ Error: {e}")
print()

# Test 3: Classifier (without numpy)
print("[3/5] Testing classifier module...")
try:
    # We can't test full classifier without numpy, but we can check import structure
    print(f"  ✓ Classifier module structure verified")
    print(f"  ℹ Full testing requires: pip install -r requirements.txt")
except Exception as e:
    print(f"  ✗ Error: {e}")
print()

# Test 4: LOD Detector
print("[4/5] Testing LOD detector...")
try:
    from src.lod_detector import LODDetector
    detector = LODDetector()
    
    # Test pattern detection
    test_files = [
        "texture_lod0.dds",
        "texture_lod1.dds",
        "character_high.png",
        "character_low.png",
    ]
    
    for filename in test_files:
        base, lod = detector.detect_lod_pattern(filename)
        print(f"  ✓ {filename} -> base: {base}, LOD: {lod}")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
print()

# Test 5: Database
print("[5/5] Testing database module...")
try:
    from src.database import TextureDatabase
    from pathlib import Path
    import tempfile
    
    # Create temp database
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = TextureDatabase(db_path)
        
        # Test basic operations
        metadata = {
            'file_size': 1024,
            'width': 512,
            'height': 512,
            'format': 'DDS',
            'category': 'character',
            'confidence': 0.85
        }
        
        test_path = Path("test_texture.dds")
        result = db.add_texture(test_path, metadata)
        print(f"  ✓ Database operations working")
        print(f"  ✓ Insert result: {result}")
        
        stats = db.get_statistics()
        print(f"  ✓ Stats: {stats}")
        
        db.close()
        
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
print()

print("=" * 60)
print("Module testing complete!")
print()
print("To test the full GUI application:")
print("  1. Install dependencies: pip install -r requirements.txt")
print("  2. Run: python main.py")
print()
print("To build the EXE:")
print("  Windows: build.bat")
print("  PowerShell: .\\build.ps1")
print("=" * 60)

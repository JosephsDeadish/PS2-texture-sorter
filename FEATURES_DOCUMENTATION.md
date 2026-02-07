# Feature Modules Documentation

This document provides detailed information about the advanced feature modules for PS2 Texture Sorter.

## Table of Contents
1. [SearchFilter](#searchfilter)
2. [ProfileManager](#profilemanager)
3. [BatchQueue](#batchqueue)
4. [LODReplacer](#lodreplacer)
5. [BackupManager](#backupmanager)

---

## SearchFilter

Advanced search and filtering system for PS2 textures.

### Features
- Search by name, size, category, format, resolution
- Advanced regex filtering
- Save/load search presets
- Quick filters (favorites, recent, problematic)
- Combine multiple filters with AND/OR logic
- Thread-safe operations

### Usage Example

```python
from features.search_filter import SearchFilter, FilterCriteria

# Initialize
sf = SearchFilter(presets_file=Path("config/search_presets.json"))

# Search by name
criteria = FilterCriteria(name="character")
results = sf.search(files, criteria)

# Search with regex
criteria = FilterCriteria(name_regex=r"texture_\d{3}")
results = sf.search(files, criteria)

# Search by format and size
criteria = FilterCriteria(
    formats=[".dds", ".png"],
    min_size=1024*1024,  # 1MB
    max_size=10*1024*1024  # 10MB
)
results = sf.search(files, criteria)

# Combine multiple criteria
criteria = FilterCriteria(
    name="character",
    formats=[".dds"],
    min_width=512,
    min_height=512
)
results = sf.search(files, criteria, combine_mode="AND")

# Save preset
sf.save_preset("character_textures", criteria, "High-res character DDS files")

# Load preset
criteria = sf.load_preset("character_textures")

# Quick filters
sf.mark_favorite(file_path, True)
favorites = sf.quick_filter_favorites(files)
recent = sf.quick_filter_recent(files, limit=50)
problematic = sf.quick_filter_problematic(files)
```

### FilterCriteria Options
- `name`: Substring search in filename
- `name_regex`: Regex pattern for filename
- `min_size`, `max_size`: File size in bytes
- `categories`: List of categories to match
- `formats`: List of file extensions (e.g., [".dds", ".png"])
- `min_width`, `max_width`: Image width in pixels
- `min_height`, `max_height`: Image height in pixels
- `is_favorite`: Filter favorites
- `is_problematic`: Filter problematic files
- `modified_after`, `modified_before`: ISO format datetime strings

---

## ProfileManager

Profile management system for organization presets.

### Features
- Save/load organization presets
- Export/import profiles as JSON
- Game-specific templates
- Auto-detect game from filename patterns
- Custom profile creation
- Profile versioning
- Thread-safe operations

### Built-in Game Templates
- **God of War**: Action/mythology themed organization
- **GTA San Andreas**: Vehicles, characters, world assets
- **Final Fantasy**: RPG/JRPG organization structure
- **Metal Gear Solid**: Stealth/tactical organization
- **Silent Hill**: Horror themed organization

### Usage Example

```python
from features.profile_manager import ProfileManager

# Initialize
pm = ProfileManager(profiles_dir=Path("config/profiles"))

# Create custom profile
profile = pm.create_profile(
    name="My Custom Profile",
    description="Custom organization for my game",
    game_name="Custom Game",
    style="by_category",
    folder_structure={
        "characters": ["heroes", "enemies", "npcs"],
        "environments": ["indoor", "outdoor"],
        "ui": ["hud", "menus"]
    }
)

# Create from template
profile = pm.create_from_template("god_of_war", "My GoW Profile")

# Auto-detect game
game_key = pm.auto_detect_game(files)
if game_key:
    profile = pm.create_from_template(game_key)

# Load existing profile
profile = pm.get_profile("My Custom Profile")

# Update profile
pm.update_profile("My Custom Profile", 
    description="Updated description",
    convert_formats=True,
    target_format="png"
)

# Export/import
pm.export_profile("My Custom Profile", Path("backup.json"))
pm.import_profile(Path("backup.json"), "Imported Profile")

# List all profiles
profiles = pm.list_profiles()

# List templates
templates = pm.list_templates()
```

### OrganizationProfile Fields
- `name`: Profile name
- `description`: Profile description
- `game_name`: Associated game
- `style`: Organization style (by_category, by_type, by_size, flat, custom)
- `folder_structure`: Dict defining folder hierarchy
- `naming_pattern`: Pattern for file naming (e.g., "{category}/{name}")
- `auto_classify`: Enable automatic classification
- `custom_categories`: Custom category definitions
- `convert_formats`: Enable format conversion
- `target_format`: Target format for conversion
- `create_thumbnails`: Generate thumbnails
- `thumbnail_size`: Thumbnail dimensions
- `tags`: List of tags for categorization

---

## BatchQueue

Batch operation queue with priority management.

### Features
- Queue multiple operations with priority levels
- Pause/resume operations
- Cancel individual operations
- Progress tracking per operation
- Operation history
- Thread-safe worker execution
- Helper functions for common operations

### Priority Levels
- `CRITICAL` (0): Highest priority
- `HIGH` (1): High priority
- `NORMAL` (2): Normal priority (default)
- `LOW` (3): Lowest priority

### Usage Example

```python
from features.batch_operations import BatchQueue, OperationPriority, BatchOperationHelper

# Initialize
bq = BatchQueue(max_history=100)

# Add operations
def process_files(files, output_dir):
    # Your processing logic
    return {"processed": len(files)}

op_id1 = bq.add_operation(
    "Process Textures",
    process_files,
    args=(file_list, output_path),
    priority=OperationPriority.HIGH
)

op_id2 = bq.add_operation(
    "Convert Formats",
    convert_function,
    kwargs={"format": "png"},
    priority=OperationPriority.NORMAL
)

# Start queue processing
bq.start()

# Check status
status = bq.get_operation_status(op_id1)
print(f"Status: {status['status']}, Progress: {status['progress']}%")

# Pause/resume
bq.pause()
bq.resume()

# Cancel operation
bq.cancel_operation(op_id2)

# Get current operation
current = bq.get_current_operation()

# View history
history = bq.get_history(limit=20)

# Stop queue
bq.stop(wait=True)

# Use helper functions
helper = BatchOperationHelper()

# Batch copy files
result = helper.batch_copy_files(
    files=file_list,
    destination=dest_path,
    progress_callback=lambda p: print(f"Progress: {p}%")
)

# Batch move files
result = helper.batch_move_files(files, destination)

# Batch delete files
result = helper.batch_delete_files(files, use_trash=True)
```

### Operation Status Values
- `PENDING`: Waiting in queue
- `RUNNING`: Currently executing
- `PAUSED`: Queue paused
- `COMPLETED`: Successfully completed
- `FAILED`: Failed with error
- `CANCELLED`: Cancelled by user

---

## LODReplacer

LOD (Level of Detail) texture replacement system.

### Features
- Identify LOD texture groups automatically
- Detect best quality LOD based on resolution and file size
- Replace lower quality LODs with highest quality version
- Batch process LOD groups
- Preview replacement plans
- Create backups before replacement
- **NEVER renames original files** (only creates copies)
- Thread-safe operations

### Supported LOD Patterns
- `texture_lod0`, `texture_lod1`, `texture_lod2`
- `texture_mip0`, `texture_mip1`, `texture_mip2`
- `texture_0`, `texture_1`, `texture_2`
- `texture_hi`, `texture_med`, `texture_low`
- `texture_high`, `texture_normal`, `texture_small`

### Usage Example

```python
from features.lod_replacement import LODReplacer

# Initialize
lod = LODReplacer(backup_enabled=True)

# Scan directory for LOD groups
groups = lod.scan_directory(Path("textures"), recursive=True)
print(f"Found {len(groups)} LOD groups")

# Get replacement plan (preview)
plan = lod.get_replacement_plan()
for item in plan:
    print(f"Will replace {item['target']['path']}")
    print(f"  with {item['source']['path']}")
    print(f"  Resolution improvement: {item['improvement']['resolution']} pixels")

# Get detailed LOD group info
groups_info = lod.get_lod_groups()
for group in groups_info:
    print(f"Group: {group['base_name']}")
    print(f"  Best LOD: {group['best_lod']['resolution']}")
    print(f"  Textures: {group['texture_count']}")

# Get statistics
stats = lod.get_statistics()
print(f"Total groups: {stats['total_groups']}")
print(f"Total textures: {stats['total_textures']}")
print(f"Replaceable: {stats['replaceable_textures']}")
print(f"Space delta: {stats['potential_space_delta']} bytes")

# Perform replacement
result = lod.replace_lods(
    base_names=None,  # None = all groups
    backup_dir=Path("backups/lod")
)
print(f"Replaced: {result['replaced']}")
print(f"Failed: {result['failed']}")
print(f"Backed up: {result['backed_up']}")

# Replace specific groups only
result = lod.replace_lods(
    base_names=["texture", "character_main"],
    backup_dir=Path("backups/lod")
)
```

### Quality Score
LODReplacer uses a quality score to determine the best LOD:
- Resolution (70% weight): width × height
- File size (30% weight): Larger files often indicate better compression/quality

---

## BackupManager

Backup and restore system with compression and verification.

### Features
- Create restore points with state snapshots
- Automatic backups before risky operations
- Restore to previous state
- Backup metadata tracking
- ZIP compression to save space
- SHA256 checksum verification
- Cleanup old backups with retention policies
- Thread-safe operations

### Usage Example

```python
from features.backup_system import BackupManager

# Initialize
bm = BackupManager(backup_dir=Path("backups"))

# Create backup
backup_id = bm.create_backup(
    source_path=Path("textures"),
    name="Before LOD Replacement",
    description="Backup before replacing LOD textures",
    compress=True,
    tags=["lod", "important"]
)

# Create restore point with state data
point_id = bm.create_restore_point(
    source_path=Path("textures"),
    name="Pre-Organization",
    description="Before reorganizing textures",
    state_data={
        "operation": "reorganize",
        "profile": "god_of_war",
        "file_count": 150
    }
)

# List backups
backups = bm.list_backups()
for backup in backups:
    print(f"{backup['name']}: {backup['file_count']} files, {backup['total_size']} bytes")

# List backups by tag
auto_backups = bm.list_backups(tags=["auto"])

# Get backup info
info = bm.get_backup_info(backup_id)
print(f"Compression ratio: {info['compression_ratio']:.2%}")
print(f"Checksum: {info['checksum']}")

# Restore backup
success = bm.restore_backup(
    backup_id=backup_id,
    restore_path=Path("textures"),  # None = original location
    verify_checksum=True
)

# Restore to specific point
success = bm.restore_to_point(point_id)

# List restore points
points = bm.list_restore_points()

# Cleanup old backups
deleted_count = bm.cleanup_old_backups(
    keep_count=10,  # Keep at least 10 most recent
    keep_days=30    # Keep backups from last 30 days
)

# Delete specific backup
bm.delete_backup(backup_id)
```

### Backup Metadata
- `backup_id`: Unique identifier
- `name`: Backup name
- `description`: Backup description
- `created_at`: Creation timestamp (ISO format)
- `backup_path`: Path to backup file/directory
- `source_path`: Original source path
- `file_count`: Number of files backed up
- `total_size`: Total size in bytes
- `compressed`: Whether backup is compressed
- `compression_ratio`: Compression ratio (compressed_size / original_size)
- `checksum`: SHA256 checksum for verification
- `tags`: List of tags for categorization

### Auto-Backup Tags
The system automatically adds tags to certain backups:
- `auto`: Automatically created backup
- `pre-restore`: Created before restore operation
- `restore_point`: Part of a restore point

---

## Integration Example

Here's how to use multiple modules together:

```python
from features.search_filter import SearchFilter, FilterCriteria
from features.profile_manager import ProfileManager
from features.batch_operations import BatchQueue, OperationPriority
from features.lod_replacement import LODReplacer
from features.backup_system import BackupManager

# Initialize all modules
sf = SearchFilter()
pm = ProfileManager()
bq = BatchQueue()
lod = LODReplacer()
bm = BackupManager()

# Step 1: Find textures to process
criteria = FilterCriteria(
    formats=[".dds"],
    min_width=256,
    min_height=256
)
textures = sf.search(all_files, criteria)

# Step 2: Create backup before processing
backup_id = bm.create_backup(
    Path("textures"),
    name="Before Processing",
    compress=True,
    tags=["pre-processing", "important"]
)

# Step 3: Process LODs
lod.scan_directory(Path("textures"))
lod_result = lod.replace_lods()

# Step 4: Organize with profile
profile = pm.auto_detect_game(textures)
if profile:
    profile = pm.create_from_template(profile)

# Step 5: Queue batch operations
def organize_files(files, profile):
    # Your organization logic
    pass

op_id = bq.add_operation(
    "Organize Textures",
    organize_files,
    args=(textures, profile),
    priority=OperationPriority.HIGH
)

bq.start()

# Step 6: Save favorite searches
criteria = FilterCriteria(name="character", formats=[".dds"])
sf.save_preset("character_dds", criteria)
```

---

## Thread Safety

All modules are designed to be thread-safe:
- **SearchFilter**: Uses locks for favorites, recent, and problematic sets
- **ProfileManager**: Uses locks for profile dictionary access
- **BatchQueue**: Uses locks and events for queue management
- **LODReplacer**: Uses locks for LOD group dictionary
- **BackupManager**: Uses locks for backup and restore point dictionaries

---

## Error Handling

All modules include comprehensive error handling:
- Try-except blocks around critical operations
- Detailed logging at DEBUG, INFO, WARNING, and ERROR levels
- Graceful degradation when optional features fail
- Return None or False on failure, never raise uncaught exceptions

---

## Logging

All modules use Python's logging module:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Module-specific loggers
logger = logging.getLogger('features.search_filter')
logger.setLevel(logging.DEBUG)
```

---

## Author

All modules created by: **Dead On The Inside / JosephsDeadish**

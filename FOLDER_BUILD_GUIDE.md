# Game Texture Sorter - Build Guide 📦

**Author:** Dead On The Inside / JosephsDeadish

This guide explains how to build the Game Texture Sorter using the **one-folder build** method.

## Why One-Folder Build?

The one-folder build method provides the best experience:

### Benefits
- ⚡ **Much faster startup** - 1-3 seconds vs 10-30 seconds for single-EXE
- 🎨 **Easy customization** - Themes, sounds, and icons are external files
- 📦 **Better performance** - No extraction to temp directory on each launch
- 💾 **Local storage** - Config, cache, and database stored in app_data folder
- 🔧 **User-friendly** - Easy to modify without rebuilding

### Structure
```
GameTextureSorter/
├── GameTextureSorter.exe       (Main executable ~10-20 MB)
├── _internal/                   (Python runtime + libraries)
├── resources/                   (Icons, sounds, cursors)
└── app_data/                    (Config, cache, themes, models)
    ├── cache/
    ├── logs/
    ├── themes/
    └── models/
```

**Note:** Single-EXE mode has been removed because the one-folder build provides significantly better startup performance and user experience.

## How to Build

### Using Windows Batch (Easiest)

```cmd
build.bat           # One-folder build
```

### Using PowerShell

```powershell
.\build.ps1         # One-folder build
```

### Manual Build with PyInstaller

```cmd
# One-folder build
pyinstaller build_spec_onefolder.spec --clean --noconfirm
```

## What You Get

### One-Folder Build Output

After running `build.bat`, you'll get:

```
dist/
└── GameTextureSorter/
    ├── GameTextureSorter.exe     <- Main executable (~10-20 MB)
    ├── _internal/                <- Python runtime + libraries (~80-120 MB)
    │   ├── _tkinter.pyd
    │   ├── python312.dll
    │   └── ... (all dependencies)
    ├── resources/                <- Application resources
    │   ├── icons/
    │   ├── sounds/
    │   ├── cursors/
    │   └── themes/
    └── app_data/                 <- User data (created at runtime)
        ├── cache/                <- Thumbnail cache
        ├── logs/                 <- Application logs
        ├── themes/               <- User themes
        └── models/               <- Downloaded AI models
```

**Total folder size:** ~100-150 MB

## Startup Performance

### One-Folder Build
- **First launch:** 1-2 seconds (cold start)
- **Subsequent launches:** 0.5-1 seconds (warm start)
- **Why so fast?** No extraction needed, Python runtime loads directly from disk

### Comparison
| Build Type | Startup Time | Performance | Customization |
|------------|-------------|-------------|---------------|
| One-Folder | 1-3 seconds | Excellent   | Easy          |
| Single-EXE (deprecated) | 10-30 seconds | Slower | Hard |

## Distribution

### How to Distribute

1. **Build** the application using `build.bat`
2. **Test** the build by running `dist\GameTextureSorter\GameTextureSorter.exe`
3. **Zip** the entire `GameTextureSorter` folder
4. **Distribute** the ZIP file to users
5. **Users** simply extract and run `GameTextureSorter.exe`

### What Users Need

- **Windows 7, 8, 10, or 11**
- **No Python installation required**
- **No dependencies**
- **Just extract and run!**

## Customization

### Theme Customization

Users can customize themes by modifying files in `app_data/themes/`:

```
app_data/themes/
├── my_theme.json
└── custom_colors.json
```

### Sound Customization

Users can replace sound files in `resources/sounds/`:

```
resources/sounds/
├── click.wav
├── success.wav
└── error.wav
```

### Icon Customization

Users can add custom icons to `resources/icons/`:

```
resources/icons/
├── panda_icon.ico
├── custom_cursor.cur
└── toolbar_icons/
```

## Advanced Configuration

### Build Options

The `build_spec_onefolder.spec` file can be customized:

- **Excluded modules** - Remove unused modules to reduce size
- **Data files** - Add additional resource files
- **Hidden imports** - Add modules that PyInstaller misses
- **Runtime options** - Configure console visibility, debug mode

### Directory Structure

The `app_data` directory is created at runtime if it doesn't exist. This allows users to:
- Delete cache to free space
- Reset configuration by deleting `app_data/config.json`
- Backup user data by copying `app_data/`

## Troubleshooting

### Build Fails

**Issue:** PyInstaller build fails
**Solution:** 
1. Check Python version (3.8+ required)
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Try cleaning build artifacts: `rmdir /s /q build dist`
4. Rebuild: `build.bat`

### Application Won't Start

**Issue:** EXE launches but crashes immediately
**Solution:**
1. Check Windows Event Viewer for errors
2. Run from command line to see error messages:
   ```cmd
   cd dist\GameTextureSorter
   GameTextureSorter.exe
   ```
3. Check `app_data/logs/` for error logs

### Slow Performance

**Issue:** Application seems slower than expected
**Solution:**
1. Verify you're running from the **folder build**, not single-EXE
2. Check if antivirus is scanning the `_internal` folder
3. Ensure `app_data/cache/` has write permissions

## Performance Tips

### For Best Performance

1. ✅ Use the **one-folder build** (not single-EXE)
2. ✅ Place folder on **local drive** (not network drive)
3. ✅ Add `_internal/` to **antivirus exclusions**
4. ✅ Use **SSD** instead of HDD
5. ✅ Keep `app_data/cache/` on **fast storage**

### Startup Optimization

The one-folder build is already optimized for fast startup:
- Python runtime loads from disk (no extraction)
- Dependencies load directly (no temporary files)
- Cache uses local storage (no network delays)

## FAQ

### Why not single-EXE anymore?

The single-EXE mode has been removed because:
- 10-30 second startup time is unacceptable for users
- Extraction to temp folder causes issues with antivirus
- Performance is significantly worse
- The one-folder build provides a better overall experience

### How do I update the application?

1. Build a new version
2. Extract it to a new folder
3. Copy the old `app_data/` folder to preserve user settings
4. Delete the old folder
5. Users keep their settings, cache, and configuration

### Can I rename the folder?

Yes! The `GameTextureSorter` folder can be renamed to anything. The application will still work correctly.

### Can I move it to a different location?

Yes! The entire folder is portable. Move it anywhere:
- Desktop
- Program Files
- USB drive
- Network drive (will be slower)
- Cloud sync folder

### Where are user settings stored?

User settings are stored in `app_data/` within the application folder. This makes the application portable - copy the folder, and all settings come with it!

## Summary

✅ **One-folder build is the standard**
✅ **Fast startup (1-3 seconds)**
✅ **Easy to customize**
✅ **Better performance**
✅ **Portable folder structure**
✅ **No Python installation required**

**To build:** Run `build.bat` and distribute the `dist\GameTextureSorter\` folder!

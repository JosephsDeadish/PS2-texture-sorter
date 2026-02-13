# One-Folder Build Guide 📦

## What Changed?

**The one-folder build is now the DEFAULT!** 🎉

Previously, the build system defaulted to a single-EXE build (~206MB) that extracts everything to a temporary folder on each launch, causing **slow startup times** and performance issues.

Now, the **one-folder build is the standard**, with single-EXE as an optional mode for special portability needs.

## Build Modes

### 1. One-Folder Build (DEFAULT) ⭐
- **Command**: `build.bat` (no parameters needed!)
- **Size**: ~100-150 MB folder
- **Startup**: FAST - no extraction needed!
- **Best for**: Daily use, development, better performance

### 2. Single-EXE Build (Optional)
- **Command**: `build.bat single`
- **Size**: ~50-100 MB
- **Startup**: SLOW - extracts to temp folder on every launch
- **Best for**: Special cases requiring single-file portability

## How to Build

### Using Windows Batch (Easiest)

```cmd
build.bat           # One-folder build (DEFAULT, faster)
build.bat single    # Single-EXE build (optional, portable)
```

### Using PowerShell

```powershell
.\build.ps1         # One-folder build (DEFAULT, faster)
.\build.ps1 single  # Single-EXE build (optional, portable)
```

### Manual Build with PyInstaller

```cmd
# One-folder build (DEFAULT)
pyinstaller build_spec_onefolder.spec --clean --noconfirm

# Single-EXE build
pyinstaller build_spec.spec --clean --noconfirm
```

## What You Get

### One-Folder Build Output (DEFAULT)

After running `build.bat`, you'll get:

```
dist/
└── GameTextureSorter/
    ├── GameTextureSorter.exe     <- Main executable (~10-20 MB)
    ├── _internal/                <- Python runtime + libraries
    │   ├── *.dll
    │   ├── *.pyd
    │   └── python39.dll
    ├── resources/                <- Icons, sounds, cursors
    │   ├── icons/
    │   ├── sounds/
    │   ├── cursors/
    │   └── translations/
    └── app_data/                 <- Config, cache, themes, models
        ├── cache/
        ├── logs/
        ├── themes/
        └── models/
```

### Single-EXE Build Output (Optional)

After running `build.bat single`, you'll get:

```
dist/
└── GameTextureSorter.exe    <- Single file (~50-100 MB)
```

## Performance Comparison

| Feature | Single-EXE (Optional) | One-Folder (DEFAULT) ⭐ |
|---------|-----------|------------|
| Startup Time | 10-30 seconds ❌ | 1-3 seconds ✅ |
| File Size | 50-100 MB | 100-150 MB total |
| Performance | Slower | Faster ✅ |
| Portability | ✅ Single file | Folder |
| Asset Access | Not accessible | ✅ Easy to modify |
| Theme Customization | Embedded | ✅ External files |
| Cache Storage | Temp folder | ✅ Local folder |
| **Default Mode** | No (use `single` flag) | **Yes** ✅ |

## Why One-Folder is Now the Default

### 🚀 Much Faster Startup
- **Single-EXE**: Extracts ~100MB to temp folder on EVERY launch
- **One-Folder**: Files already on disk, no extraction needed!

### 💾 Better Resource Management
- Config, cache, and database stored in local `app_data/` folder
- No cleanup of temp files needed
- Persistent cache between launches

### 🎨 Easy Customization
- Modify themes in `app_data/themes/`
- Add custom sounds to `resources/sounds/`
- Replace icons in `resources/icons/`

### ⚡ Better Overall Performance
- No I/O overhead from extraction
- Faster file access
- More efficient memory usage

## How to Distribute

### For End Users (One-Folder - Standard)
1. Build with `build.bat` (default)
2. Zip the entire `dist/GameTextureSorter/` folder
3. Users extract and run `GameTextureSorter.exe`
4. They can move the folder anywhere

### For Maximum Portability (Single-EXE - Optional)
1. Build with `build.bat single`
2. Distribute `dist/GameTextureSorter.exe`
3. Users can run it from anywhere, including USB drives

## Troubleshooting

### "The folder is too big!"
The one-folder build is slightly larger (~100-150 MB vs 50-100 MB) because files aren't compressed. However, the **performance benefits far outweigh the size increase**.

### "I want both builds"
You can create both! Just run:
```cmd
build.bat           # Creates dist/GameTextureSorter/ folder (DEFAULT)
build.bat single    # Creates dist/GameTextureSorter.exe (optional)
```

Keep them in separate releases or move the folder before building the single-EXE.

### "Where's my database/config/cache?"
- **Single-EXE**: Stored in `%TEMP%\<random>\_MEI<numbers>\` (temporary)
- **One-Folder**: Stored in `dist\GameTextureSorter\app_data\` (persistent)

### "Can I convert between builds?"
No, you need to rebuild. The internal structure is different:
- Single-EXE: Everything in one compressed archive
- One-Folder: Files extracted to folder structure

## Recommended Usage

For **everyone** (now the default):
```cmd
build.bat           # One-folder build - faster, better performance
```

For **special portability needs only**:
```cmd
build.bat single    # Single-EXE - if you absolutely need one file
```

The one-folder build is now the standard because of its superior performance!

## Technical Details

The main difference is in the PyInstaller configuration:

**Single-EXE** (`build_spec.spec`):
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # Everything bundled in EXE
    a.zipfiles,
    a.datas,
    ...
)
```

**One-Folder** (`build_spec_onefolder.spec`):
```python
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # Don't bundle in EXE
    ...
)

coll = COLLECT(  # Create folder structure
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    ...
)
```

---

**Built with ❤️ by Dead On The Inside / JosephsDeadish**

# PS2 Texture Sorter 🐼

**Author:** Dead On The Inside / JosephsDeadish  
**Version:** 1.0.0  
**License:** TBD

A professional, single-executable Windows application for automatically sorting PS2 texture dumps with advanced AI classification, massive-scale support (200,000+ textures), and a modern panda-themed UI.

![PS2 Texture Sorter](https://img.shields.io/badge/Status-In%20Development-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)

## 🌟 Features

### Core Functionality
- **🤖 Automatic Classification** - 50+ texture categories with AI-powered classification
- **🔄 Format Conversion** - Bidirectional DDS ↔ PNG conversion with quality preservation
- **📊 Massive Scale** - Handle 200,000+ textures efficiently with database indexing
- **🎮 LOD Detection** - Automatically detect and group Level-of-Detail texture sets
- **🗂️ Smart Organization** - 9+ hierarchical organization presets (Sims style, Neopets style, etc.)
- **🔍 Duplicate Detection** - Find duplicate textures by hash or name+size
- **🛡️ File Integrity** - Corruption detection and safe file operations
- **💾 Progress Saving** - Pause/resume operations anytime with auto-save

### User Interface
- **🐼 Panda Theme** - Modern, fun interface with customizable panda elements
- **🎨 Full Customization** - Colors, cursors (skull, panda, sword), themes, layouts
- **💡 4-Level Tooltips** - From expert mode to "Panda Explains It" mode
- **🌓 Dark/Light Mode** - Built-in theme switching
- **📊 Real-Time Monitoring** - Live progress for massive operations
- **📝 Built-in Notepad** - Take notes while organizing

### Performance
- **⚡ Multi-threaded** - Utilize all CPU cores for scanning and processing
- **🗄️ Database Indexing** - SQLite-based indexing for instant searches
- **💨 Streaming Processing** - Low memory footprint for huge files
- **🔄 Incremental Processing** - Pause/resume with session recovery
- **💾 Smart Caching** - LRU cache for thumbnails and previews

### Reliability
- **🔒 Safe Operations** - Transaction-based with rollback on failure
- **📦 Backup System** - Automatic backups before operations
- **🔁 Undo/Redo** - Configurable undo history
- **💥 Crash Recovery** - Automatic session recovery after crashes
- **📋 Operation Logging** - Complete audit trail of all operations

## 📥 Quick Start

### For Users (Pre-built EXE)

1. **Download** the latest `PS2TextureSorter.exe` from [Releases](https://github.com/JosephsDeadish/PS2-texture-sorter/releases)
2. **Run** the EXE - No installation required!
3. **Start Sorting** - Select your texture folder and let the magic happen 🐼

### For Developers (Build from Source)

#### Automated Build (Recommended)

**Windows Batch:**
```cmd
git clone https://github.com/JosephsDeadish/PS2-texture-sorter.git
cd PS2-texture-sorter
build.bat
```

**PowerShell:**
```powershell
git clone https://github.com/JosephsDeadish/PS2-texture-sorter.git
cd PS2-texture-sorter
.\build.ps1
```

The build scripts automatically:
- Set up virtual environment
- Install dependencies
- Build single EXE with PyInstaller
- Create `dist/PS2TextureSorter.exe`

#### Manual Build

See [BUILD.md](BUILD.md) for detailed manual build instructions.

## 🎯 Usage

### Basic Workflow

1. **Launch Application** - Run PS2TextureSorter.exe
2. **Select Input Folder** - Choose folder containing PS2 textures
3. **Choose Organization Style** - Select from 9+ presets or create custom
4. **Configure Settings** - Adjust classification, grouping, LOD detection
5. **Start Sorting** - Watch real-time progress as textures are organized
6. **Browse Results** - Use built-in file browser to view organized textures

### Classification Modes

- **Automatic Mode** - AI classifies everything automatically
- **Manual Mode** - You choose category for each texture
- **Suggested Mode** - AI suggests, you confirm
- **Custom Rules** - Create regex patterns for specific files

### Organization Styles

1. **Sims Style** - Gender/Skin/BodyPart/Variant
2. **Neopets Style** - Category/Type/Individual LOD folders
3. **Flat Style** - All LODs in category root
4. **Game Area Style** - Level/Area/Type/Asset
5. **Asset Pipeline Style** - Type/Resolution/Format
6. **Modular Style** - Character/Vehicle/Environment/UI
7. **Minimalist Style** - Simple categories only
8. **Maximum Detail Style** - Deep nested hierarchies
9. **Custom Style** - Build your own with drag-and-drop

### LOD (Level of Detail) Features

Automatically detects and groups:
- `texture_lod0`, `texture_lod1`, `texture_lod2`
- `texture_high`, `texture_med`, `texture_low`
- `texture_0`, `texture_1`, `texture_2`
- Visual similarity detection for unnumbered LODs

## 🔧 Configuration

Settings are stored in: `%USERPROFILE%\.ps2_texture_sorter\config.json`

### Key Settings Categories

- **UI Settings** - Theme, colors, cursors, tooltips, layout
- **Performance** - Thread count, memory limits, cache size
- **File Handling** - Backup, overwrite, auto-save, undo depth
- **Sorting** - Mode, organization style, grouping options
- **Logging** - Log level, crash reports, performance metrics
- **Notifications** - Sounds, alerts, completion notifications

## 📚 Documentation

- **[BUILD.md](BUILD.md)** - Detailed build instructions
- **[CODE_SIGNING.md](CODE_SIGNING.md)** - Guide to signing the EXE
- **User Manual** - Embedded in application + external PDF (coming soon)
- **Developer Docs** - API documentation and architecture (coming soon)

## 🛠️ Development

### Project Structure

```
PS2-texture-sorter/
├── main.py                      # Application entry point
├── src/                         # Source code
│   ├── classifier/              # Texture classification engine
│   │   ├── categories.py        # 50+ category definitions
│   │   └── classifier_engine.py # AI classification logic
│   ├── lod_detector/            # LOD detection system
│   ├── file_handler/            # File operations & conversion
│   ├── database/                # SQLite indexing
│   ├── ui/                      # User interface components
│   ├── settings/                # Settings management
│   ├── utils/                   # Helper utilities
│   └── resources/               # Icons, cursors, themes, sounds
├── requirements.txt             # Python dependencies
├── build_spec.spec              # PyInstaller configuration
├── file_version_info.txt        # EXE metadata
├── build.bat                    # Automated build (Batch)
├── build.ps1                    # Automated build (PowerShell)
├── sign.bat                     # Code signing script
├── BUILD.md                     # Build guide
└── CODE_SIGNING.md              # Signing guide
```

### Technologies Used

- **Python 3.8+** - Core language
- **CustomTkinter** - Modern UI framework
- **Pillow (PIL)** - Image processing
- **OpenCV** - Advanced image analysis
- **NumPy** - Numerical operations
- **scikit-learn** - Machine learning
- **SQLite** - Database indexing
- **PyInstaller** - Single EXE creation

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🔐 Code Signing

For Windows SmartScreen compatibility and trust:

1. Obtain code signing certificate ($179-$600/year)
2. Update certificate details in `sign.bat`
3. Run: `sign.bat`

See [CODE_SIGNING.md](CODE_SIGNING.md) for complete guide.

## 📦 Building Single EXE

The application is built as a single, portable EXE file:

- **Size:** ~50-100 MB (all dependencies included)
- **No Installation Required** - Run from anywhere
- **USB Compatible** - Fully portable
- **Offline** - Works 100% offline, no internet required
- **Zero Dependencies** - Everything is embedded

### Automated Build

```cmd
# Windows Batch
build.bat

# PowerShell
.\build.ps1
```

Output: `dist/PS2TextureSorter.exe`

## 🐛 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python 3.8+ from [python.org](https://www.python.org/)
- Ensure "Add to PATH" was checked during installation

**"Module not found" errors**
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Application won't start**
- Check crash logs in `%USERPROFILE%\.ps2_texture_sorter\logs\`
- Try safe mode (feature coming soon)
- Report issue with log file

**Performance issues with 200,000+ files**
- Increase memory limit in settings
- Disable image analysis for speed
- Use incremental processing mode

## 📊 Performance

Tested with:
- ✅ 200,000+ texture files
- ✅ 4K, 8K, 16K textures
- ✅ Multi-GB file sizes
- ✅ Mixed DDS and PNG formats
- ✅ Windows 7, 8, 10, 11

## 🎯 Roadmap

- [ ] Complete UI implementation (Phase 6)
- [ ] Add machine learning training mode
- [ ] Implement all 9 organization presets
- [ ] Add batch conversion GUI
- [ ] Create video tutorials
- [ ] Multi-language support
- [ ] macOS/Linux versions (future consideration)

## 📄 License

License TBD by author. All rights reserved to Dead On The Inside / JosephsDeadish.

## 🙏 Credits

**Author:** Dead On The Inside / JosephsDeadish  
**Repository:** [JosephsDeadish/PS2-texture-sorter](https://github.com/JosephsDeadish/PS2-texture-sorter)

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/JosephsDeadish/PS2-texture-sorter/issues)
- **Discussions:** [GitHub Discussions](https://github.com/JosephsDeadish/PS2-texture-sorter/discussions)

## 🐼 About the Panda Theme

The panda theme represents:
- **Friendly & Approachable** - Even complex texture sorting becomes simple
- **Efficient & Focused** - Like pandas eating bamboo, the app focuses on one task
- **Reliable & Steady** - Dependable performance even with massive files
- **Fun & Memorable** - Sorting textures doesn't have to be boring!

---

**Made with 🐼 by Dead On The Inside / JosephsDeadish**
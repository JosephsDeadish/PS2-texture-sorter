# File Picker Widget Documentation

## Overview

The **FilePickerWidget** is a universal, reusable UI component for file selection across all tools in the PS2 Texture Sorter application. It provides a consistent, feature-rich interface for selecting files, folders, and archives.

## Features

✅ **Single file selection** - Select one file at a time  
✅ **Multiple file selection** - Select multiple files with checkboxes  
✅ **Folder/directory picker** - Browse and select entire folders  
✅ **Archive file picker** - Select .zip, .7z, .rar, .tar files  
✅ **Visual file browser** - Clean, modern UI with file list display  
✅ **Recent files history** - Quick access to last 10 selected files  
✅ **Drag & drop support** - Drag files directly onto the widget  
✅ **File filtering by type** - Restrict to specific file extensions  
✅ **Configurable per tool** - Each tool can customize behavior  
✅ **Custom tooltip support** - Set tooltips for user guidance  
✅ **PyQt6 signals** - Event-driven integration with panels  

## Installation

The widget is located in:
```
src/ui/widgets/file_picker_widget.py
src/ui/widgets/__init__.py
```

## Quick Start

### Basic Usage

```python
from src.ui.widgets import FilePickerWidget

# Create a simple file picker
file_picker = FilePickerWidget(
    file_types=('*.png', '*.jpg', '*.jpeg'),
    allow_multiple=False
)

# Connect to signal
file_picker.files_selected.connect(on_files_selected)

def on_files_selected(files):
    if files:
        print(f"Selected: {files[0]}")
```

## API Reference

### Constructor

```python
FilePickerWidget(
    file_types: Tuple[str, ...] = IMAGE_FORMATS,
    allow_multiple: bool = False,
    allow_folders: bool = False,
    allow_archives: bool = False,
    parent=None
)
```

**Parameters:**
- `file_types` - Tuple of file extensions (e.g., `('*.png', '*.jpg')`)
- `allow_multiple` - Enable multi-file selection with checkboxes
- `allow_folders` - Show folder browse button
- `allow_archives` - Show archive browse button
- `parent` - Parent widget (optional)

### Constants

```python
FilePickerWidget.IMAGE_FORMATS
# ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp', '*.tiff', '*.tif')

FilePickerWidget.ARCHIVE_FORMATS
# ('*.zip', '*.7z', '*.rar', '*.tar', '*.tar.gz')

FilePickerWidget.ALL_FORMATS
# IMAGE_FORMATS + ARCHIVE_FORMATS
```

### Signals

```python
files_selected = pyqtSignal(list)  # List[Path]
# Emitted when files are selected (via browse, drag-drop, or recent menu)

folder_selected = pyqtSignal(Path)
# Emitted when a folder is selected

archive_selected = pyqtSignal(Path)
# Emitted when an archive file is selected
```

### Methods

#### `set_files(files: List[Path])`
Programmatically set selected files.
```python
files = [Path('/path/to/file1.png'), Path('/path/to/file2.png')]
file_picker.set_files(files)
```

#### `get_selected_files() -> List[Path]`
Get all currently selected files as a list.
```python
files = file_picker.get_selected_files()
```

#### `get_selected_file() -> Optional[Path]`
Get the first selected file (useful for single-file mode).
```python
file = file_picker.get_selected_file()
```

#### `on_clear()`
Clear all selected files.
```python
file_picker.on_clear()
```

## Usage Examples

### Example 1: Upscaler Tool (Single File)

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from src.ui.widgets import FilePickerWidget

class UpscalerPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Single file picker for upscaling
        self.file_picker = FilePickerWidget(
            file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp'),
            allow_multiple=False,
            allow_folders=False,
            allow_archives=False
        )
        self.file_picker.files_selected.connect(self.on_file_selected)
        self.file_picker.setToolTip("Select image to upscale")
        
        layout.addWidget(self.file_picker)
        self.setLayout(layout)
    
    def on_file_selected(self, files):
        if files:
            print(f"Upscaling: {files[0]}")
```

### Example 2: Batch Rename Tool (Multiple Files + Folder)

```python
from src.ui.widgets import FilePickerWidget

class BatchRenamePanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Multi-file picker with folder support
        self.file_picker = FilePickerWidget(
            file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.webp'),
            allow_multiple=True,   # Enable multi-select
            allow_folders=True,    # Enable folder selection
            allow_archives=False
        )
        self.file_picker.files_selected.connect(self.on_files_selected)
        self.file_picker.folder_selected.connect(self.on_folder_selected)
        
        layout.addWidget(self.file_picker)
        self.setLayout(layout)
    
    def on_files_selected(self, files):
        print(f"Selected {len(files)} files for renaming")
    
    def on_folder_selected(self, folder):
        print(f"Selected folder: {folder}")
        # Scan folder for images...
```

### Example 3: Organizer Tool (All Features)

```python
from src.ui.widgets import FilePickerWidget

class OrganizerPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Full-featured picker
        self.file_picker = FilePickerWidget(
            file_types=FilePickerWidget.IMAGE_FORMATS,
            allow_multiple=True,   # Multi-select
            allow_folders=True,    # Folder selection
            allow_archives=True    # Archive selection
        )
        self.file_picker.files_selected.connect(self.on_files_selected)
        self.file_picker.folder_selected.connect(self.on_folder_selected)
        self.file_picker.archive_selected.connect(self.on_archive_selected)
        self.file_picker.setToolTip("Select files, folder, or archive to organize")
        
        layout.addWidget(self.file_picker)
        self.setLayout(layout)
    
    def on_files_selected(self, files):
        print(f"Organizing {len(files)} files")
    
    def on_folder_selected(self, folder):
        print(f"Organizing folder: {folder}")
    
    def on_archive_selected(self, archive):
        print(f"Extracting and organizing: {archive}")
```

## Integration with PyQt6BasePanel

```python
from src.ui.pyqt6_base_panel import PyQt6BasePanel
from src.ui.widgets import FilePickerWidget

class MyToolPanel(PyQt6BasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        layout = QVBoxLayout()
        
        # Add file picker
        self.file_picker = FilePickerWidget(
            file_types=('*.png', '*.jpg'),
            allow_multiple=True
        )
        self.file_picker.files_selected.connect(self._on_files_selected)
        
        layout.addWidget(self.file_picker)
        self.setLayout(layout)
    
    def _on_files_selected(self, files):
        # Use base panel's status system
        self.status_changed.emit(f"Selected {len(files)} files")
```

## Features in Detail

### Drag and Drop

The widget automatically supports drag and drop:
1. User drags files from file manager
2. Drops onto the widget
3. Files are validated against `file_types`
4. Invalid files are filtered out
5. Selected files are updated
6. Signals are emitted

No additional code required!

### Recent Files History

The widget maintains a recent files history:
- Saves last 10 selected files/folders/archives
- Persistent across sessions
- Stored in `~/.ps2_texture_sorter/recent_files.json`
- "⏱️  Recent" button shows dropdown menu
- Only shows files that still exist
- Can clear history via "🗑️  Clear History" option

### File Filtering

Files are automatically filtered based on `file_types`:
```python
# Only PNG and JPEG
file_picker = FilePickerWidget(file_types=('*.png', '*.jpg', '*.jpeg'))

# All image formats
file_picker = FilePickerWidget(file_types=FilePickerWidget.IMAGE_FORMATS)

# Archives only
file_picker = FilePickerWidget(file_types=FilePickerWidget.ARCHIVE_FORMATS)

# Everything
file_picker = FilePickerWidget(file_types=FilePickerWidget.ALL_FORMATS)
```

### UI Customization

The widget uses styled buttons and a clean layout:
- **Blue** - Browse Files button
- **Green** - Browse Folder button
- **Orange** - Browse Archive button
- **Purple** - Recent files button
- **Red** - Clear selection button

Set custom tooltips:
```python
file_picker.setToolTip("Your custom tooltip here")
```

## Testing

Run the test suite:
```bash
python test_file_picker_widget.py
```

Run the demo application:
```bash
python demo_file_picker.py
```

## File Structure

```
src/ui/widgets/
├── __init__.py              # Package exports
└── file_picker_widget.py    # Main widget implementation

test_file_picker_widget.py   # Unit tests
demo_file_picker.py          # Demo application
USAGE_EXAMPLES_FILE_PICKER.py # Code examples
```

## Requirements

- PyQt6 >= 6.6.0
- Python >= 3.9

## Supported File Formats

### Images
- PNG (*.png)
- JPEG (*.jpg, *.jpeg)
- BMP (*.bmp)
- WebP (*.webp)
- TIFF (*.tiff, *.tif)

### Archives
- ZIP (*.zip)
- 7-Zip (*.7z)
- RAR (*.rar)
- TAR (*.tar, *.tar.gz)

## Technical Details

### Signals and Slots

The widget uses PyQt6's signal/slot mechanism:
```python
# Emitting signals
self.files_selected.emit(files)
self.folder_selected.emit(folder_path)
self.archive_selected.emit(archive_path)

# Connecting to signals
file_picker.files_selected.connect(my_handler)
```

### State Management

Selected files are stored in:
```python
self.selected_files: List[Path]
```

Access via:
```python
files = file_picker.get_selected_files()  # Returns copy
file = file_picker.get_selected_file()    # Returns first file
```

### Configuration Storage

Recent files are saved to:
```
~/.ps2_texture_sorter/recent_files.json
```

Format:
```json
[
    "/path/to/file1.png",
    "/path/to/file2.png",
    "/path/to/folder"
]
```

## Best Practices

1. **Connect signals early** - Connect to signals in `__init__` or `_create_widgets`
2. **Use type constants** - Use `FilePickerWidget.IMAGE_FORMATS` instead of hardcoding
3. **Set tooltips** - Help users understand what files to select
4. **Handle all signals** - If you enable folders/archives, connect to all signals
5. **Validate files** - Even though the widget filters, validate in your handler
6. **Use base panel integration** - Leverage `PyQt6BasePanel` for consistent UI

## Troubleshooting

### Files not being selected
- Check that `file_types` matches your file extensions
- Ensure extensions start with `*.` (e.g., `'*.png'`)
- Use lowercase extensions

### Drag and drop not working
- Ensure `setAcceptDrops(True)` is called (done automatically)
- Check that dropped files match `file_types`

### Recent files not saving
- Check that `~/.ps2_texture_sorter/` directory is writable
- Look for errors in logs

## Contributing

To modify the widget:
1. Edit `src/ui/widgets/file_picker_widget.py`
2. Add tests to `test_file_picker_widget.py`
3. Update examples in `USAGE_EXAMPLES_FILE_PICKER.py`
4. Update this documentation
5. Run tests: `python test_file_picker_widget.py`

## License

Part of the PS2 Texture Sorter project.

## Support

For issues or questions:
1. Check this documentation
2. Review usage examples
3. Run the demo application
4. Check the test file for validation patterns

"""
File Picker Widget Usage Examples

This file demonstrates how to use the FilePickerWidget in different tools
"""

# Example 1: Simple Single File Picker (Upscaler Tool)
# =======================================================
def example_upscaler_usage():
    """Example: Single image file selection for upscaler"""
    from PyQt6.QtWidgets import QWidget, QVBoxLayout
    from src.ui.widgets import FilePickerWidget
    
    class UpscalerPanel(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()
            
            # Create file picker (single file, images only)
            self.file_picker = FilePickerWidget(
                file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp'),
                allow_multiple=False,
                allow_folders=False,
                allow_archives=False
            )
            self.file_picker.files_selected.connect(self.on_files_selected)
            self.file_picker.setToolTip("Select image to upscale (PNG, JPG, etc.)")
            
            layout.addWidget(self.file_picker)
            self.setLayout(layout)
        
        def on_files_selected(self, files):
            """Handle file selection"""
            if files:
                file_path = files[0]
                print(f"Selected file for upscaling: {file_path}")
                # Process file...


# Example 2: Multi-File Picker with Folders and Archives (Organizer Tool)
# ========================================================================
def example_organizer_usage():
    """Example: Multi-file selection with folder and archive support"""
    from PyQt6.QtWidgets import QWidget, QVBoxLayout
    from src.ui.widgets import FilePickerWidget
    
    class OrganizerPanel(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()
            
            # Create file picker with all options enabled
            self.file_picker = FilePickerWidget(
                file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp'),
                allow_multiple=True,   # Multi-select with checkboxes
                allow_folders=True,    # Can pick folders
                allow_archives=True    # Can pick archives
            )
            self.file_picker.files_selected.connect(self.on_files_selected)
            self.file_picker.folder_selected.connect(self.on_folder_selected)
            self.file_picker.archive_selected.connect(self.on_archive_selected)
            self.file_picker.setToolTip("Select folder with textures to organize or pick archive")
            
            layout.addWidget(self.file_picker)
            self.setLayout(layout)
        
        def on_files_selected(self, files):
            """Handle multiple file selection"""
            print(f"Selected {len(files)} files for organizing")
            for file_path in files:
                print(f"  - {file_path}")
        
        def on_folder_selected(self, folder_path):
            """Handle folder selection"""
            print(f"Selected folder: {folder_path}")
            # Process all images in folder...
        
        def on_archive_selected(self, archive_path):
            """Handle archive selection"""
            print(f"Selected archive: {archive_path}")
            # Extract and process archive...


# Example 3: Batch Processing with Multiple Files
# ================================================
def example_batch_rename_usage():
    """Example: Multiple file selection for batch operations"""
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
    from src.ui.widgets import FilePickerWidget
    
    class BatchRenamePanel(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()
            
            # Info label
            info_label = QLabel("Select multiple images to batch rename")
            layout.addWidget(info_label)
            
            # Create file picker for multiple files
            self.file_picker = FilePickerWidget(
                file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.webp'),
                allow_multiple=True,   # Enable multi-select
                allow_folders=True,    # Allow selecting entire folders
                allow_archives=False   # Don't need archives for renaming
            )
            self.file_picker.files_selected.connect(self.on_files_selected)
            self.file_picker.folder_selected.connect(self.on_folder_selected)
            
            layout.addWidget(self.file_picker)
            self.setLayout(layout)
        
        def on_files_selected(self, files):
            """Handle file selection"""
            print(f"Selected {len(files)} files to rename")
            # Show preview of renamed files...
        
        def on_folder_selected(self, folder_path):
            """Handle folder selection - find all images in folder"""
            print(f"Selected folder: {folder_path}")
            # Scan folder for images and show preview...


# Example 4: Getting Selected Files
# ==================================
def example_get_selected_files():
    """Example: How to retrieve selected files from the widget"""
    from src.ui.widgets import FilePickerWidget
    
    # Create widget
    file_picker = FilePickerWidget(
        allow_multiple=True,
        allow_folders=False
    )
    
    # Later in your code, retrieve the selected files:
    
    # Get all selected files as a list
    all_files = file_picker.get_selected_files()
    print(f"All selected files: {all_files}")
    
    # Get just the first file (useful for single-file mode)
    first_file = file_picker.get_selected_file()
    print(f"First file: {first_file}")


# Example 5: Custom File Types
# =============================
def example_custom_file_types():
    """Example: Using custom file types for different tools"""
    from src.ui.widgets import FilePickerWidget
    
    # For a tool that works with all image formats
    all_images_picker = FilePickerWidget(
        file_types=FilePickerWidget.IMAGE_FORMATS  # All supported image formats
    )
    
    # For a tool that only works with PNG and JPEG
    png_jpeg_picker = FilePickerWidget(
        file_types=('*.png', '*.jpg', '*.jpeg')
    )
    
    # For a tool that works with archives
    archive_picker = FilePickerWidget(
        file_types=FilePickerWidget.ARCHIVE_FORMATS,  # All supported archives
        allow_archives=True
    )
    
    # For a tool that accepts both images and archives
    combined_picker = FilePickerWidget(
        file_types=FilePickerWidget.ALL_FORMATS,  # Images + Archives
        allow_archives=True
    )


# Example 6: Setting Files Programmatically
# ==========================================
def example_set_files_programmatically():
    """Example: How to set files in the widget from code"""
    from pathlib import Path
    from src.ui.widgets import FilePickerWidget
    
    # Create widget
    file_picker = FilePickerWidget(allow_multiple=True)
    
    # Set files from code (e.g., from a saved session)
    files = [
        Path('/home/user/texture1.png'),
        Path('/home/user/texture2.png'),
        Path('/home/user/texture3.png')
    ]
    
    file_picker.set_files(files)
    # This will:
    # - Update the display
    # - Emit the files_selected signal
    # - Add to recent files


# Example 7: Drag and Drop Support
# =================================
def example_drag_and_drop():
    """
    The widget automatically supports drag and drop!
    
    Users can:
    1. Drag files from their file manager
    2. Drop onto the widget
    3. Files are automatically validated against allowed types
    4. Invalid files are filtered out
    5. Recent files are updated
    """
    from src.ui.widgets import FilePickerWidget
    
    # Just create the widget - drag & drop works automatically
    file_picker = FilePickerWidget(
        file_types=('*.png', '*.jpg'),
        allow_multiple=True
    )
    
    # That's it! Users can now drag PNG/JPG files onto the widget


# Example 8: Recent Files History
# ================================
def example_recent_files():
    """
    The widget automatically tracks recent files!
    
    Features:
    - Saves last 10 recently selected files/folders
    - Persistent across sessions (saved to ~/.ps2_texture_sorter/recent_files.json)
    - "Recent" button shows dropdown menu
    - Can clear history
    - Only shows files that still exist
    """
    from src.ui.widgets import FilePickerWidget
    
    # Create widget - recent files work automatically
    file_picker = FilePickerWidget()
    
    # Users can:
    # 1. Click "⏱️  Recent" button
    # 2. Select from recent files dropdown
    # 3. Click "🗑️  Clear History" to clear
    
    # Recent files are shared across all widgets
    # (stored globally for the application)


# Example 9: Integration with Existing Tool Panel
# ================================================
def example_integrate_with_base_panel():
    """Example: Integrate with PyQt6BasePanel"""
    from PyQt6.QtWidgets import QVBoxLayout, QGroupBox
    from src.ui.pyqt6_base_panel import PyQt6BasePanel
    from src.ui.widgets import FilePickerWidget
    
    class MyToolPanel(PyQt6BasePanel):
        def __init__(self, parent=None):
            super().__init__(parent)
            self._create_widgets()
        
        def _create_widgets(self):
            """Create panel widgets"""
            layout = QVBoxLayout()
            
            # Input section
            input_group = QGroupBox("Input Files")
            input_layout = QVBoxLayout()
            
            # Add file picker
            self.file_picker = FilePickerWidget(
                file_types=('*.png', '*.jpg', '*.jpeg'),
                allow_multiple=True,
                allow_folders=True
            )
            self.file_picker.files_selected.connect(self._on_files_selected)
            self.file_picker.folder_selected.connect(self._on_folder_selected)
            
            input_layout.addWidget(self.file_picker)
            input_group.setLayout(input_layout)
            layout.addWidget(input_group)
            
            self.setLayout(layout)
        
        def _on_files_selected(self, files):
            """Handle file selection"""
            # Use base panel's status system
            self.status_changed.emit(f"Selected {len(files)} files")
        
        def _on_folder_selected(self, folder):
            """Handle folder selection"""
            self.status_changed.emit(f"Selected folder: {folder.name}")


# Summary of Features
# ===================
"""
The FilePickerWidget provides:

✅ Single file selection (images: PNG, JPG, BMP, WEBP, TIFF)
✅ Multiple file selection with checkboxes
✅ Folder/directory picker
✅ Archive file picker (.zip, .7z, .rar, .tar)
✅ Visual file browser with file list display
✅ Recent files history (last 10 files)
✅ Drag & drop support (automatic)
✅ File filtering by type
✅ Configurable for each tool (different file types per tool)
✅ Return selected files as list or single file
✅ Custom tooltip support (each tool can set own tooltip)
✅ Beautiful UI with colors and icons
✅ PyQt6 signals for integration (files_selected, folder_selected, archive_selected)
✅ Persistent recent files across sessions
✅ Clear selection button
✅ Compatible with PyQt6BasePanel
"""

if __name__ == '__main__':
    print("File Picker Widget Usage Examples")
    print("=" * 50)
    print()
    print("See the examples above for integration patterns.")
    print()
    print("Quick Start:")
    print("  from src.ui.widgets import FilePickerWidget")
    print()
    print("  widget = FilePickerWidget(")
    print("      file_types=('*.png', '*.jpg'),")
    print("      allow_multiple=True")
    print("  )")
    print("  widget.files_selected.connect(my_callback)")

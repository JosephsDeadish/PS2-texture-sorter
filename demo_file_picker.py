#!/usr/bin/env python3
"""
File Picker Widget Demo Application

This script demonstrates the FilePickerWidget in action.
Run this to see the widget's UI and test its features.

Requirements:
    - PyQt6 must be installed
    - Run from the repository root directory

Usage:
    python demo_file_picker.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout,
        QTabWidget, QLabel, QGroupBox, QTextEdit
    )
    from PyQt6.QtCore import Qt
    from src.ui.widgets import FilePickerWidget
except ImportError as e:
    print(f"Error: Could not import required modules: {e}")
    print("\nPlease install PyQt6:")
    print("  pip install PyQt6")
    sys.exit(1)


class FilePickerDemo(QMainWindow):
    """Demo application showing different FilePickerWidget configurations"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Picker Widget Demo")
        self.setGeometry(100, 100, 900, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("File Picker Widget Demo")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Create tab widget to show different configurations
        tabs = QTabWidget()
        
        # Tab 1: Single File Picker
        tabs.addTab(self._create_single_file_tab(), "Single File")
        
        # Tab 2: Multiple Files Picker
        tabs.addTab(self._create_multiple_files_tab(), "Multiple Files")
        
        # Tab 3: Folder & Archive Picker
        tabs.addTab(self._create_folder_archive_tab(), "Folder & Archive")
        
        # Tab 4: All Features
        tabs.addTab(self._create_all_features_tab(), "All Features")
        
        layout.addWidget(tabs)
        
        # Event log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(150)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #00ff00;
                font-family: monospace;
                font-size: 11px;
                border: 1px solid #444;
                border-radius: 4px;
            }
        """)
        layout.addWidget(QLabel("Event Log:"))
        layout.addWidget(self.log_area)
        
        central_widget.setLayout(layout)
        
        self.log("Application started. Try selecting files!")
    
    def _create_single_file_tab(self):
        """Create tab showing single file selection"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Description
        desc = QLabel(
            "Single File Picker\n\n"
            "• Select one file at a time\n"
            "• Used by: Upscaler, Image Repair, etc.\n"
            "• Shows file name and path when selected"
        )
        desc.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 4px;")
        layout.addWidget(desc)
        
        # File picker
        group = QGroupBox("Single File Selection")
        group_layout = QVBoxLayout()
        
        self.single_picker = FilePickerWidget(
            file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp'),
            allow_multiple=False,
            allow_folders=False,
            allow_archives=False
        )
        self.single_picker.files_selected.connect(self._on_single_file_selected)
        self.single_picker.setToolTip("Select a single image file")
        
        group_layout.addWidget(self.single_picker)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_multiple_files_tab(self):
        """Create tab showing multiple file selection"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Description
        desc = QLabel(
            "Multiple Files Picker\n\n"
            "• Select multiple files with checkboxes\n"
            "• Used by: Batch Rename, Batch Normalizer, etc.\n"
            "• Shows list of selected files"
        )
        desc.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 4px;")
        layout.addWidget(desc)
        
        # File picker
        group = QGroupBox("Multiple File Selection")
        group_layout = QVBoxLayout()
        
        self.multi_picker = FilePickerWidget(
            file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp', '*.tiff'),
            allow_multiple=True,
            allow_folders=False,
            allow_archives=False
        )
        self.multi_picker.files_selected.connect(self._on_multi_files_selected)
        self.multi_picker.setToolTip("Select multiple image files")
        
        group_layout.addWidget(self.multi_picker)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_folder_archive_tab(self):
        """Create tab showing folder and archive selection"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Description
        desc = QLabel(
            "Folder & Archive Picker\n\n"
            "• Browse for folders or archive files\n"
            "• Used by: Organizer, Batch tools, etc.\n"
            "• Supports .zip, .7z, .rar, .tar archives"
        )
        desc.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 4px;")
        layout.addWidget(desc)
        
        # File picker
        group = QGroupBox("Folder & Archive Selection")
        group_layout = QVBoxLayout()
        
        self.folder_picker = FilePickerWidget(
            file_types=('*.png', '*.jpg', '*.jpeg'),
            allow_multiple=False,
            allow_folders=True,
            allow_archives=True
        )
        self.folder_picker.files_selected.connect(self._on_files_selected)
        self.folder_picker.folder_selected.connect(self._on_folder_selected)
        self.folder_picker.archive_selected.connect(self._on_archive_selected)
        self.folder_picker.setToolTip("Select folder or archive file")
        
        group_layout.addWidget(self.folder_picker)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_all_features_tab(self):
        """Create tab showing all features enabled"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Description
        desc = QLabel(
            "All Features Enabled\n\n"
            "• Multi-file selection with checkboxes\n"
            "• Folder browsing\n"
            "• Archive file support\n"
            "• Drag & drop files here!\n"
            "• Recent files history\n"
            "• Used by: Advanced tools like Organizer"
        )
        desc.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 4px;")
        layout.addWidget(desc)
        
        # File picker
        group = QGroupBox("All Features")
        group_layout = QVBoxLayout()
        
        self.full_picker = FilePickerWidget(
            file_types=('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp', '*.tiff'),
            allow_multiple=True,
            allow_folders=True,
            allow_archives=True
        )
        self.full_picker.files_selected.connect(self._on_full_files_selected)
        self.full_picker.folder_selected.connect(self._on_full_folder_selected)
        self.full_picker.archive_selected.connect(self._on_full_archive_selected)
        self.full_picker.setToolTip("Full-featured file picker with all options")
        
        group_layout.addWidget(self.full_picker)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    # Event handlers
    def _on_single_file_selected(self, files):
        if files:
            self.log(f"[Single] Selected file: {files[0].name}")
    
    def _on_multi_files_selected(self, files):
        self.log(f"[Multi] Selected {len(files)} files")
        for f in files:
            self.log(f"  - {f.name}")
    
    def _on_files_selected(self, files):
        if files:
            self.log(f"[Folder/Archive] Selected {len(files)} files")
    
    def _on_folder_selected(self, folder):
        self.log(f"[Folder] Selected: {folder}")
    
    def _on_archive_selected(self, archive):
        self.log(f"[Archive] Selected: {archive.name}")
    
    def _on_full_files_selected(self, files):
        self.log(f"[Full] Selected {len(files)} files")
        for f in files[:3]:  # Show first 3
            self.log(f"  - {f.name}")
        if len(files) > 3:
            self.log(f"  ... and {len(files) - 3} more")
    
    def _on_full_folder_selected(self, folder):
        self.log(f"[Full] Folder: {folder}")
    
    def _on_full_archive_selected(self, archive):
        self.log(f"[Full] Archive: {archive.name}")
    
    def log(self, message):
        """Add message to log"""
        self.log_area.append(message)


def main():
    """Run the demo application"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show demo window
    demo = FilePickerDemo()
    demo.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

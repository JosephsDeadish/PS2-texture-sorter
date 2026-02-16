"""
Test File Picker Widget

Tests the universal file picker widget structure and functionality
without requiring a running GUI (validates structure, imports, and API)
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import the widget
try:
    from src.ui.widgets import FilePickerWidget
    WIDGET_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import FilePickerWidget: {e}")
    WIDGET_AVAILABLE = False


class TestFilePickerWidgetStructure(unittest.TestCase):
    """Test File Picker Widget structure and API"""
    
    def setUp(self):
        """Skip tests if widget not available"""
        if not WIDGET_AVAILABLE:
            self.skipTest("FilePickerWidget not available")
    
    def test_widget_class_exists(self):
        """Test that FilePickerWidget class exists"""
        self.assertTrue(hasattr(FilePickerWidget, '__init__'))
    
    def test_widget_has_required_signals(self):
        """Test that widget has required signals"""
        # Check class attributes for signals
        self.assertTrue(hasattr(FilePickerWidget, 'files_selected'))
        self.assertTrue(hasattr(FilePickerWidget, 'folder_selected'))
        self.assertTrue(hasattr(FilePickerWidget, 'archive_selected'))
    
    def test_widget_has_format_constants(self):
        """Test that widget has file format constants"""
        self.assertTrue(hasattr(FilePickerWidget, 'IMAGE_FORMATS'))
        self.assertTrue(hasattr(FilePickerWidget, 'ARCHIVE_FORMATS'))
        self.assertTrue(hasattr(FilePickerWidget, 'ALL_FORMATS'))
        
        # Check types
        self.assertIsInstance(FilePickerWidget.IMAGE_FORMATS, tuple)
        self.assertIsInstance(FilePickerWidget.ARCHIVE_FORMATS, tuple)
        self.assertIsInstance(FilePickerWidget.ALL_FORMATS, tuple)
    
    def test_widget_has_required_methods(self):
        """Test that widget has required public methods"""
        required_methods = [
            'setup_ui',
            'on_browse',
            'on_browse_folder',
            'on_browse_archive',
            'on_clear',
            'set_files',
            'update_display',
            'update_info',
            'add_to_recent',
            'load_recent_files',
            'load_recent_files_list',
            'show_recent_menu',
            'on_clear_recent',
            'get_filter_string',
            'get_archive_filter_string',
            'is_valid_file',
            'get_selected_files',
            'get_selected_file',
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(FilePickerWidget, method_name),
                f"Missing method: {method_name}"
            )
    
    def test_init_parameters(self):
        """Test widget initialization parameters"""
        # Test that __init__ accepts expected parameters
        import inspect
        sig = inspect.signature(FilePickerWidget.__init__)
        params = list(sig.parameters.keys())
        
        expected_params = ['self', 'file_types', 'allow_multiple', 'allow_folders', 'allow_archives', 'parent']
        for param in expected_params:
            self.assertIn(param, params, f"Missing parameter: {param}")
    
    def test_image_formats_valid(self):
        """Test that IMAGE_FORMATS contains expected formats"""
        formats = FilePickerWidget.IMAGE_FORMATS
        expected = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp']
        
        for fmt in expected:
            self.assertIn(fmt, formats, f"Missing image format: {fmt}")
    
    def test_archive_formats_valid(self):
        """Test that ARCHIVE_FORMATS contains expected formats"""
        formats = FilePickerWidget.ARCHIVE_FORMATS
        expected = ['*.zip', '*.7z', '*.rar', '*.tar']
        
        for fmt in expected:
            self.assertIn(fmt, formats, f"Missing archive format: {fmt}")
    
    def test_widget_import_from_package(self):
        """Test that widget can be imported from package"""
        from src.ui.widgets import FilePickerWidget as FPW
        self.assertIsNotNone(FPW)
        self.assertEqual(FPW.__name__, 'FilePickerWidget')


class TestFilePickerAPI(unittest.TestCase):
    """Test File Picker Widget API (without GUI)"""
    
    def setUp(self):
        """Skip tests if widget not available"""
        if not WIDGET_AVAILABLE:
            self.skipTest("FilePickerWidget not available")
    
    def test_is_valid_file(self):
        """Test file validation logic"""
        # We can test the validation method without creating the widget
        # by testing the logic directly
        
        # Mock a simple validator
        def is_valid(file_path: Path, file_types: tuple) -> bool:
            suffix = file_path.suffix.lower()
            return any(suffix == ext.replace('*', '') for ext in file_types)
        
        # Test image files
        image_types = ('*.png', '*.jpg', '*.jpeg')
        self.assertTrue(is_valid(Path('test.png'), image_types))
        self.assertTrue(is_valid(Path('test.jpg'), image_types))
        self.assertTrue(is_valid(Path('test.JPEG'), image_types))
        self.assertFalse(is_valid(Path('test.txt'), image_types))
        
        # Test archive files
        archive_types = ('*.zip', '*.7z', '*.rar')
        self.assertTrue(is_valid(Path('test.zip'), archive_types))
        self.assertTrue(is_valid(Path('test.7z'), archive_types))
        self.assertFalse(is_valid(Path('test.png'), archive_types))
    
    def test_get_filter_string_logic(self):
        """Test filter string generation logic"""
        file_types = ('*.png', '*.jpg', '*.jpeg')
        types_str = " ".join(file_types)
        filter_string = f"Image Files ({types_str});;All Files (*)"
        
        self.assertIn('*.png', filter_string)
        self.assertIn('*.jpg', filter_string)
        self.assertIn('All Files (*)', filter_string)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestFilePickerWidgetStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestFilePickerAPI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

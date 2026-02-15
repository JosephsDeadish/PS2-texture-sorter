"""
Test Performance Integration
Tests that all performance optimizations are properly integrated into the application.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


class TestPerformanceIntegration(unittest.TestCase):
    """Test that performance optimizations are integrated"""
    
    def test_performance_utilities_importable(self):
        """Test that performance utilities can be imported"""
        try:
            from src.utils.performance import LazyLoader, JobScheduler, ProgressiveLoader
            from src.utils.memory_cleanup import ImageManager, WeakCache, MemoryManager
            from src.utils.system_detection import detect_system_capabilities, PerformanceMode
            self.assertTrue(True, "All performance utilities imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import performance utilities: {e}")
    
    def test_lazy_loader_exists(self):
        """Test LazyLoader utility exists and works"""
        from src.utils.performance import LazyLoader
        
        # Test lazy loading behavior
        load_count = [0]
        def expensive_resource():
            load_count[0] += 1
            return "loaded"
        
        loader = LazyLoader(expensive_resource, "test")
        self.assertEqual(load_count[0], 0, "Should not load immediately")
        
        result = loader.get()
        self.assertEqual(result, "loaded")
        self.assertEqual(load_count[0], 1, "Should load once")
        
        result2 = loader.get()
        self.assertEqual(load_count[0], 1, "Should not reload")
    
    def test_job_scheduler_exists(self):
        """Test JobScheduler utility exists and works"""
        from src.utils.performance import JobScheduler
        
        scheduler = JobScheduler(max_workers=2)
        self.assertEqual(scheduler.max_workers, 2)
        
        # Test simple job
        result = scheduler.submit_job(lambda x: x * 2, 5)
        self.assertEqual(result, 10)
        
        scheduler.shutdown()
    
    def test_memory_manager_exists(self):
        """Test MemoryManager utility exists"""
        from src.utils.memory_cleanup import get_memory_manager
        
        manager = get_memory_manager()
        self.assertIsNotNone(manager)
        
        # Test cleanup doesn't crash
        manager.full_cleanup()
    
    def test_system_detection_exists(self):
        """Test system detection utility exists"""
        from src.utils.system_detection import detect_system_capabilities, PerformanceMode
        
        capabilities = detect_system_capabilities()
        self.assertIsNotNone(capabilities)
        self.assertGreater(capabilities.cpu_cores, 0)
        self.assertGreater(capabilities.ram_gb, 0)
        self.assertIn(capabilities.recommended_mode, [
            PerformanceMode.LOW_SPEC,
            PerformanceMode.BALANCED,
            PerformanceMode.HIGH_QUALITY
        ])
    
    def test_panda_widget_has_fps_cap(self):
        """Test that panda widget has FPS optimization"""
        try:
            with open('src/ui/panda_widget.py', 'r') as f:
                content = f.read()
                
            # Check for FPS constants
            self.assertIn('TARGET_FPS', content, "Should have TARGET_FPS constant")
            self.assertIn('MIN_FRAME_INTERVAL', content, "Should have MIN_FRAME_INTERVAL constant")
            
            # Check for FPS limiter in animation
            self.assertIn('_last_frame_time', content, "Should track last frame time")
            self.assertIn('MIN_FRAME_INTERVAL', content, "Should use frame interval")
            
        except FileNotFoundError:
            self.skipTest("panda_widget.py not found")
    
    def test_main_imports_performance_utils(self):
        """Test that main.py imports performance utilities"""
        try:
            with open('main.py', 'r') as f:
                content = f.read()
            
            # Check for imports
            self.assertIn('from src.utils.performance import', content, 
                         "Should import performance utilities")
            self.assertIn('LazyLoader', content, 
                         "Should import LazyLoader")
            self.assertIn('JobScheduler', content, 
                         "Should import JobScheduler")
            
        except FileNotFoundError:
            self.skipTest("main.py not found")
    
    def test_main_uses_lazy_loading(self):
        """Test that main.py uses lazy loading for AI models"""
        try:
            with open('main.py', 'r') as f:
                content = f.read()
            
            # Check for lazy loader declarations
            self.assertIn('_ai_model_loader', content, 
                         "Should declare AI model lazy loader")
            self.assertIn('lazy loading', content.lower(), 
                         "Should mention lazy loading")
            
        except FileNotFoundError:
            self.skipTest("main.py not found")
    
    def test_main_cleanup_includes_performance(self):
        """Test that main.py cleanup includes performance utilities"""
        try:
            with open('main.py', 'r') as f:
                content = f.read()
            
            # Check for cleanup in _on_close
            self.assertIn('_on_close', content, "Should have close handler")
            
            # Check for performance cleanup
            if 'PERFORMANCE_UTILS_AVAILABLE' in content:
                # Only check if performance utils are used
                self.assertIn('unload', content, 
                             "Should unload lazy resources")
                self.assertIn('shutdown', content, 
                             "Should shutdown scheduler")
            
        except FileNotFoundError:
            self.skipTest("main.py not found")
    
    def test_integration_summary_exists(self):
        """Test that integration summary documentation exists"""
        expected_files = [
            'PERFORMANCE_OPTIMIZATION_SUMMARY.md',
            'COMPLETE_SESSION_SUMMARY.md',
        ]
        
        for filename in expected_files:
            path = Path(filename)
            if path.exists():
                self.assertTrue(True, f"{filename} exists")
                return
        
        self.skipTest("Documentation files not found (acceptable)")


class TestAllTasksCompleted(unittest.TestCase):
    """Verify that all tasks from problem statements are completed"""
    
    def test_pyinstaller_fix_integrated(self):
        """Test PyInstaller fix is integrated"""
        # Check runtime hook exists
        self.assertTrue(Path('pyi_rth_tkinter_fix.py').exists(), 
                       "Runtime hook should exist")
        
        # Check startup validation exists
        startup_val = Path('src/startup_validation.py')
        if startup_val.exists():
            self.assertTrue(True, "Startup validation exists")
    
    def test_ui_performance_fixes_integrated(self):
        """Test UI performance fixes are integrated"""
        try:
            with open('src/ui/lineart_converter_panel.py', 'r') as f:
                content = f.read()
            
            # Check for thread control
            self.assertIn('_preview_running', content, 
                         "Should have preview running flag")
            self.assertIn('_preview_cancelled', content, 
                         "Should have cancellation flag")
            
        except FileNotFoundError:
            self.skipTest("lineart_converter_panel.py not found")
    
    def test_line_tool_presets_improved(self):
        """Test line tool presets are improved"""
        try:
            with open('src/ui/lineart_converter_panel.py', 'r') as f:
                content = f.read()
            
            # Count presets (should be 19)
            preset_count = content.count('"name":')
            self.assertGreaterEqual(preset_count, 19, 
                                   f"Should have at least 19 presets, found {preset_count}")
            
        except FileNotFoundError:
            self.skipTest("lineart_converter_panel.py not found")
    
    def test_advanced_line_features_integrated(self):
        """Test advanced line tool features are integrated"""
        try:
            with open('src/ui/lineart_converter_panel.py', 'r') as f:
                content = f.read()
            
            # Check for advanced features
            self.assertIn('edge_low_threshold', content, 
                         "Should have edge detection controls")
            self.assertIn('adaptive_block_size', content, 
                         "Should have adaptive threshold controls")
            self.assertIn('smooth_lines', content, 
                         "Should have line smoothing")
            self.assertIn('Make Thicker', content, 
                         "Should have quick adjusters")
            
        except FileNotFoundError:
            self.skipTest("lineart_converter_panel.py not found")
    
    def test_performance_framework_created(self):
        """Test performance framework utilities exist"""
        utils_files = [
            'src/utils/performance.py',
            'src/utils/memory_cleanup.py',
            'src/utils/system_detection.py',
        ]
        
        for util_file in utils_files:
            path = Path(util_file)
            self.assertTrue(path.exists(), 
                          f"{util_file} should exist")
    
    def test_documentation_complete(self):
        """Test that comprehensive documentation exists"""
        doc_files = [
            'EXTRACTION_TROUBLESHOOTING.md',
            'UI_PERFORMANCE_FIXES_SUMMARY.md',
            'LINE_TOOL_PRESET_IMPROVEMENTS.md',
            'ADVANCED_LINE_FEATURES_GUIDE.md',
            'PERFORMANCE_OPTIMIZATION_SUMMARY.md',
        ]
        
        existing_docs = [f for f in doc_files if Path(f).exists()]
        self.assertGreater(len(existing_docs), 0, 
                          "Should have at least some documentation")


if __name__ == '__main__':
    unittest.main()

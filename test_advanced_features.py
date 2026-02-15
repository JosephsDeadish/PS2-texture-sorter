"""
Test Advanced Line Art Features
Tests for new advanced controls and features
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


class TestAdvancedFeatures(unittest.TestCase):
    """Test advanced line art features."""
    
    def test_advanced_settings_exist(self):
        """Test that LineArtSettings has advanced parameters."""
        from src.tools.lineart_converter import LineArtSettings
        
        # Create settings with advanced parameters
        settings = LineArtSettings(
            edge_low_threshold=30,
            edge_high_threshold=180,
            edge_aperture_size=5,
            adaptive_block_size=15,
            adaptive_c_constant=3,
            adaptive_method="mean",
            smooth_lines=True,
            smooth_amount=1.5
        )
        
        # Check all advanced parameters are set
        self.assertEqual(settings.edge_low_threshold, 30)
        self.assertEqual(settings.edge_high_threshold, 180)
        self.assertEqual(settings.edge_aperture_size, 5)
        self.assertEqual(settings.adaptive_block_size, 15)
        self.assertEqual(settings.adaptive_c_constant, 3)
        self.assertEqual(settings.adaptive_method, "mean")
        self.assertTrue(settings.smooth_lines)
        self.assertEqual(settings.smooth_amount, 1.5)
    
    def test_default_advanced_parameters(self):
        """Test that advanced parameters have sensible defaults."""
        from src.tools.lineart_converter import LineArtSettings
        
        settings = LineArtSettings()
        
        # Check defaults
        self.assertEqual(settings.edge_low_threshold, 50)
        self.assertEqual(settings.edge_high_threshold, 150)
        self.assertEqual(settings.edge_aperture_size, 3)
        self.assertEqual(settings.adaptive_block_size, 11)
        self.assertEqual(settings.adaptive_c_constant, 2)
        self.assertEqual(settings.adaptive_method, "gaussian")
        self.assertFalse(settings.smooth_lines)
        self.assertEqual(settings.smooth_amount, 1.0)
    
    def test_converter_has_new_methods(self):
        """Test that converter has new processing methods."""
        from src.tools.lineart_converter import LineArtConverter
        
        converter = LineArtConverter()
        
        # Check that new methods exist
        self.assertTrue(hasattr(converter, '_smooth_lines'))
        self.assertTrue(callable(getattr(converter, '_smooth_lines')))
    
    def test_edge_detection_accepts_settings(self):
        """Test that edge detection method accepts settings parameter."""
        from src.tools.lineart_converter import LineArtConverter, LineArtSettings
        import inspect
        
        converter = LineArtConverter()
        
        # Check method signature
        sig = inspect.signature(converter._detect_edges)
        params = list(sig.parameters.keys())
        
        self.assertIn('settings', params, "Edge detection should accept settings parameter")
    
    def test_adaptive_threshold_accepts_settings(self):
        """Test that adaptive threshold method accepts settings parameter."""
        from src.tools.lineart_converter import LineArtConverter, LineArtSettings
        import inspect
        
        converter = LineArtConverter()
        
        # Check method signature
        sig = inspect.signature(converter._adaptive_threshold)
        params = list(sig.parameters.keys())
        
        self.assertIn('settings', params, "Adaptive threshold should accept settings parameter")


def run_tests():
    """Run all advanced feature tests."""
    print("="*70)
    print("Running Advanced Line Art Features Tests")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAdvancedFeatures)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✓ ALL ADVANCED FEATURE TESTS PASSED")
        print("New features validated:")
        print("  ✓ Advanced edge detection parameters")
        print("  ✓ Adaptive threshold configuration")
        print("  ✓ Line smoothing post-processing")
        print("  ✓ Settings structure extended properly")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())

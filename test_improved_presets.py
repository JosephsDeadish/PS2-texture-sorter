"""
Test Improved Line Art Presets
Validates that all presets have proper settings and descriptions
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


class TestImprovedPresets(unittest.TestCase):
    """Test improved line art presets."""
    
    def test_preset_count_increased(self):
        """Test that we added new presets."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        # Should have original 11 + 8 new = 19 presets
        self.assertEqual(len(LINEART_PRESETS), 19, 
                        f"Should have 19 presets, found {len(LINEART_PRESETS)}")
    
    def test_all_presets_have_required_fields(self):
        """Test that all presets have all required settings."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        required_fields = [
            'desc', 'mode', 'threshold', 'auto_threshold', 'background',
            'invert', 'remove_midtones', 'midtone_threshold', 'contrast',
            'sharpen', 'sharpen_amount', 'morphology', 'morph_iter',
            'kernel', 'denoise', 'denoise_size'
        ]
        
        for preset_name, preset_data in LINEART_PRESETS.items():
            for field in required_fields:
                self.assertIn(field, preset_data, 
                            f"Preset '{preset_name}' missing field '{field}'")
    
    def test_new_presets_exist(self):
        """Test that new specialized presets were added."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        new_presets = [
            "🎨 Watercolor Lines",
            "✍️ Handdrawn / Natural",
            "🏛️ Engraving / Crosshatch",
            "🎭 Screen Print / Posterize",
            "📸 Photo to Sketch",
            "🖼️ Art Nouveau Lines",
            "⚫ High Contrast B&W",
            "🔥 Graffiti / Street Art",
        ]
        
        for preset_name in new_presets:
            self.assertIn(preset_name, LINEART_PRESETS,
                         f"New preset '{preset_name}' not found")
    
    def test_original_presets_still_exist(self):
        """Test that original presets are still present."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        original_presets = [
            "⭐ Clean Ink Lines",
            "✏️ Pencil Sketch",
            "🖊️ Bold Outlines",
            "🔍 Fine Detail Lines",
            "💥 Comic Book Inks",
            "📖 Manga Lines",
            "🖍️ Coloring Book",
            "📐 Blueprint / Technical",
            "✂️ Stencil / Vinyl Cut",
            "🪵 Woodcut / Linocut",
            "🖋️ Tattoo Stencil",
        ]
        
        for preset_name in original_presets:
            self.assertIn(preset_name, LINEART_PRESETS,
                         f"Original preset '{preset_name}' missing")
    
    def test_preset_parameter_improvements(self):
        """Test that presets have improved parameters."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        # Check Clean Ink Lines has better parameters
        clean_ink = LINEART_PRESETS["⭐ Clean Ink Lines"]
        self.assertEqual(clean_ink["threshold"], 135, "Clean Ink threshold should be 135")
        self.assertEqual(clean_ink["contrast"], 1.6, "Clean Ink contrast should be 1.6")
        self.assertEqual(clean_ink["morphology"], "close", "Clean Ink should use close morphology")
        
        # Check Bold Outlines is more bold
        bold = LINEART_PRESETS["🖊️ Bold Outlines"]
        self.assertEqual(bold["morph_iter"], 3, "Bold Outlines should have 3 iterations")
        self.assertEqual(bold["kernel"], 5, "Bold Outlines should use kernel 5")
        
        # Check Fine Detail Lines preserves detail better
        fine = LINEART_PRESETS["🔍 Fine Detail Lines"]
        self.assertEqual(fine["sharpen_amount"], 2.2, "Fine Detail should sharpen more")
        self.assertEqual(fine["denoise_size"], 1, "Fine Detail should denoise minimally")
    
    def test_preset_descriptions_are_descriptive(self):
        """Test that all presets have meaningful descriptions."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        for preset_name, preset_data in LINEART_PRESETS.items():
            desc = preset_data['desc']
            self.assertGreater(len(desc), 20,
                             f"Preset '{preset_name}' description too short: {desc}")
            # Description should describe the purpose/style
            self.assertTrue(any(word in desc.lower() for word in 
                              ['line', 'style', 'art', 'for', 'like', 'with']),
                          f"Preset '{preset_name}' description not descriptive: {desc}")
    
    def test_valid_conversion_modes(self):
        """Test that all presets use valid conversion modes."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        valid_modes = ["pure_black", "threshold", "stencil_1bit", 
                      "edge_detect", "adaptive", "sketch"]
        
        for preset_name, preset_data in LINEART_PRESETS.items():
            mode = preset_data['mode']
            self.assertIn(mode, valid_modes,
                         f"Preset '{preset_name}' has invalid mode: {mode}")
    
    def test_valid_morphology_operations(self):
        """Test that all presets use valid morphology operations."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        valid_operations = ["none", "dilate", "erode", "close", "open"]
        
        for preset_name, preset_data in LINEART_PRESETS.items():
            operation = preset_data['morphology']
            self.assertIn(operation, valid_operations,
                         f"Preset '{preset_name}' has invalid morphology: {operation}")
    
    def test_parameter_ranges(self):
        """Test that all preset parameters are within valid ranges."""
        from src.ui.lineart_converter_panel import LINEART_PRESETS
        
        for preset_name, preset_data in LINEART_PRESETS.items():
            # Threshold: 0-255
            self.assertGreaterEqual(preset_data['threshold'], 0)
            self.assertLessEqual(preset_data['threshold'], 255)
            
            # Contrast: typically 0.1-5.0
            self.assertGreater(preset_data['contrast'], 0)
            self.assertLessEqual(preset_data['contrast'], 5.0)
            
            # Sharpen amount: typically 0.5-3.0
            self.assertGreater(preset_data['sharpen_amount'], 0)
            self.assertLessEqual(preset_data['sharpen_amount'], 5.0)
            
            # Morphology iterations: 1-10
            self.assertGreaterEqual(preset_data['morph_iter'], 1)
            self.assertLessEqual(preset_data['morph_iter'], 10)
            
            # Kernel size: 3, 5, 7, or 9
            self.assertIn(preset_data['kernel'], [3, 5, 7, 9])
            
            # Denoise size: 1-10
            self.assertGreaterEqual(preset_data['denoise_size'], 1)
            self.assertLessEqual(preset_data['denoise_size'], 10)


def run_tests():
    """Run all preset tests."""
    print("="*70)
    print("Running Improved Line Art Presets Tests")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestImprovedPresets)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✓ ALL PRESET TESTS PASSED")
        print("Improvements verified:")
        print("  ✓ 19 total presets (11 improved + 8 new)")
        print("  ✓ All presets have proper settings")
        print("  ✓ Parameter improvements validated")
        print("  ✓ New specialized presets added")
        print("  ✓ All descriptions are descriptive")
        print("  ✓ Valid modes and operations")
        print("  ✓ Parameters within valid ranges")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())

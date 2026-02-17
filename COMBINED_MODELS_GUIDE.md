# Combined Feature Extractors - Implementation Guide

## Overview

The Organizer Settings Panel now supports **7 feature extractor presets**, including 4 combined model configurations that use multiple AI models simultaneously for improved accuracy.

## Available Presets

### Single Models

1. **CLIP (image-to-text classification)**
   - Uses OpenAI's CLIP model
   - Best for: Images with text, UI elements, labeled content
   - Speed: Fast (~0.5s per image)

2. **DINOv2 (visual similarity clustering)**
   - Uses Meta's DINOv2 model
   - Best for: Visual patterns, textures, similar objects
   - Speed: Medium (~0.8s per image)

3. **timm (PyTorch Image Models)**
   - Uses EfficientNet from timm library
   - Best for: General image classification
   - Speed: Very Fast (~0.3s per image)
   - **Note: NOT compiled with TorchScript** (prevents source access errors)

### Combined Models

4. **CLIP+DINOv2 (Combined: text + visual)**
   - Combines text understanding + visual similarity
   - Best for: Complex categorization needing both approaches
   - Speed: Slower (~1.3s per image)
   - ⚠️ Performance warning shown

5. **CLIP+timm (Combined: text + PyTorch)**
   - Combines text understanding + general classification
   - Best for: Text-heavy images with general content
   - Speed: Medium-Slow (~0.8s per image)
   - ⚠️ Performance warning shown

6. **DINOv2+timm (Combined: visual + PyTorch)**
   - Combines visual similarity + general classification
   - Best for: Texture/pattern categorization
   - Speed: Medium (~1.1s per image)
   - ⚠️ Performance warning shown

7. **CLIP+DINOv2+timm (All three combined)**
   - Uses all three models simultaneously
   - Best for: Maximum accuracy, complex multi-faceted categorization
   - Speed: Slowest (~1.6s per image)
   - ⚠️ Strong performance warning shown

## UI Implementation

### Feature Extractor Dropdown

Located in: `src/ui/organizer_settings_panel.py`

The dropdown automatically:
- Shows/hides relevant model-specific dropdowns (CLIP Model, DINOv2 Model)
- Displays performance warnings for combined models
- Saves selection to configuration

### Performance Warnings

Combined models display automatic warnings:

**2-model combinations:**
```
⚠️ Warning: CLIP+DINOv2 combines two models, which may reduce processing 
speed. This provides better accuracy but takes longer than single models.
```

**3-model combination:**
```
⚠️ Warning: Using all three models (CLIP+DINOv2+timm) will significantly 
impact performance. Processing will be slower but may provide better accuracy 
for complex categorization tasks.
```

## Backend Implementation

### Combined Feature Extractor Class

Located in: `src/organizer/combined_feature_extractor.py`

```python
from src.organizer.combined_feature_extractor import create_feature_extractor

# Create extractor from settings
settings = {'feature_extractor': 'CLIP+DINOv2 (Combined: text + visual)'}
extractor = create_feature_extractor(settings)

# Extract features from image
features = extractor.extract_features(image_path)

# Check if combined
if extractor.is_combined():
    print(f"Using {extractor.get_model_count()} models")
```

### Feature Extraction Process

For combined models:
1. Each model extracts features independently
2. Features are concatenated into a single vector
3. If one model fails, others continue
4. Combined feature vector is returned

### Example Usage

```python
from pathlib import Path
from src.organizer.combined_feature_extractor import (
    CombinedFeatureExtractor,
    estimate_processing_time
)

# Initialize with combined model
extractor = CombinedFeatureExtractor("CLIP+DINOv2 (Combined: text + visual)")

# Extract features
image_path = Path("texture.png")
features = extractor.extract_features(image_path)

print(f"Feature vector shape: {features.shape}")
print(f"Using models: {extractor.get_model_names()}")

# Estimate processing time
time_s, time_str = estimate_processing_time("CLIP+DINOv2+timm", num_images=100)
print(f"Estimated time for 100 images: {time_str}")
```

## Performance Characteristics

### Processing Time Estimates

| Configuration | Single Image | 100 Images | 1000 Images |
|--------------|--------------|------------|-------------|
| CLIP | ~0.5s | ~50s | ~8 min |
| DINOv2 | ~0.8s | ~80s | ~13 min |
| timm | ~0.3s | ~30s | ~5 min |
| CLIP+DINOv2 | ~1.3s | ~130s | ~22 min |
| CLIP+timm | ~0.8s | ~80s | ~13 min |
| DINOv2+timm | ~1.1s | ~110s | ~18 min |
| CLIP+DINOv2+timm | ~1.6s | ~160s | ~27 min |

*Note: Times are estimates and vary based on hardware*

### Memory Usage

Combined models require more memory:
- Single model: ~500 MB - 1 GB
- 2-model combination: ~1.5 GB - 2 GB
- 3-model combination: ~2.5 GB - 3 GB

### Accuracy Benefits

Combined models can provide better accuracy when:
- Categories are complex and multi-faceted
- Images have both text and visual elements
- High precision is critical
- Processing time is not a constraint

## TorchScript Safety

### timm Models

**IMPORTANT:** timm models are **NOT** compiled with TorchScript.

Located in: `src/vision_models/efficientnet_model.py`

```python
# Standard model loading (NO TorchScript)
self.model = timm.create_model(model_name, pretrained=pretrained, num_classes=0)
self.model = self.model.to(self.device)
self.model.eval()  # Standard eval mode, NOT torch.jit.script()
```

**What's NOT used:**
- ❌ `torch.jit.script()`
- ❌ `torch.jit.trace()`
- ❌ `torch.jit.compile()`

This prevents source access errors when Settings inspects the model.

## Configuration Storage

Settings are stored in the config file:

```json
{
  "organizer": {
    "feature_extractor": "CLIP+DINOv2 (Combined: text + visual)",
    "clip_model": "CLIP_ViT-B/32 (340 MB - Balanced)",
    "dinov2_model": "DINOv2_base (340 MB - Balanced)",
    ...
  }
}
```

## Best Practices

### When to Use Single Models

- **CLIP**: Text-heavy images, UI elements, labeled content
- **DINOv2**: Visual patterns, textures, similar objects
- **timm**: General images, fastest processing

### When to Use Combined Models

- **CLIP+DINOv2**: Images with both text and visual patterns
- **CLIP+timm**: Text content with general classification needs
- **DINOv2+timm**: Visual patterns with general classification
- **All three**: Maximum accuracy needed, time is not critical

### Recommendations

1. **Start with single models** - Test with CLIP or DINOv2 first
2. **Use combined models for challenging datasets** - When single models don't achieve desired accuracy
3. **Consider processing time** - Combined models are 2-3x slower
4. **Monitor memory usage** - Ensure sufficient RAM for combined models
5. **Batch processing** - For large datasets, consider overnight processing with 3-model combination

## Testing

### Validation Script

Run validation:
```bash
python validate_feature_extractor.py
```

Checks:
- ✅ All 7 presets present
- ✅ Performance warning implementation
- ✅ Combined model detection
- ✅ No TorchScript compilation

### Manual Testing

Test the UI:
```bash
python test_organizer_settings_ui.py
```

This shows the settings panel with:
- All 7 preset options
- Dynamic model dropdown visibility
- Performance warnings for combined models

## Troubleshooting

### Performance Issues

**Problem:** Combined models are too slow

**Solutions:**
1. Use single models for initial categorization
2. Process in batches overnight
3. Upgrade hardware (GPU recommended)
4. Use CLIP or timm alone for faster processing

### Memory Errors

**Problem:** Out of memory with 3-model combination

**Solutions:**
1. Close other applications
2. Process smaller batches
3. Use 2-model combinations instead
4. Upgrade RAM

### Model Initialization Fails

**Problem:** One model fails to load in combination

**Solutions:**
1. Check model files are downloaded
2. Verify dependencies installed
3. Check error logs
4. Other models will continue working

## Version History

- **v2.0** (PR #168) - Added combined model support with 7 presets
- **v1.0** (PR #168) - Initial implementation with 3 single models

## Related Files

- `src/ui/organizer_settings_panel.py` - UI implementation
- `src/organizer/combined_feature_extractor.py` - Backend logic
- `src/vision_models/efficientnet_model.py` - timm implementation
- `src/vision_models/clip_model.py` - CLIP implementation
- `src/vision_models/dinov2_model.py` - DINOv2 implementation
- `validate_feature_extractor.py` - Validation script
- `test_organizer_settings_ui.py` - UI test

## Author

Implementation by GitHub Copilot for PR #168

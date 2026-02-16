# Feature Extractor Dropdown Implementation

## Overview

This document describes the implementation of the Feature Extractor dropdown in the Organizer Settings Panel, added as part of PR #168.

## Problem Statement

The Organizer Settings Panel needed a unified Feature Extractor dropdown to allow users to choose between different AI models for texture classification:
- CLIP (image-to-text classification)
- DINOv2 (visual similarity clustering)  
- timm (PyTorch Image Models)

Additionally, timm models needed to be verified as NOT using TorchScript compilation to avoid source access errors in Settings.

## Implementation

### File: `src/ui/organizer_settings_panel.py`

#### 1. Feature Extractor Dropdown (Lines 50-64)

Added a new dropdown selector above the existing CLIP and DINOv2 model selectors:

```python
# Feature Extractor selector
extractor_layout = QHBoxLayout()
extractor_label = QLabel("Feature Extractor:")
extractor_label.setMinimumWidth(100)
self.extractor_combo = QComboBox()
self.extractor_combo.addItems([
    "CLIP (image-to-text classification)",
    "DINOv2 (visual similarity clustering)",
    "timm (PyTorch Image Models)"
])
self.extractor_combo.currentTextChanged.connect(self.on_extractor_changed)
```

#### 2. Conditional Visibility System

Modified CLIP and DINOv2 selectors to use instance variables for their layouts:
- `self.clip_layout` (Line 67)
- `self.dinov2_layout` (Line 82)

This enables dynamic show/hide based on the selected feature extractor.

#### 3. Event Handler (Lines 299-314)

```python
def on_extractor_changed(self):
    """Update model-specific dropdown visibility based on selected feature extractor"""
    extractor = self.extractor_combo.currentText()
    
    # Hide all model-specific dropdowns first
    self.set_layout_visible(self.clip_layout, False)
    self.set_layout_visible(self.dinov2_layout, False)
    
    # Show the relevant dropdown based on selection
    if "CLIP" in extractor:
        self.set_layout_visible(self.clip_layout, True)
    elif "DINOv2" in extractor:
        self.set_layout_visible(self.dinov2_layout, True)
    # For timm, no specific model dropdown is shown
    
    self.emit_settings()
```

#### 4. Layout Visibility Helper (Lines 316-321)

```python
def set_layout_visible(self, layout, visible):
    """Set visibility for all widgets in a layout"""
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item.widget():
            item.widget().setVisible(visible)
```

#### 5. Settings Integration

**Load Settings (Lines 367-372):**
```python
# Load Feature Extractor
if 'feature_extractor' in org_config:
    extractor_text = org_config['feature_extractor']
    idx = self.extractor_combo.findText(extractor_text, Qt.MatchFlag.MatchContains)
    if idx >= 0:
        self.extractor_combo.setCurrentIndex(idx)
```

**Emit Settings (Line 387):**
```python
settings = {
    'feature_extractor': self.extractor_combo.currentText(),
    'clip_model': self.clip_combo.currentText(),
    'dinov2_model': self.dinov2_combo.currentText(),
    # ... other settings
}
```

**Get Settings (Line 407):**
```python
return {
    'feature_extractor': self.extractor_combo.currentText(),
    'clip_model': self.clip_combo.currentText(),
    'dinov2_model': self.dinov2_combo.currentText(),
    # ... other settings
}
```

## TorchScript Safety

### File: `src/vision_models/efficientnet_model.py`

Verified that timm models are **NOT** compiled with TorchScript:

```python
# Line 54 - Standard model loading (NO TorchScript)
self.model = timm.create_model(model_name, pretrained=pretrained, num_classes=0)
self.model = self.model.to(self.device)
self.model.eval()  # Standard eval mode, NOT torch.jit.script()
```

**What's NOT present (good):**
- ❌ `torch.jit.script()`
- ❌ `torch.jit.trace()`
- ❌ `torch.jit.compile()`
- ❌ `@torch.jit.script` decorator

This prevents source access errors that can occur when Settings tries to inspect TorchScript-compiled models.

## User Interface

### Before Selection
```
🧠 AI Model Selection
┌────────────────────────────────────────────┐
│ Feature Extractor: [CLIP (image-to-tex...▼]│
│ CLIP Model:        [CLIP_ViT-B/32... ▼]    │
│ (DINOv2 Model hidden)                      │
│ Organization Mode: [Suggested...      ▼]    │
└────────────────────────────────────────────┘
```

### When CLIP Selected
- ✅ CLIP Model dropdown **visible**
- ❌ DINOv2 Model dropdown **hidden**

### When DINOv2 Selected  
- ❌ CLIP Model dropdown **hidden**
- ✅ DINOv2 Model dropdown **visible**

### When timm Selected
- ❌ CLIP Model dropdown **hidden**
- ❌ DINOv2 Model dropdown **hidden**
- (Uses default timm models from efficientnet_model.py)

## Testing

### Test File: `test_organizer_settings_ui.py`

Updated config to include `feature_extractor`:

```python
config = {
    'organizer': {
        'feature_extractor': 'CLIP (image-to-text classification)',
        'clip_model': 'CLIP_ViT-B/32 (340 MB - Balanced)',
        'dinov2_model': 'DINOv2_base (340 MB - Balanced)',
        # ... other settings
    }
}
```

### Validation Script: `validate_feature_extractor.py`

Created automated validation that checks:
- ✅ Feature Extractor dropdown exists
- ✅ All three options present (CLIP, DINOv2, timm)
- ✅ Event handler implemented
- ✅ Visibility methods implemented
- ✅ Settings integration complete
- ✅ No TorchScript compilation in timm

Run with:
```bash
python validate_feature_extractor.py
```

## Backend Integration

The selected feature extractor can be used by backend code:

```python
# In organizer tool code
settings = organizer_settings_panel.get_settings()
extractor = settings['feature_extractor']

if 'CLIP' in extractor:
    # Use CLIP model
    clip_model = settings['clip_model']
    # Initialize CLIP with selected variant
elif 'DINOv2' in extractor:
    # Use DINOv2 model
    dinov2_model = settings['dinov2_model']
    # Initialize DINOv2 with selected variant
elif 'timm' in extractor:
    # Use timm/EfficientNet model
    from src.vision_models.efficientnet_model import EfficientNetModel
    model = EfficientNetModel('efficientnet_b0')
```

## Configuration Storage

Settings are stored in the config file under `organizer` section:

```json
{
  "organizer": {
    "feature_extractor": "CLIP (image-to-text classification)",
    "clip_model": "CLIP_ViT-B/32 (340 MB - Balanced)",
    "dinov2_model": "DINOv2_base (340 MB - Balanced)",
    "organization_mode": "Suggested (AI suggests, you confirm)",
    "confidence_threshold": 75,
    ...
  }
}
```

## Benefits

1. **Unified Selection**: Single dropdown to choose the AI model type
2. **Clean UI**: Only shows relevant model options based on selection
3. **Backward Compatible**: Existing CLIP/DINOv2 settings still work
4. **Extensible**: Easy to add new feature extractors in the future
5. **Safe**: timm models avoid TorchScript compilation issues

## Future Enhancements

Potential improvements for future versions:

1. **Model Comparison**: Show performance/speed metrics for each extractor
2. **Auto-Selection**: Suggest best extractor based on image type
3. **Hybrid Mode**: Use multiple extractors for better accuracy
4. **Custom Models**: Allow users to load their own feature extractors
5. **Benchmarking**: Built-in tool to compare extractors on sample images

## Related Files

- `src/ui/organizer_settings_panel.py` - Main implementation
- `src/vision_models/efficientnet_model.py` - timm backend
- `src/vision_models/clip_model.py` - CLIP backend
- `src/vision_models/dinov2_model.py` - DINOv2 backend
- `test_organizer_settings_ui.py` - UI test
- `validate_feature_extractor.py` - Validation script

## Version History

- **v1.0** (PR #168) - Initial implementation with CLIP, DINOv2, and timm support

## Author

Implementation by GitHub Copilot for PR #168

# Advanced Line Tool Features Guide

## Overview
This guide covers the advanced features and fine-tuning controls added to the Line Art Converter tool, giving you precise control over the line art conversion process.

## Table of Contents
1. [Quick Line Weight Adjusters](#quick-line-weight-adjusters)
2. [Advanced Edge Detection](#advanced-edge-detection)
3. [Advanced Adaptive Thresholding](#advanced-adaptive-thresholding)
4. [Post-Processing Line Smoothing](#post-processing-line-smoothing)
5. [Usage Examples](#usage-examples)
6. [Tips & Tricks](#tips--tricks)

---

## Quick Line Weight Adjusters

### Make Thicker Button (➕)
**Purpose**: Instantly make lines thicker and bolder

**What it does**:
- Sets morphology operation to "dilate" if not already active
- Increases morphology iterations by 1 (up to 10)
- Optionally increases kernel size for stronger effect
- Automatically updates preview

**When to use**:
- Lines are too thin or faint
- Creating bold cartoon or graffiti styles
- Making stickers or designs that need strong outlines
- Coloring books that need thick borders

**Example Workflow**:
1. Load an image and apply "Clean Ink Lines" preset
2. If lines are too thin, click "Make Thicker" 1-3 times
3. Preview updates automatically

### Make Thinner Button (➖)
**Purpose**: Instantly make lines thinner and more delicate

**What it does**:
- Sets morphology operation to "erode" if not already active
- Increases erosion iterations by 1 (up to 10)
- Automatically updates preview

**When to use**:
- Lines are too thick or overlapping
- Creating fine detail illustrations
- Technical or architectural drawings
- Delicate art styles

**Example Workflow**:
1. Load an image and apply "Bold Outlines" preset
2. If lines are too thick, click "Make Thinner" 1-2 times
3. Fine-tune with other controls as needed

---

## Advanced Edge Detection

Enable these controls by checking **"⚙️ Advanced Settings"**

### Low Threshold Slider
**Range**: 0-255  
**Default**: 50  
**Effect**: Controls sensitivity to weak edges

- **Lower values (10-40)**: Detects more subtle edges, may include noise
- **Medium values (50-80)**: Balanced detection (recommended)
- **Higher values (80-120)**: Only strong edges detected, cleaner result

### High Threshold Slider
**Range**: 0-255  
**Default**: 150  
**Effect**: Controls which edges are considered strong

- **Lower values (100-140)**: More edges classified as strong
- **Medium values (150-180)**: Balanced (recommended)
- **Higher values (180-220)**: Only very strong edges kept

**Rule of Thumb**: High threshold should be 2-3× the low threshold

### Aperture Size
**Options**: 3, 5, 7  
**Default**: 3  
**Effect**: Size of Sobel operator kernel

- **3**: Fastest, good for most images
- **5**: More accurate edge detection, slightly slower
- **7**: Most accurate, best for high-resolution images

### When to Use Edge Detection Controls

**Noisy Images**:
```
Low Threshold: 60-80 (higher to ignore noise)
High Threshold: 180-200
Aperture: 3
```

**Fine Detail Images**:
```
Low Threshold: 30-40
High Threshold: 120-150
Aperture: 5 or 7
```

**Clean, Simple Images**:
```
Low Threshold: 50
High Threshold: 150
Aperture: 3 (default)
```

---

## Advanced Adaptive Thresholding

Enable these controls by checking **"⚙️ Advanced Settings"**

### Block Size Slider
**Range**: 3-51 (must be odd)  
**Default**: 11  
**Effect**: Size of local neighborhood for threshold calculation

- **Small (3-9)**: Adapts quickly to local variations, good for varying lighting
- **Medium (11-21)**: Balanced, works for most images (recommended)
- **Large (23-51)**: Smoother result, less sensitive to local variations

### C Constant Slider
**Range**: -10 to 10  
**Default**: 2  
**Effect**: Constant subtracted from weighted mean

- **Negative values (-10 to 0)**: More pixels become white, lighter result
- **Zero (0)**: Pure local mean threshold
- **Small positive (1-3)**: Slightly darker, good for clean lines
- **Large positive (4-10)**: More pixels become black, darker result

### Method Selection
**Options**: Gaussian, Mean  
**Default**: Gaussian

**Gaussian Method**:
- Uses Gaussian-weighted mean of neighborhood
- Smoother transitions between regions
- Better for images with gradual lighting changes
- **Recommended for photos and natural images**

**Mean Method**:
- Uses simple mean of neighborhood
- Sharper transitions
- Faster processing
- **Recommended for drawings and clean line art**

### When to Use Adaptive Threshold Controls

**Photos with Uneven Lighting**:
```
Block Size: 15-25 (larger blocks)
C Constant: 2-3
Method: Gaussian
```

**Hand-drawn Sketches**:
```
Block Size: 9-13
C Constant: 1-2
Method: Mean
```

**Technical Drawings**:
```
Block Size: 11
C Constant: 0-1
Method: Mean
```

**Watercolor or Soft Art**:
```
Block Size: 21-31 (very large)
C Constant: 3-5
Method: Gaussian
```

---

## Post-Processing: Line Smoothing

Enable these controls by checking **"⚙️ Advanced Settings"**

### Smooth Lines Toggle
**Purpose**: Apply edge-preserving smoothing to reduce jaggedness

**When enabled**:
- Uses bilateral filter (CV2) or smooth filter (PIL fallback)
- Smooths lines while preserving edges
- Reduces artifacts and noise
- Creates cleaner, more professional-looking lines

### Smooth Amount Slider
**Range**: 0.5-3.0  
**Default**: 1.0  
**Effect**: Controls intensity of smoothing

- **Light (0.5-1.0)**: Subtle smoothing, minimal change
- **Medium (1.0-1.5)**: Balanced smoothing (recommended)
- **Heavy (1.5-3.0)**: Strong smoothing, may lose some detail

### When to Use Line Smoothing

**✅ Good For**:
- Scanned hand-drawn artwork (removes paper texture)
- Digital sketches with jagged lines
- Vectorization preparation
- Print-ready line art
- Comic book inking

**❌ Not Recommended For**:
- Technical drawings (preserve sharp corners)
- Pixel art (will blur intentional pixels)
- Already clean vector-based art
- When you want maximum detail preservation

### Smoothing Examples

**Light Touch-Up**:
```
Smooth Lines: ✓ Enabled
Smooth Amount: 0.8
Use with: Clean Ink Lines preset
Result: Slightly cleaner professional lines
```

**Medium Cleanup**:
```
Smooth Lines: ✓ Enabled
Smooth Amount: 1.5
Use with: Pencil Sketch preset
Result: Smoother pencil strokes, less paper texture
```

**Heavy Smoothing**:
```
Smooth Lines: ✓ Enabled
Smooth Amount: 2.5
Use with: Hand-drawn sketches
Result: Very smooth, almost vector-like quality
```

---

## Usage Examples

### Example 1: Perfect Comic Book Inks

**Goal**: Clean, professional comic book style inks

1. Load your pencil sketch
2. Apply "💥 Comic Book Inks" preset
3. Open Advanced Settings
4. Adjust if needed:
   - If lines too thin: Click "Make Thicker" once
   - If edges too rough: Enable "Smooth Lines" (amount: 1.2)
5. Result: Professional comic inks ready for coloring

### Example 2: Technical Drawing from Photo

**Goal**: Clean line drawing from photograph

1. Load photograph
2. Apply "📐 Blueprint / Technical" preset
3. Open Advanced Settings
4. Fine-tune edge detection:
   - Low Threshold: 40
   - High Threshold: 130
   - Aperture: 5
5. If needed: Click "Make Thinner" to clean up
6. Result: Clean technical line drawing

### Example 3: Manga/Anime Style

**Goal**: Clean manga lines with smooth curves

1. Load sketch or screenshot
2. Apply "📖 Manga Lines" preset
3. Open Advanced Settings
4. Enable smoothing:
   - Smooth Lines: ✓
   - Smooth Amount: 1.3
5. Fine-tune line weight with quick adjusters
6. Result: Smooth, professional manga-style lines

### Example 4: Handdrawn Watercolor Lines

**Goal**: Soft lines for watercolor painting

1. Load pencil sketch
2. Apply "🎨 Watercolor Lines" preset
3. Open Advanced Settings
4. Adjust adaptive threshold:
   - Block Size: 25 (larger for softer)
   - C Constant: 4
   - Method: Gaussian
5. Do NOT use smoothing (want natural texture)
6. Result: Soft, natural lines perfect for watercolor

### Example 5: Recovery from Noisy Scan

**Goal**: Clean lines from noisy scanned artwork

1. Load noisy scan
2. Start with "⭐ Clean Ink Lines" preset
3. Open Advanced Settings
4. Adjust edge detection:
   - Low Threshold: 70 (higher to ignore noise)
   - High Threshold: 190
5. Enable Post-Processing:
   - Smooth Lines: ✓
   - Smooth Amount: 1.8
   - Denoise: ✓ (in main settings)
   - Denoise Size: 4
6. Result: Clean lines with noise removed

---

## Tips & Tricks

### General Tips

1. **Start with a Preset**: Always begin with the closest preset to your goal
2. **Use Quick Adjusters First**: Try the Make Thicker/Thinner buttons before diving into advanced settings
3. **Preview Often**: Enable live preview to see changes immediately
4. **Iterate Gradually**: Make small adjustments and check results
5. **Save Custom Presets**: Once you find settings that work, save them as a custom preset

### Advanced Tips

**Tip 1: Layered Approach**
- Run image through multiple passes with different settings
- First pass: Extract main lines
- Second pass: Extract fine details
- Combine in your image editor

**Tip 2: Edge Detection + Adaptive Threshold**
- Use Edge Detection mode for mechanical/technical subjects
- Use Adaptive Threshold for organic/hand-drawn subjects
- Mix both for mixed-content images

**Tip 3: Morphology Mastery**
- "Dilate" then "Erode" = "Close" (closes small gaps)
- "Erode" then "Dilate" = "Open" (removes small details)
- Use Close for coloring books
- Use Open for cleaning up noise

**Tip 4: Smoothing Sweet Spot**
- Amount 0.8-1.2 for most artwork
- Amount 1.5-2.0 for heavy cleanup
- Amount below 1.0 for subtle touch-up
- Always check 100% zoom to see actual effect

**Tip 5: Adaptive Threshold Troubleshooting**
- If result too dark: Decrease C constant or increase block size
- If result too light: Increase C constant or decrease block size
- If too sensitive to variations: Increase block size
- If losing detail: Decrease block size

### Performance Tips

1. **Collapse Advanced Settings**: Keep advanced settings collapsed when not in use
2. **Disable Live Preview**: For very large images, disable live preview during bulk adjustments
3. **Use Lower Resolution Preview**: Preview with smaller test image first
4. **Batch Similar Images**: Group similar images and use same settings for faster workflow

### Troubleshooting

**Problem**: Lines disappearing
**Solution**: Lower threshold or adjust edge detection low threshold

**Problem**: Too much noise in result
**Solution**: Increase denoise size, raise edge detection thresholds, or increase adaptive block size

**Problem**: Lines too jagged
**Solution**: Enable line smoothing with amount 1.0-1.5

**Problem**: Lost fine details
**Solution**: Decrease adaptive block size, lower denoise settings, disable smoothing

**Problem**: Uneven results across image
**Solution**: Use adaptive threshold mode instead of simple threshold, adjust block size

---

## Keyboard Shortcuts & Workflow

### Recommended Workflow

1. **Select preset** (closest to desired result)
2. **Preview** with sample image
3. **Quick adjust** using Make Thicker/Thinner buttons
4. **Fine-tune** in advanced settings if needed
5. **Save preset** if you'll reuse these settings
6. **Batch process** your images

### Quick Reference Card

```
Quick Adjusters:
  Make Thicker  ➜  Bolder, thicker lines
  Make Thinner  ➜  Finer, thinner lines

Edge Detection (for technical/photo):
  Low Thresh    ➜  Noise sensitivity
  High Thresh   ➜  Edge strength
  Aperture      ➜  Detection accuracy

Adaptive Threshold (for drawings):
  Block Size    ➜  Local adaptation size
  C Constant    ➜  Brightness bias
  Method        ➜  Gaussian or Mean

Post-Processing:
  Smooth Lines  ➜  Reduce jaggedness
  Smooth Amount ➜  Smoothing intensity
```

---

## Summary

The advanced features give you professional-level control over line art conversion:

- **Quick Adjusters**: One-click line weight modification
- **Edge Detection Controls**: Precise control over photo-to-line conversion
- **Adaptive Threshold Controls**: Perfect tuning for hand-drawn art
- **Line Smoothing**: Professional finish for any style

Start with presets, use quick adjusters for common needs, and dive into advanced settings for perfect results!

---

**Version**: 2.0  
**Date**: 2026-02-15  
**Features Added**: 8 advanced parameters, 2 quick adjusters, collapsible UI section

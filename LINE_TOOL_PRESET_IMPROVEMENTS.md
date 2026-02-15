# Line Tool Preset Improvements

## Overview
This document describes the improvements made to the Line Art Converter presets to make them more accurate for their intended artistic purposes.

## Summary of Changes

### Improved Existing Presets (11 presets)

Each preset has been carefully tuned with optimized parameters for better accuracy:

#### 1. ⭐ Clean Ink Lines
**Purpose**: Professional crisp black ink lines for general use
**Improvements**:
- Threshold: 128 → 135 (better line detection)
- Contrast: 1.5 → 1.6 (crisper lines)
- Sharpen: 1.2 → 1.3 (sharper edges)
- Morphology: none → close (closes small gaps)
- Midtone threshold: 200 → 210 (cleaner whites)

#### 2. ✏️ Pencil Sketch
**Purpose**: Soft graphite pencil appearance with tonal gradation
**Improvements**:
- Threshold: 128 → 140 (lighter strokes)
- Contrast: 1.2 → 1.1 (softer appearance)
- Denoise size: 2 → 1 (preserves texture)

#### 3. 🖊️ Bold Outlines
**Purpose**: Thick outlines for stickers and cartoon style
**Improvements**:
- Threshold: 140 → 145 (cleaner selection)
- Contrast: 2.0 → 2.2 (stronger lines)
- Sharpen: 1.5 → 1.6 (crisper edges)
- Morphology iterations: 2 → 3 (thicker lines)
- Kernel: 3 → 5 (larger dilation)
- Denoise size: 3 → 4 (cleaner result)

#### 4. 🔍 Fine Detail Lines
**Purpose**: Preserve intricate details with thin lines
**Improvements**:
- Threshold: 128 → 125 (captures more detail)
- Contrast: 1.8 → 1.9 (better edge definition)
- Sharpen: 2.0 → 2.2 (maximum detail preservation)
- Midtone threshold: 220 → 230 (preserves highlights)

#### 5. 💥 Comic Book Inks
**Purpose**: High-contrast professional comic book style
**Improvements**:
- Threshold: 120 → 115 (darker, bolder inks)
- Contrast: 2.5 → 2.7 (professional contrast)
- Sharpen: 1.8 → 2.0 (sharp ink edges)
- Morphology iterations: 1 → 2 (better line definition)

#### 6. 📖 Manga Lines
**Purpose**: Clean adaptive lines for manga/anime style
**Improvements**:
- Threshold: 128 → 130 (cleaner lines)
- Contrast: 1.6 → 1.7 (better definition)
- Sharpen: 1.4 → 1.5 (crisper manga lines)
- Morphology: none → close (closes gaps)
- Midtone threshold: 210 → 215 (whiter backgrounds)

#### 7. 🖍️ Coloring Book
**Purpose**: Thick outlines with no inner detail for coloring
**Improvements**:
- Contrast: 1.4 → 1.5 (better outlines)
- Morphology iterations: 3 → 4 (thicker outlines)
- Kernel: 5 → 7 (much thicker lines)
- Denoise size: 4 → 5 (cleaner areas to color)

#### 8. 📐 Blueprint / Technical
**Purpose**: Precise edge detection for technical drawings
**Improvements**:
- Contrast: 1.0 → 1.2 (better visibility)
- Sharpen: 1.5 → 1.8 (precise edges)
- Denoise size: 2 → 1 (minimal noise removal)

#### 9. ✂️ Stencil / Vinyl Cut
**Purpose**: Clean 1-bit shapes for cutting
**Improvements**:
- Contrast: 2.0 → 2.3 (cleaner shapes)
- Morphology iterations: 2 → 3 (closed gaps)
- Denoise size: 5 → 6 (cleaner cutting paths)

#### 10. 🪵 Woodcut / Linocut
**Purpose**: Bold carved appearance
**Improvements**:
- Threshold: 100 → 95 (bolder shapes)
- Contrast: 2.8 → 3.0 (maximum boldness)
- Morphology iterations: 2 → 3 (more closed shapes)
- Denoise size: 6 → 7 (cleaner carved look)

#### 11. 🖋️ Tattoo Stencil
**Purpose**: Smooth outlines for tattoo transfer
**Improvements**:
- Threshold: 135 → 132 (better line capture)
- Contrast: 2.2 → 2.4 (stronger transfer)
- Sharpen: 1.6 → 1.7 (precise lines)
- Denoise size: 3 → 4 (smoother result)

### New Specialized Presets (8 presets)

#### 12. 🎨 Watercolor Lines
**Purpose**: Soft flowing lines that complement watercolor paintings
**Settings**:
- Mode: sketch
- Threshold: 150 (very light)
- Contrast: 1.0 (natural)
- No sharpening or midtone removal
- Preserves soft edges

#### 13. ✍️ Handdrawn / Natural
**Purpose**: Organic hand-drawn appearance with slight imperfections
**Settings**:
- Mode: adaptive
- Contrast: 1.3 (subtle)
- No sharpening
- No denoising (preserves natural texture)
- No midtone removal (keeps tonal variation)

#### 14. 🏛️ Engraving / Crosshatch
**Purpose**: Fine parallel lines like traditional engravings
**Settings**:
- Mode: edge_detect
- Heavy sharpening (2.5)
- No midtone removal (preserves shading)
- Minimal denoising (preserves line detail)

#### 15. 🎭 Screen Print / Posterize
**Purpose**: Bold flat shapes for screen printing
**Settings**:
- Mode: threshold
- Low threshold (110)
- Very high contrast (2.8)
- Heavy morphology (close, 4 iterations)
- Large kernel (7)
- Maximum denoising (8)

#### 16. 📸 Photo to Sketch
**Purpose**: Convert photos to realistic pencil sketches
**Settings**:
- Mode: sketch
- Auto threshold enabled
- Subtle contrast (1.25)
- No sharpening
- No midtone removal (preserves tones)

#### 17. 🖼️ Art Nouveau Lines
**Purpose**: Flowing decorative Art Nouveau style
**Settings**:
- Mode: adaptive
- Threshold: 135
- Moderate contrast (1.5)
- Moderate sharpening (1.4)
- Clean midtones

#### 18. ⚫ High Contrast B&W
**Purpose**: Maximum contrast with no grays
**Settings**:
- Mode: stencil_1bit
- Very high contrast (3.5)
- Sharp edges (1.5)
- Pure black and white output

#### 19. 🔥 Graffiti / Street Art
**Purpose**: Bold urban style with thick outlines
**Settings**:
- Mode: pure_black
- High contrast (2.5)
- Heavy sharpening (1.8)
- Strong dilation (4 iterations)
- Large kernel (7)
- Heavy denoising (5)

## Technical Improvements

### Parameter Optimization Strategy

1. **Threshold Values**: Adjusted based on line darkness
   - Lighter lines: higher threshold (135-150)
   - Darker lines: lower threshold (95-120)

2. **Contrast Boost**: Tuned for style intensity
   - Subtle: 1.0-1.5
   - Moderate: 1.6-2.2
   - Strong: 2.3-3.0

3. **Sharpening**: Based on detail preservation needs
   - None: soft styles (pencil, watercolor)
   - Moderate (1.2-1.7): general use
   - Heavy (1.8-2.5): fine details, engravings

4. **Morphology Operations**:
   - none: preserve original line width
   - erode: thin lines (fine details)
   - dilate: thicken lines (bold, graffiti)
   - close: close gaps (inks, comics, tattoos)

5. **Kernel Size**: Based on line thickness needs
   - 3: standard lines
   - 5: moderately thick
   - 7: thick outlines (coloring book, graffiti)

6. **Denoising**: Based on cleanliness needs
   - 1-2: preserve texture
   - 3-4: balanced cleaning
   - 5-8: maximum cleanliness (stencils, prints)

## Usage Guidelines

### Choosing the Right Preset

**For Illustrations & Art**:
- General purpose → Clean Ink Lines
- Soft/sketchy → Pencil Sketch or Watercolor Lines
- Bold cartoons → Bold Outlines or Graffiti
- Detailed work → Fine Detail Lines

**For Comics & Manga**:
- Western comics → Comic Book Inks
- Manga/anime → Manga Lines
- Heavy inks → Bold Outlines

**For Specific Purposes**:
- Coloring → Coloring Book
- Technical drawings → Blueprint / Technical
- Cutting (vinyl/stencil) → Stencil / Vinyl Cut
- Tattoos → Tattoo Stencil
- Screen printing → Screen Print / Posterize

**For Artistic Styles**:
- Traditional print → Woodcut / Linocut or Engraving
- Art movements → Art Nouveau Lines
- Photo conversion → Photo to Sketch
- Natural/organic → Handdrawn / Natural
- Maximum contrast → High Contrast B&W

## Testing & Validation

All presets have been:
- ✅ Validated for parameter correctness
- ✅ Tested with representative images
- ✅ Tuned for their specific purpose
- ✅ Documented with clear descriptions

## Future Enhancements

Potential future improvements:
- Add interactive parameter previews
- Enable preset customization
- Add preset import/export
- Create preset categories
- Add more artistic style presets

---

**Version**: 1.1  
**Date**: 2026-02-15  
**Author**: GitHub Copilot

# Texture Sorting and AI Configuration Guide

This document explains the improvements made to the PS2 Texture Sorter to address the following issues:
- Sorting method selection not working correctly
- Missing AI model configuration settings
- AI not recognizing images properly
- Non-customizable hotkeys

## Sorting Methods

The PS2 Texture Sorter now properly implements three sorting modes:

### 1. Automatic Mode (Default)
- **How it works**: The AI automatically classifies textures based on image content and filenames
- **Best for**: Large batches where you trust the AI to make decisions
- **User interaction**: None - fully automated
- **Speed**: Fastest mode

### 2. Manual Mode
- **How it works**: You manually select the category for each texture
- **The AI shows suggestions**: The AI analyzes each image and displays its recommended category and confidence level
- **Best for**: Small batches where you want complete control
- **User interaction**: You review and select the category for each file
- **Speed**: Slowest mode (interactive)

### 3. Suggested Mode
- **How it works**: AI suggests a category, and you confirm or change it
- **Best for**: When you want AI assistance but want to verify each classification
- **User interaction**: Quick accept or modify AI suggestions
- **Speed**: Medium (interactive but faster than manual)

## AI Model Configuration

The application now supports comprehensive AI configuration through the Settings window.

### Image Content vs Filename Priority

**New Setting**: "Prioritize image content over filename patterns"
- **Enabled (recommended)**: AI analyzes what's actually IN the image
- **Disabled**: AI relies primarily on filename patterns

This addresses the issue where textures were being classified by name instead of content.

### Offline AI Model Settings

The offline AI model runs locally on your CPU using ONNX:

**Available Settings**:
- **Enable/Disable**: Turn offline AI on or off
- **CPU Threads**: Number of CPU threads to use (default: 4)
- **Confidence Weight**: How much to trust this model (0.0-1.0, default: 0.7)
- **Use for Image Analysis**: Enable AI-powered image content recognition
- **Model Path**: Path to custom ONNX model (leave empty for default)

**Benefits**:
- Works completely offline
- No API costs
- Fast processing
- Privacy-friendly

### Online AI Model Settings

The online AI model connects to external APIs for more powerful classification:

**Available Settings**:
- **Enable/Disable**: Turn online AI on or off
- **API Key**: Your API key for the service
- **API URL**: API endpoint (default: OpenAI)
- **Model**: Model name to use (default: clip-vit-base-patch32)
- **Timeout**: Request timeout in seconds (default: 30)
- **Rate Limits**: 
  - Per Minute (default: 60)
  - Per Hour (default: 1000)
- **Confidence Weight**: How much to trust this model (0.0-1.0, default: 0.8)
- **Use for Difficult Images**: Automatically use online AI when offline has low confidence
- **Low Confidence Threshold**: Threshold to trigger online fallback (default: 0.5)

**Benefits**:
- More accurate classification
- Better with complex/unusual textures
- Fallback for difficult cases

**Requirements**:
- Internet connection
- API key from supported service
- May incur API costs

### AI Blending Modes

When both offline and online AI are enabled, you can choose how to combine their predictions:

- **confidence_weighted** (recommended): Blend based on each model's confidence
- **max**: Use the prediction with highest confidence
- **average**: Average the predictions
- **offline_only**: Only use offline model
- **online_only**: Only use online model

**Minimum Confidence**: Set the minimum confidence threshold (0.0-1.0, default: 0.3)
- Predictions below this threshold are marked as "unclassified"

## Hotkey Customization

Hotkeys are now fully customizable through the Settings window.

### Accessing Hotkey Settings

1. Open Settings (Ctrl+,)
2. Scroll to "Hotkey Configuration" section
3. Click "⌨️ Customize Hotkeys"

### Hotkey Categories

Hotkeys are organized into categories:
- **File**: Open, save, export, close
- **Processing**: Start, pause, stop, resume
- **View**: Toggle panels, refresh, fullscreen
- **Navigation**: Move between textures
- **Selection**: Select all, deselect, invert
- **Tools**: Search, filter, settings, statistics
- **Special**: Achievements, sound toggle, panda mode
- **Global**: Hotkeys that work when app is not focused

### Global Hotkeys

Enable "global hotkeys" in settings to use shortcuts even when the application is not focused:
- **Ctrl+Alt+P**: Global start processing
- **Ctrl+Alt+Space**: Global pause

**Note**: Global hotkeys require the `pynput` library and appropriate system permissions.

## Configuration File Location

All settings are automatically saved to:
```
%USERPROFILE%\.ps2_texture_sorter\config.json
```

You can manually edit this file if needed, but use the Settings UI for safety.

## Troubleshooting

### AI Classification Not Working
1. Check that "Enable offline AI model" is checked in Settings
2. Verify "Prioritize image content over filename patterns" is enabled
3. Check the log for error messages about model loading

### Offline Model Not Found
- The app looks for models in:
  - `src/ai/models/texture_classifier.onnx`
  - `%USERPROFILE%\.ps2_texture_sorter\models\texture_classifier.onnx`
  - `models/texture_classifier.onnx`
- If no model is found, the app falls back to rule-based classification

### Online API Errors
1. Verify your API key is correct
2. Check your internet connection
3. Verify you haven't exceeded rate limits
4. Check API URL is correct

### Manual/Suggested Mode Dialogs Not Appearing
- Ensure you're not running too many files (these modes are interactive)
- Check logs for timeout or error messages
- Try with a smaller batch first

## Best Practices

1. **Start with Automatic Mode** for large batches
2. **Use Suggested Mode** when learning what the AI can do
3. **Use Manual Mode** for critical/important textures
4. **Enable Image Content Priority** for best accuracy
5. **Use Online AI as Fallback** - enable "use for difficult images"
6. **Adjust Confidence Thresholds** based on your needs:
   - Higher = more conservative (more "unclassified")
   - Lower = more aggressive (may have errors)

## Performance Tips

### For Fast Processing
- Use Automatic mode
- Disable online AI
- Increase CPU threads (offline AI)
- Lower confidence threshold

### For Best Accuracy
- Use Suggested mode
- Enable both offline and online AI
- Use "confidence_weighted" blend mode
- Set confidence threshold higher (0.5-0.7)

### For Privacy
- Disable online AI
- Enable offline AI only
- All processing stays on your machine

## Summary of Fixes

✅ **Sorting modes now work correctly**
- Automatic: Fully automated AI classification
- Manual: User selects with AI suggestions
- Suggested: AI suggests, user confirms

✅ **AI focuses on image content**
- New "prefer image content" setting
- Analyzes actual image data, not just filenames
- Improved texture recognition

✅ **Comprehensive AI settings**
- Offline AI: CPU threads, confidence, model path
- Online AI: API key, URL, model, rate limits
- Blending: Multiple modes for combining predictions

✅ **Customizable hotkeys**
- All shortcuts can be rebound
- Organized by category
- Conflict detection
- Global hotkeys supported

✅ **Better configuration**
- All settings in one place
- Real-time preview of changes
- Save/load configuration
- Reset to defaults option

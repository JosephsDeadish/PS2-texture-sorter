# PyTorch/CUDA DLL Fix Documentation

## Problem

When bundling the application with PyInstaller, users encountered the following error:

```
OSError: [WinError 1114] A dynamic link library (DLL) initialization routine failed. 
Error loading "C:\Users\...\torch\lib\c10.dll" or one of its dependencies.
```

This occurred because PyTorch's CUDA libraries have complex dependencies that PyInstaller doesn't handle automatically, and the bundled executable was missing critical CUDA runtime DLLs.

## Solution

This fix implements a comprehensive solution with multiple layers of protection:

### 1. Build-Time Hook (hook-torch.py)

A PyInstaller hook that:
- Detects torch installation without importing it (avoids DLL errors during build)
- **Excludes CUDA DLLs by default** (CPU-only build)
- Optionally includes CUDA DLLs when `TORCH_INCLUDE_CUDA=1` environment variable is set
- Collects all necessary torch C++ libraries and dependencies
- Works even when torch is not installed (graceful degradation)

### 2. Runtime Hook (runtime-hook-torch.py)

A runtime hook that runs before the application starts and:
- Monkey-patches `torch.cuda.is_available()` to catch DLL initialization errors
- Prevents application crash when CUDA runtime is missing
- Allows app to continue in CPU-only mode when GPU support fails

### 3. Comprehensive Error Handling

All code that imports torch now handles three error types:
- `ImportError`: When PyTorch is not installed
- `OSError`: When DLL initialization fails (missing CUDA runtime)
- `RuntimeError`: When CUDA runtime errors occur at runtime

### 4. Build Script Options

The `build.ps1` script now supports:

```powershell
# Standard CPU-only build (recommended for most users)
.\build.ps1

# GPU-enabled build with CUDA support (larger, requires CUDA runtime on target system)
.\build.ps1 -IncludeCuda

# Minimal build without PyTorch (saves ~1GB, disables AI models)
.\build.ps1 -ExcludeTorch
```

## Build Types

### CPU-Only Build (Default, Recommended)

```powershell
.\build.ps1
```

**Characteristics:**
- ✅ CUDA DLLs excluded (smaller size)
- ✅ Works on all Windows systems
- ✅ AI models run on CPU
- ✅ No GPU required
- ✅ Size: ~200-300MB smaller than GPU build

**Use when:**
- Distributing to users who may not have NVIDIA GPUs
- Want smaller download size
- CPU performance is acceptable

### GPU-Enabled Build

```powershell
.\build.ps1 -IncludeCuda
```

**Characteristics:**
- ✅ CUDA DLLs included
- ✅ GPU acceleration available
- ⚠️ Larger build size (~1-2GB)
- ⚠️ Requires CUDA runtime on target system
- ⚠️ Only works on systems with NVIDIA GPUs

**Use when:**
- Target systems have NVIDIA GPUs
- Need maximum AI model performance
- Size is not a concern

### Minimal Build

```powershell
.\build.ps1 -ExcludeTorch
```

**Characteristics:**
- ✅ PyTorch completely excluded
- ✅ Smallest build size (~1GB smaller)
- ⚠️ AI models (CLIP, ViT, etc.) not available
- ✅ Basic texture sorting still works

**Use when:**
- Want minimal download size
- Don't need AI-powered features
- Only need basic texture sorting

## Technical Details

### Why CPU-Only by Default?

1. **Compatibility**: Works on all Windows systems, not just those with NVIDIA GPUs
2. **Size**: CUDA DLLs add 500MB-1GB to the build
3. **Dependencies**: CUDA requires specific runtime libraries on target system
4. **Error-prone**: Missing CUDA dependencies cause cryptic DLL errors

### How It Works

1. **Build Phase** (hook-torch.py):
   - Detects torch package location without importing
   - Scans for DLL files in torch/lib directory
   - Filters out CUDA DLLs based on filename patterns
   - Collects remaining CPU-only DLLs
   - Respects TORCH_INCLUDE_CUDA environment variable

2. **Runtime Phase** (runtime-hook-torch.py):
   - Runs before application code
   - Wraps torch.cuda.is_available() in try-except
   - Catches OSError/RuntimeError from missing CUDA
   - Returns False instead of crashing
   - Allows app to continue in CPU mode

3. **Application Code**:
   - All torch imports wrapped in try-except
   - Catches ImportError, OSError, RuntimeError
   - Logs errors for debugging
   - Provides fallback behavior
   - User-friendly error messages

### Environment Variables

- `TORCH_INCLUDE_CUDA=1`: Include CUDA DLLs in build (set by `build.ps1 -IncludeCuda`)
- `TORCH_INCLUDE_CUDA=0`: Exclude CUDA DLLs (default)

## Testing

### Test Import Handling

```python
# This should not crash even without torch installed
python -c "
import sys
sys.path.insert(0, 'src')
from utils.gpu_detector import GPUDetector
detector = GPUDetector()
devices = detector.detect_gpus()
print(f'Found {len(devices)} device(s)')
"
```

### Test Build

```powershell
# Build and test
.\build.ps1
cd dist\GameTextureSorter
.\GameTextureSorter.exe
```

The application should:
- ✅ Start without errors
- ✅ Run even without NVIDIA GPU
- ✅ Detect available hardware correctly
- ✅ Disable GPU features gracefully if not available

## Troubleshooting

### Build Fails with "torch not found"

This is expected if torch is not installed. The hook handles this gracefully. The application will build without torch support.

### Application Crashes with DLL Error

If you still get DLL errors after this fix:

1. **Check build flags**: Make sure you're using CPU-only build (default)
2. **Verify hook is loaded**: Look for `[torch hook]` messages during build
3. **Check runtime hook**: Verify `runtime-hook-torch.py` is in runtime_hooks list
4. **Try minimal build**: Use `build.ps1 -ExcludeTorch` to exclude torch entirely

### GPU Not Detected

This is expected behavior if:
- Using CPU-only build (default)
- NVIDIA drivers not installed
- No NVIDIA GPU in system

The application will work fine in CPU-only mode.

## Migration Guide

### For Users with Existing Builds

If you have an existing build that crashes with DLL errors:

1. Pull the latest changes
2. Rebuild with `.\build.ps1`
3. Application will now work on all systems

### For Developers

When adding code that uses torch:

```python
# ✅ Good - Handles all error types
try:
    import torch
except ImportError as e:
    logger.warning(f"PyTorch not available: {e}")
    TORCH_AVAILABLE = False
except OSError as e:
    logger.warning(f"PyTorch DLL initialization failed: {e}")
    TORCH_AVAILABLE = False
except Exception as e:
    logger.warning(f"Unexpected error loading PyTorch: {e}")
    TORCH_AVAILABLE = False
else:
    TORCH_AVAILABLE = True

# When checking CUDA availability
if TORCH_AVAILABLE:
    try:
        has_cuda = torch.cuda.is_available()
    except (RuntimeError, OSError):
        has_cuda = False
```

## References

- **Problem Statement**: See issue description for original error message
- **hook-torch.py**: Build-time PyInstaller hook
- **runtime-hook-torch.py**: Runtime CUDA error handler
- **build.ps1**: Build script with torch options
- **src/utils/gpu_detector.py**: GPU detection with fallback
- **src/vision_models/**: Vision models with error handling

"""PyInstaller hook for Real-ESRGAN upscaling

This hook ensures that realesrgan and all its dependencies are properly collected
when building with PyInstaller. This is required for AI-powered texture upscaling.
"""

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all realesrgan submodules (architectures, utilities, etc.)
hiddenimports = collect_submodules('realesrgan')

# Collect data files (model weights, architectures, configs)
datas = collect_data_files('realesrgan', includes=['**/*.py', '**/*.pth', '**/*.yml', '**/*.yaml'])

print(f"[realesrgan hook] Collected {len(hiddenimports)} hidden imports and {len(datas)} data files")

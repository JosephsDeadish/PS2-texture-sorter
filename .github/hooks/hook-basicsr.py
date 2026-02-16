"""PyInstaller hook for basicsr (Basic Super-Resolution Restoration)

This hook ensures that basicsr and all its dependencies are properly collected
when building with PyInstaller. This is required for Real-ESRGAN upscaling support.
"""

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all basicsr submodules (architectures, models, utilities, etc.)
hiddenimports = collect_submodules('basicsr')

# Collect data files (model architectures, configs, pretrained weights)
datas = collect_data_files('basicsr', includes=['**/*.py', '**/*.pth', '**/*.yml', '**/*.yaml'])

print(f"[basicsr hook] Collected {len(hiddenimports)} hidden imports and {len(datas)} data files")

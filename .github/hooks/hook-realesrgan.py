"""PyInstaller hook for Real-ESRGAN"""
from PyInstaller.utils.hooks import collect_data_files

# DON'T introspect - force include known modules
hiddenimports = [
    'realesrgan',
    'realesrgan.archs',
    'realesrgan.archs.rrdbnet_arch',
    'realesrgan.data',
]

try:
    datas = collect_data_files('realesrgan', includes=['archs', 'data', 'weights'])
except Exception as e:
    print(f"[realesrgan hook] Warning: Could not collect data files: {e}")
    datas = []

print(f"[realesrgan hook] Forced inclusion of {len(hiddenimports)} modules")
print(f"[realesrgan hook] Collected {len(datas)} data files")

"""PyInstaller hook for basicsr (Basic Super-Resolution)"""
from PyInstaller.utils.hooks import collect_data_files

# DON'T try to introspect basicsr - causes version conflicts
# Instead, force-include the modules we know are needed

hiddenimports = [
    'basicsr',
    'basicsr.archs',
    'basicsr.archs.rrdbnet_arch',
    'basicsr.data',
    'basicsr.metrics',
    'basicsr.losses',
    'basicsr.models',
]

# Try to collect data files, but don't fail if unable
try:
    datas = collect_data_files('basicsr', includes=['archs', 'metrics', 'losses'])
except Exception as e:
    print(f"[basicsr hook] Warning: Could not collect data files: {e}")
    datas = []

print(f"[basicsr hook] Forced inclusion of {len(hiddenimports)} modules")
print(f"[basicsr hook] Collected {len(datas)} data files")

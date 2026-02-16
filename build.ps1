#!/usr/bin/env pwsh
################################################################################
# Game Texture Sorter - Automated Windows Build Script (PowerShell)
# Author: Dead On The Inside / JosephsDeadish
#
# This PowerShell script automatically builds the application in ONE-FOLDER mode.
# It provides better error handling and progress reporting than the batch file.
#
# Usage:
#   .\build.ps1                   - Build one-folder with external assets
#   .\build.ps1 -IncludeCuda      - Build with CUDA support (larger, GPU-enabled)
#   .\build.ps1 -ExcludeTorch     - Build without PyTorch (smaller, basic features only)
#
# The one-folder build provides:
#   - Much faster startup (1-3 seconds vs 10-30 seconds)
#   - Better performance overall
#   - Easy asset customization (themes, sounds, icons)
#   - Local storage for config, cache, and database
#
# Build Options:
#   -IncludeCuda    : Include CUDA DLLs for GPU acceleration (default: excluded)
#   -ExcludeTorch   : Exclude PyTorch entirely (saves ~1GB, disables AI models)
################################################################################

param(
    [switch]$IncludeCuda = $false,
    [switch]$ExcludeTorch = $false
)

$ErrorActionPreference = "Stop"

# One-folder mode is now the only build mode
$BuildMode = "folder"

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  Game Texture Sorter - Automated Build Script (PowerShell)" -ForegroundColor Cyan
Write-Host "  Author: Dead On The Inside / JosephsDeadish" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Build mode: ONE-FOLDER (with external assets)" -ForegroundColor White

# Display build options
if ($IncludeCuda) {
    Write-Host "CUDA Support: ENABLED (GPU acceleration, larger build)" -ForegroundColor Yellow
    $env:TORCH_INCLUDE_CUDA = "1"
} else {
    Write-Host "CUDA Support: DISABLED (CPU-only, smaller build)" -ForegroundColor Green
    $env:TORCH_INCLUDE_CUDA = "0"
}

if ($ExcludeTorch) {
    Write-Host "PyTorch: EXCLUDED (minimal build, ~1GB smaller)" -ForegroundColor Yellow
    Write-Host "  Note: AI models (CLIP, ViT, etc.) will be unavailable" -ForegroundColor Gray
} else {
    Write-Host "PyTorch: INCLUDED (full AI features)" -ForegroundColor Green
}

Write-Host ""

# Check Python installation
Write-Host "[1/7] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Create virtual environment
Write-Host "[2/7] Setting up virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "[3/7] Activating virtual environment..." -ForegroundColor Yellow
$activateScript = "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ ERROR: Activation script not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Upgrade pip
Write-Host "[4/7] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "[5/7] Installing dependencies..." -ForegroundColor Yellow

if ($ExcludeTorch) {
    # Install minimal requirements without PyTorch
    Write-Host "Installing minimal requirements (no PyTorch)..." -ForegroundColor Gray
    
    # Check if requirements-minimal.txt exists
    if (Test-Path "requirements-minimal.txt") {
        pip install -r requirements-minimal.txt
    } else {
        # If minimal requirements doesn't exist, install full and user can uninstall torch later
        Write-Host "⚠ requirements-minimal.txt not found, installing full requirements" -ForegroundColor Yellow
        pip install -r requirements.txt
    }
} else {
    # Install full requirements including PyTorch
    pip install -r requirements.txt
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Verify PyYAML is installed in this environment
Write-Host "[6/7] Verifying PyYAML is installed..." -ForegroundColor Yellow
try {
    $yamlVersion = python -c "import yaml; print(yaml.__version__)" 2>&1
    if ($LASTEXITCODE -ne 0) { throw "PyYAML not found" }
    Write-Host "✓ PyYAML $yamlVersion is available" -ForegroundColor Green
} catch {
    Write-Host "⚠ PyYAML not found. Installing PyYAML..." -ForegroundColor Yellow
    pip install PyYAML
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ ERROR: Failed to install PyYAML" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✓ PyYAML installed successfully" -ForegroundColor Green
}
Write-Host ""

# Clean previous builds
Write-Host "[7/7] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "✓ Removed build directory" -ForegroundColor Gray
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "✓ Removed dist directory" -ForegroundColor Gray
}
Get-ChildItem -Path . -Filter "*.spec" -Exclude "build_spec_onefolder.spec","build_spec_with_svg.spec" | Remove-Item -Force
Write-Host "✓ Cleaned previous builds" -ForegroundColor Green
Write-Host ""

# Create resource directories
Write-Host "Creating resource directories..." -ForegroundColor Yellow
$resourceDirs = @(
    "src\resources\icons",
    "src\resources\cursors",
    "src\resources\themes",
    "src\resources\sounds"
)
foreach ($dir in $resourceDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created $dir" -ForegroundColor Gray
    }
}
Write-Host ""

# Pre-build validation
Write-Host "🔍 Pre-build validation..." -ForegroundColor Yellow
Write-Host "Checking for problematic long paths..." -ForegroundColor Gray

# Check if basicsr is installed
try {
    $basicsr_check = python -c "import basicsr; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ basicsr found" -ForegroundColor Green
    } else {
        Write-Warning "⚠️  basicsr not installed - upscaling will be disabled"
    }
} catch {
    Write-Warning "⚠️  basicsr not installed - upscaling will be disabled"
}

# Check if realesrgan is installed
try {
    $realesrgan_check = python -c "import realesrgan; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ realesrgan found" -ForegroundColor Green
    } else {
        Write-Warning "⚠️  realesrgan not installed - upscaling will be disabled"
    }
} catch {
    Write-Warning "⚠️  realesrgan not installed - upscaling will be disabled"
}

Write-Host ""

# Build with PyInstaller
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  Building One-Folder with PyInstaller..." -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

# Display build configuration
Write-Host "Build Configuration:" -ForegroundColor White
if ($IncludeCuda) {
    Write-Host "  • PyTorch: CPU + CUDA (GPU acceleration enabled)" -ForegroundColor Green
} elseif ($ExcludeTorch) {
    Write-Host "  • PyTorch: Excluded (minimal build)" -ForegroundColor Yellow
} else {
    Write-Host "  • PyTorch: CPU-only (no CUDA)" -ForegroundColor Green
}
Write-Host ""

# Run PyInstaller with one-folder spec file
pyinstaller build_spec_onefolder.spec --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "✗ BUILD FAILED!" -ForegroundColor Red
    Write-Host "Check the error messages above for details." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "  ✓ BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""

# Create the app_data directory structure and show results
$folderPath = "dist\GameTextureSorter"
if (Test-Path $folderPath) {
    Write-Host "Creating app_data directory structure..." -ForegroundColor Yellow
    $appDataDirs = @(
        "$folderPath\app_data",
        "$folderPath\app_data\cache",
        "$folderPath\app_data\logs",
        "$folderPath\app_data\themes",
        "$folderPath\app_data\models"
    )
    foreach ($dir in $appDataDirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "✓ Created $dir" -ForegroundColor Gray
        }
    }
    Write-Host ""
    
    $exePath = "$folderPath\GameTextureSorter.exe"
    if (Test-Path $exePath) {
        $exeSize = (Get-Item $exePath).Length
        $exeSizeMB = [math]::Round($exeSize / 1MB, 2)
        
        Write-Host "The application has been created in the one-folder format:" -ForegroundColor White
        Write-Host "  Location: dist\GameTextureSorter\" -ForegroundColor Cyan
        Write-Host "  Main EXE: GameTextureSorter.exe ($exeSizeMB MB)" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Folder structure:" -ForegroundColor White
        Write-Host "  dist\GameTextureSorter\" -ForegroundColor Gray
        Write-Host "    ├── GameTextureSorter.exe    (Main executable)" -ForegroundColor Gray
        Write-Host "    ├── _internal\               (Python runtime + libraries)" -ForegroundColor Gray
        Write-Host "    ├── resources\               (Icons, sounds, cursors)" -ForegroundColor Gray
        Write-Host "    └── app_data\                (Config, cache, themes, models)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Benefits of one-folder build:" -ForegroundColor Green
        Write-Host "  ✓ Much faster startup (1-3 seconds vs 10-30 seconds)" -ForegroundColor Green
        Write-Host "  ✓ Better performance overall" -ForegroundColor Green
        Write-Host "  ✓ Easier to modify themes and assets" -ForegroundColor Green
        Write-Host "  ✓ Config and cache stored locally" -ForegroundColor Green
        Write-Host ""
        
        # Display build-specific info
        if ($IncludeCuda) {
            Write-Host "GPU Support: ENABLED" -ForegroundColor Green
            Write-Host "  • CUDA runtime libraries included" -ForegroundColor Gray
            Write-Host "  • Hardware acceleration available" -ForegroundColor Gray
        } elseif ($ExcludeTorch) {
            Write-Host "Minimal Build: PyTorch EXCLUDED" -ForegroundColor Yellow
            Write-Host "  • Significantly smaller size (~1GB less)" -ForegroundColor Gray
            Write-Host "  • AI models (CLIP, ViT) not available" -ForegroundColor Gray
            Write-Host "  • Basic sorting features still work" -ForegroundColor Gray
        } else {
            Write-Host "Standard Build: CPU-only PyTorch" -ForegroundColor Green
            Write-Host "  • CUDA DLLs excluded (smaller size)" -ForegroundColor Gray
            Write-Host "  • AI models work on CPU" -ForegroundColor Gray
            Write-Host "  • Suitable for systems without NVIDIA GPU" -ForegroundColor Gray
        }
        Write-Host ""
        
        Write-Host "To distribute: Copy the entire 'GameTextureSorter' folder" -ForegroundColor Yellow
    } else {
        Write-Host "✗ WARNING: EXE file not found in folder" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ WARNING: Folder build not found at expected location" -ForegroundColor Yellow
}

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"

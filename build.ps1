#!/usr/bin/env pwsh
################################################################################
# Game Texture Sorter - Automated Windows Build Script (PowerShell)
# Author: Dead On The Inside / JosephsDeadish
#
# This PowerShell script automatically builds the application.
# It provides better error handling and progress reporting than the batch file.
#
# Usage:
#   .\build.ps1          - Build single-EXE (portable)
#   .\build.ps1 folder   - Build one-folder with external assets (faster startup)
################################################################################

param(
    [Parameter(Position=0)]
    [ValidateSet("single", "folder", "")]
    [string]$BuildMode = "single"
)

# If no parameter or empty, default to single
if ($BuildMode -eq "") {
    $BuildMode = "single"
}

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  Game Texture Sorter - Automated Build Script (PowerShell)" -ForegroundColor Cyan
Write-Host "  Author: Dead On The Inside / JosephsDeadish" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Build mode: $BuildMode" -ForegroundColor White
Write-Host ""

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
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
Write-Host "[2/6] Setting up virtual environment..." -ForegroundColor Yellow
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
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow
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
Write-Host "[4/6] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "[5/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Verify PyYAML is installed in this environment
Write-Host "Verifying PyYAML is installed in the PyInstaller environment..." -ForegroundColor Yellow
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
Write-Host "[6/6] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "✓ Removed build directory" -ForegroundColor Gray
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "✓ Removed dist directory" -ForegroundColor Gray
}
Get-ChildItem -Path . -Filter "*.spec" -Exclude "build_spec.spec" | Remove-Item -Force
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

# Build with PyInstaller
Write-Host "========================================================================" -ForegroundColor Cyan
if ($BuildMode -eq "folder") {
    Write-Host "  Building One-Folder with PyInstaller..." -ForegroundColor Cyan
} else {
    Write-Host "  Building Single EXE with PyInstaller..." -ForegroundColor Cyan
}
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

# Run PyInstaller with appropriate spec file
if ($BuildMode -eq "folder") {
    pyinstaller build_spec_onefolder.spec --clean --noconfirm
} else {
    pyinstaller build_spec.spec --clean --noconfirm
}

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

# Check if build was successful and provide appropriate message
if ($BuildMode -eq "folder") {
    # For folder builds, create the app_data directory structure
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
            Write-Host "  ✓ Much faster startup (no extraction to temp)" -ForegroundColor Green
            Write-Host "  ✓ Better performance overall" -ForegroundColor Green
            Write-Host "  ✓ Easier to modify themes and assets" -ForegroundColor Green
            Write-Host "  ✓ Config and cache stored locally" -ForegroundColor Green
            Write-Host ""
            Write-Host "To distribute: Copy the entire 'GameTextureSorter' folder" -ForegroundColor Yellow
        } else {
            Write-Host "✗ WARNING: EXE file not found in folder" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ WARNING: Folder build not found at expected location" -ForegroundColor Yellow
    }
} else {
    # Single-EXE build
    $exePath = "dist\GameTextureSorter.exe"
    if (Test-Path $exePath) {
        $exeSize = (Get-Item $exePath).Length
        $exeSizeMB = [math]::Round($exeSize / 1MB, 2)
        
        Write-Host "The executable has been created:" -ForegroundColor White
        Write-Host "  Location: $exePath" -ForegroundColor Cyan
        Write-Host "  Size: $exeSizeMB MB" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "You can now:" -ForegroundColor White
        Write-Host "  1. Run the EXE: .\$exePath" -ForegroundColor Gray
        Write-Host "  2. Copy it anywhere (fully portable)" -ForegroundColor Gray
        Write-Host "  3. Sign it with a code certificate (see CODE_SIGNING.md)" -ForegroundColor Gray
        Write-Host "  4. Distribute to users" -ForegroundColor Gray
        Write-Host ""
        Write-Host "The EXE is completely standalone - no installation required! 🐼" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 TIP: For faster startup, use 'build.ps1 folder' to create" -ForegroundColor Yellow
        Write-Host "   a one-folder build with external assets!" -ForegroundColor Yellow
    } else {
        Write-Host "✗ WARNING: EXE file not found at expected location" -ForegroundColor Yellow
    }
}

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"

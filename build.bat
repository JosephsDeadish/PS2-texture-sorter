@echo off
REM ============================================================================
REM Game Texture Sorter - Automated Windows Build Script
REM Author: Dead On The Inside / JosephsDeadish
REM 
REM This script builds the application for Windows in ONE-FOLDER mode ONLY.
REM 
REM Usage:
REM   build.bat              - Build one-folder with external assets
REM 
REM The one-folder build provides:
REM   - Much faster startup (1-3 seconds vs 10-30 seconds)
REM   - Better performance overall
REM   - Easy asset customization (themes, sounds, icons)
REM   - Local storage for config, cache, and database
REM 
REM It will:
REM   1. Check for Python installation
REM   2. Create/activate virtual environment
REM   3. Install dependencies
REM   4. Run PyInstaller to create the build
REM   5. Package the final output
REM ============================================================================

echo.
echo ========================================================================
echo   Game Texture Sorter - Automated Build Script
echo   Author: Dead On The Inside / JosephsDeadish
echo ========================================================================
echo.

REM One-folder mode is now the only build mode
set BUILD_MODE=folder

echo Build mode: ONE-FOLDER (with external assets)
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Python found: 
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo [2/6] Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [5/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully.
echo.

REM Verify PyYAML is installed in this environment
echo Verifying PyYAML is installed in the PyInstaller environment...
python -c "import yaml; print('PyYAML ' + yaml.__version__ + ' is available')"
if errorlevel 1 (
    echo WARNING: PyYAML not found. Installing PyYAML...
    pip install PyYAML
    if errorlevel 1 (
        echo ERROR: Failed to install PyYAML
        pause
        exit /b 1
    )
    echo PyYAML installed successfully.
) else (
    echo PyYAML verified in the PyInstaller environment.
)
echo.

REM Clean previous builds
echo [6/6] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec
echo.

REM Create necessary resource directories if they don't exist
if not exist "src\resources\icons" mkdir src\resources\icons
if not exist "src\resources\cursors" mkdir src\resources\cursors
if not exist "src\resources\themes" mkdir src\resources\themes
if not exist "src\resources\sounds" mkdir src\resources\sounds

REM Create a placeholder icon if it doesn't exist
if not exist "src\resources\icons\panda_icon.ico" (
    echo Creating placeholder icon...
    REM PyInstaller will use default icon if custom one doesn't exist
)

echo ========================================================================
echo   Building with PyInstaller (ONE-FOLDER mode)...
echo ========================================================================
echo.

REM Run PyInstaller with one-folder spec file
pyinstaller build_spec_onefolder.spec --clean --noconfirm
if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above for details.
    pause
    exit /b 1
)

REM Create the app_data directory structure
echo Creating app_data directory structure...
mkdir dist\GameTextureSorter\app_data 2>nul
mkdir dist\GameTextureSorter\app_data\cache 2>nul
mkdir dist\GameTextureSorter\app_data\logs 2>nul
mkdir dist\GameTextureSorter\app_data\themes 2>nul
mkdir dist\GameTextureSorter\app_data\models 2>nul

echo.
echo ========================================================================
echo   BUILD SUCCESSFUL!
echo ========================================================================
echo.

echo The application has been created in the 'dist\GameTextureSorter' folder.
echo.
echo   dist\GameTextureSorter\GameTextureSorter.exe
echo   dist\GameTextureSorter\app_data\     ^(config, cache, database, themes^)
echo   dist\GameTextureSorter\resources\     ^(icons, sounds, cursors^)
echo.
echo Benefits of one-folder build:
echo   - FASTER startup (1-3 seconds vs 10-30 seconds for single-EXE)
echo   - Better overall performance
echo   - Easy customization of themes and assets
echo   - Local config and cache storage
echo.
echo To distribute: Copy the entire 'GameTextureSorter' folder
echo.
echo You can now:
echo   1. Run GameTextureSorter.exe directly from the folder
echo   2. Copy the entire folder to any location (portable)
echo   3. Sign it with a code certificate (see CODE_SIGNING.md)
echo   4. Distribute the folder to users
echo.
echo ========================================================================
echo.

pause

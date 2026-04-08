@echo off
chcp 65001 >nul
echo ========================================
echo QuizMaster Windows Build Script
echo ========================================
echo.

REM Check Python environment
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not detected
    echo.
    echo Please install Python 3.9+:
    echo 1. Visit https://www.python.org/downloads/
    echo 2. Download and install Python 3.9 or higher
    echo 3. Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [Error] Failed to install dependencies
    pause
    exit /b 1
)
echo [Done] Dependencies installed
echo.

echo [2/5] Installing PyInstaller...
pip install pyinstaller >nul 2>&1
echo [Done] PyInstaller installed
echo.

echo [3/5] Cleaning old build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo [Done] Cleaned
echo.

echo [4/5] Building executable...
echo This may take 1-3 minutes...
pyinstaller --clean QuizMaster.spec
if errorlevel 1 (
    echo [Error] Build failed
    pause
    exit /b 1
)
echo [Done] Build completed
echo.

echo [5/5] Checking output...
if exist "dist\QuizMaster.exe" (
    echo [Success] Executable generated
    echo.
    echo Location: dist\QuizMaster.exe
    echo.
    dir "dist\QuizMaster.exe" | find "QuizMaster.exe"
    echo.
    echo ========================================
    echo Build Successful!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Copy QuizMaster.exe from dist folder to distribute
    echo 2. User can double-click to run without Python installed
    echo.
) else (
    echo [Error] Executable not found
)

pause

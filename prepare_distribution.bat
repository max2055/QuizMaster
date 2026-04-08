@echo off
chcp 65001 >nul
echo ========================================
echo QuizMaster Distribution Prep
echo ========================================
echo.

REM Create distribution folder
set DIST_FOLDER=QuizMaster_Distribution

echo [1/3] Creating distribution folder...
if exist "%DIST_FOLDER%" rmdir /s /q "%DIST_FOLDER%"
mkdir "%DIST_FOLDER%"
echo [Done] Created: %DIST_FOLDER%
echo.

echo [2/3] Copying executable...
if exist "dist\QuizMaster.exe" (
    copy "dist\QuizMaster.exe" "%DIST_FOLDER%\" >nul
    echo [Done] Copied QuizMaster.exe
) else (
    echo [Warning] QuizMaster.exe not found. Run package_for_windows.bat first.
)
echo.

echo [3/3] Copying database...
copy "quizmaster.db" "%DIST_FOLDER%\" >nul
echo [Done] Copied quizmaster.db
echo.

echo ========================================
echo Distribution Ready!
echo ========================================
echo.
echo Folder: %DIST_FOLDER%
echo.
echo Next steps:
echo 1. Compress %DIST_FOLDER% to zip
echo 2. Send zip file to user
echo 3. User extracts and double-clicks QuizMaster.exe
echo.

pause

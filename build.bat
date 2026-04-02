@echo off
REM QuizMaster Windows 打包脚本

echo ========================================
echo QuizMaster 打包工具
echo ========================================
echo.

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python 环境，请先安装 Python 3.9+
    pause
    exit /b 1
)

echo [1/4] 检查依赖包...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [错误] 依赖包安装失败
    pause
    exit /b 1
)
echo [完成] 依赖包检查完成
echo.

echo [2/4] 清理旧的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo [完成] 清理完成
echo.

echo [3/4] 开始打包...
pyinstaller --clean QuizMaster.spec
if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)
echo [完成] 打包完成
echo.

echo [4/4] 检查输出文件...
if exist "dist\QuizMaster.exe" (
    echo [成功] 可执行文件已生成：dist\QuizMaster.exe
    echo.
    echo 文件大小:
    dir "dist\QuizMaster.exe" | find "QuizMaster.exe"
) else (
    echo [错误] 未找到生成的可执行文件
)

echo.
echo ========================================
echo 打包完成！
echo 可执行文件位置：dist\QuizMaster.exe
echo ========================================
pause

@echo off
chcp 65001 >nul
echo ========================================
echo QuizMaster Windows 打包工具
echo ========================================
echo.

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python 环境
    echo.
    echo 请先安装 Python 3.9+：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装 Python 3.9 或更高版本
    echo 3. 安装时勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [1/5] 检查依赖包...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [错误] 依赖包安装失败
    pause
    exit /b 1
)
echo [完成] 依赖包安装完成
echo.

echo [2/5] 安装 PyInstaller...
pip install pyinstaller >nul 2>&1
echo [完成] PyInstaller 安装完成
echo.

echo [3/5] 清理旧的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo [完成] 清理完成
echo.

echo [4/5] 开始打包...
echo 这可能需要 1-3 分钟，请耐心等待...
pyinstaller --clean 逢考必过.spec
if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)
echo [完成] 打包完成
echo.

echo [5/5] 检查输出文件...
if exist "dist\QuizMaster.exe" (
    echo [成功] 可执行文件已生成
    echo.
    echo 文件位置：dist\QuizMaster.exe
    echo.
    dir "dist\QuizMaster.exe" | find "QuizMaster.exe"
    echo.
    echo ========================================
    echo 打包成功！
    echo ========================================
    echo.
    echo 下一步操作：
    echo 1. 将 dist 文件夹中的 QuizMaster.exe 复制给用户
    echo 2. 用户双击即可运行，无需安装 Python
    echo.
) else (
    echo [错误] 未找到生成的可执行文件
)

pause

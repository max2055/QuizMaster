@echo off
chcp 65001 >nul
echo ========================================
echo QuizMaster 分发文件准备工具
echo ========================================
echo.

REM 创建分发文件夹
set DIST_FOLDER=QuizMaster_分发版

echo [1/4] 创建分发文件夹...
if exist "%DIST_FOLDER%" rmdir /s /q "%DIST_FOLDER%"
mkdir "%DIST_FOLDER%"
echo [完成] 创建文件夹：%DIST_FOLDER%
echo.

echo [2/4] 复制可执行文件...
if exist "dist\QuizMaster.exe" (
    copy "dist\QuizMaster.exe" "%DIST_FOLDER%\" >nul
    echo [完成] 已复制 QuizMaster.exe
) else (
    echo [警告] 未找到 QuizMaster.exe，请先运行 package_for_windows.bat 打包
)
echo.

echo [3/4] 复制数据库文件...
copy "quizmaster.db" "%DIST_FOLDER%\" >nul
echo [完成] 已复制 quizmaster.db
echo.

echo [4/4] 复制用户说明...
copy "README_用户说明.txt" "%DIST_FOLDER%\" >nul
echo [完成] 已复制 README_用户说明.txt
echo.

echo ========================================
echo 分发文件准备完成！
echo ========================================
echo.
echo 文件夹位置：%DIST_FOLDER%
echo.
echo 下一步操作：
echo 1. 压缩 %DIST_FOLDER% 文件夹成 zip
echo 2. 将 zip 文件发送给用户
echo 3. 用户解压后双击 QuizMaster.exe 即可运行
echo.

pause

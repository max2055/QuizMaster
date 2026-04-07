#!/bin/bash
# QuizMaster macOS/Linux 打包脚本

echo "========================================"
echo "QuizMaster 打包工具"
echo "========================================"
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3 环境"
    exit 1
fi

echo "[1/4] 检查依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 依赖包安装失败"
    exit 1
fi
echo "[完成] 依赖包检查完成"
echo ""

echo "[2/4] 清理旧的构建文件..."
rm -rf build dist
echo "[完成] 清理完成"
echo ""

echo "[3/4] 开始打包..."
pyinstaller --clean 逢考必过.spec
if [ $? -ne 0 ]; then
    echo "[错误] 打包失败"
    exit 1
fi
echo "[完成] 打包完成"
echo ""

echo "[4/4] 检查输出文件..."
if [ -f "dist/QuizMaster" ]; then
    echo "[成功] 可执行文件已生成：dist/QuizMaster"
    echo ""
    echo "文件大小:"
    ls -lh dist/QuizMaster
else
    echo "[错误] 未找到生成的可执行文件"
fi

echo ""
echo "========================================"
echo "打包完成！"
echo "可执行文件位置：dist/QuizMaster"
echo "========================================"

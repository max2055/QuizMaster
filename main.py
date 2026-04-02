"""
QuizMaster - 刷题工具
主程序入口
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor


def main():
    """主函数"""
    # 添加 PyQt6 插件路径（修复 Anaconda Python 下 cocoa 插件加载问题）
    try:
        import PyQt6
        pyqt6_path = os.path.dirname(PyQt6.__file__)
        qt6_path = os.path.join(pyqt6_path, 'Qt6')
        plugins_path = os.path.join(qt6_path, 'plugins')
        if os.path.exists(plugins_path):
            # 在创建 QApplication 之前添加库路径
            from PyQt6.QtCore import QCoreApplication
            QCoreApplication.addLibraryPath(plugins_path)
    except Exception:
        pass  # 如果失败，使用默认路径

    # 启用高 DPI 支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # macOS 强制使用浅色外观（修复标题栏深色问题）
    if sys.platform == 'darwin':
        os.environ['QT_MAC_FORCE_LIGHT_MODE'] = '1'
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("QuizMaster")
    app.setApplicationVersion("1.5.0")
    app.setOrganizationName("QuizMaster - 逢考必过")

    # 加载全局样式表
    from pathlib import Path
    style_path = Path(__file__).parent / "ui" / "stylesheet.qss"
    try:
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass  # 如果不存在，使用默认样式

    # macOS 强制浅色模式
    if sys.platform == 'darwin':
        # 设置浅色调色板 - 使用 Google Material Design 配色
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(248, 249, 250))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(60, 64, 67))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(241, 243, 244))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(60, 64, 67))
        palette.setColor(QPalette.ColorRole.Text, QColor(60, 64, 67))
        palette.setColor(QPalette.ColorRole.Button, QColor(248, 249, 250))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(60, 64, 67))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Link, QColor(26, 115, 232))  # Google Blue
        palette.setColor(QPalette.ColorRole.Highlight, QColor(26, 115, 232))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        app.setPalette(palette)
    
    # 设置全局字体（跨平台兼容）
    if sys.platform == 'win32':
        font = QFont("Microsoft YaHei", 10)
    elif sys.platform == 'darwin':
        font = QFont("PingFang SC", 10)
    else:
        font = QFont("Noto Sans CJK SC", 10)
    app.setFont(font)
    
    # 创建主窗口
    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

"""
主窗口 - 应用主界面
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QTabWidget, QPushButton,
    QLabel, QToolBar, QStatusBar, QMenuBar, QMenu,
    QFileDialog, QMessageBox, QFrame, QLineEdit, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QAction

from database.db_manager import DatabaseManager
from services.question_service import QuestionService
from services.practice_service import PracticeService
from services.import_service import ImportService

from ui.question_widget import QuestionWidget
from ui.stats_widget import StatsWidget
from ui.dialogs import QuestionDialog, ImportDialog, CategoryDialog


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化数据库和服务
        self.db = DatabaseManager()
        self.question_service = QuestionService(self.db)
        self.practice_service = PracticeService(self.db)
        self.import_service = ImportService()
        
        # 当前选中的分类
        self.current_category_id = None
        
        # 初始化 UI
        self._init_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        
        # 加载分类树
        self._load_categories()
        
        # 应用样式
        self._apply_styles()
    
    def _init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("QuizMaster - 逢考必过")
        self.setMinimumSize(900, 650)
        self.resize(1200, 800)

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # 左侧：分类树
        left_widget = QWidget()
        left_widget.setMinimumWidth(180)
        left_widget.setMaximumWidth(220)
        left_widget.setStyleSheet("""
            QWidget {
                background-color: #FAFBFC;
                border-right: 1px solid #E8EAED;
            }
        """)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(6, 6, 6, 6)
        left_layout.setSpacing(4)

        # 分类树标题和按钮行
        title_row = QHBoxLayout()
        title_row.setSpacing(6)
        title_row.setContentsMargins(0, 0, 0, 4)

        cat_label = QLabel("📚 题库")
        cat_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        cat_label.setStyleSheet("color: #3C4043; padding: 4px 0;")
        title_row.addWidget(cat_label)

        # 图标按钮 - 与顶部工具栏风格一致
        add_btn_row = QHBoxLayout()
        add_btn_row.setSpacing(6)
        add_btn_row.setContentsMargins(0, 0, 0, 0)

        self.add_category_btn = QPushButton("+")
        self.add_category_btn.setMinimumSize(48, 48)
        self.add_category_btn.setMaximumSize(48, 48)
        self.add_category_btn.setToolTip("添加分类")
        self.add_category_btn.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.add_category_btn.setStyleSheet("""
            QPushButton {
                background-color: #E6F4EA;
                color: #1E8E3E;
                border: none;
                border-radius: 8px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #D3EDE6;
            }
        """)
        self.add_category_btn.clicked.connect(self._add_category)
        add_btn_row.addWidget(self.add_category_btn)

        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.setMinimumSize(48, 48)
        self.refresh_btn.setMaximumSize(48, 48)
        self.refresh_btn.setToolTip("刷新")
        self.refresh_btn.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #5F6368;
                border: 1px solid #E8EAED;
                border-radius: 8px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #DADCE0;
            }
        """)
        self.refresh_btn.clicked.connect(self._load_categories)
        add_btn_row.addWidget(self.refresh_btn)

        add_btn_row.addStretch()
        title_row.addLayout(add_btn_row)

        left_layout.addLayout(title_row)

        # 分类树
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderHidden(True)
        self.category_tree.setExpandsOnDoubleClick(True)
        self.category_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.category_tree.customContextMenuRequested.connect(self._show_category_context_menu)
        self.category_tree.itemClicked.connect(self._on_category_selected)
        self.category_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
                outline: none;
            }
            QTreeWidget::item {
                padding: 4px 6px;
                border-radius: 4px;
                margin: 1px 0;
                color: #3C4043;
            }
            QTreeWidget::item:hover {
                background-color: #F8F9FA;
            }
            QTreeWidget::item:selected {
                background-color: #E8F0FE;
                color: #1A73E8;
                font-weight: 600;
            }
            QTreeWidget:focus {
                border-color: #1A73E8;
            }
        """)
        left_layout.addWidget(self.category_tree)

        splitter.addWidget(left_widget)

        # 右侧：主内容区
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 选项卡 - 淡雅平面风格
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E8EAED;
                border-radius: 8px;
                background-color: #FFFFFF;
                padding: 16px;
            }
            QTabBar::tab {
                background-color: #FFFFFF;
                border: none;
                border-bottom: 2px solid transparent;
                padding: 10px 20px;
                margin-right: 6px;
                font-size: 13px;
                color: #5F6368;
                font-weight: 500;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                border-bottom-color: #1A73E8;
                color: #1A73E8;
                font-weight: 600;
            }
            QTabBar::tab:hover:!selected {
                background-color: #F8F9FA;
                color: #3C4043;
            }
        """)

        # 刷题标签页
        self.question_widget = QuestionWidget(
            self.question_service,
            self.practice_service
        )
        self.tabs.addTab(self.question_widget, "📝 答题")

        # 统计标签页
        self.stats_widget = StatsWidget(self.practice_service)
        self.tabs.addTab(self.stats_widget, "📊 统计")

        right_layout.addWidget(self.tabs)

        splitter.addWidget(right_widget)

        # 设置分割器比例
        splitter.setSizes([170, 1030])
    
    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件 (&F)")
        
        import_action = QAction("📥 导入题目", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self._import_questions)
        file_menu.addAction(import_action)
        
        export_action = QAction("📤 导出题库", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self._export_questions)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction("💾 备份数据库", self)
        backup_action.triggered.connect(self._backup_database)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 题目菜单
        question_menu = menubar.addMenu("题目 (&Q)")

        add_action = QAction("➕ 添加题目", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self._add_question)
        question_menu.addAction(add_action)

        # 设置菜单
        settings_menu = menubar.addMenu("设置 (&S)")

        settings_action = QAction("⚙️ 偏好设置", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._show_settings)
        settings_menu.addAction(settings_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助 (&H)")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """创建工具栏 - 淡雅平面风格"""
        toolbar = QToolBar("主工具栏")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.setMinimumHeight(48)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E8EAED;
                padding: 4px 8px;
                spacing: 8px;
            }
            QToolBar::separator {
                width: 1px;
                background: #E8EAED;
                margin: 6px 4px;
            }
        """)

        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索题目...")
        self.search_input.setMinimumWidth(180)
        self.search_input.setMaximumWidth(280)
        self.search_input.setMinimumHeight(30)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E8EAED;
                border-radius: 6px;
                padding: 4px 8px;
                background-color: #F8F9FA;
                color: #3C4043;
                font-size: 12px;
            }
            QLineEdit:hover {
                border-color: #DADCE0;
            }
            QLineEdit:focus {
                border-color: #1A73E8;
                background-color: #FFFFFF;
            }
        """)
        self.search_input.textChanged.connect(self._on_search_changed)
        toolbar.addWidget(self.search_input)

        toolbar.addSeparator()

        # 添加题目下拉菜单
        add_menu = QMenu(self)
        add_menu.setStyleSheet("""
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 6px;
                padding: 6px 0;
            }
            QMenu::item {
                padding: 8px 16px;
                font-size: 13px;
                color: #3C4043;
            }
            QMenu::item:hover {
                background-color: #E8F0FE;
                color: #1A73E8;
            }
        """)
        add_action = QAction("➕ 添加题目", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self._add_question)
        add_menu.addAction(add_action)

        import_action = QAction("📥 导入题目", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self._import_questions)
        add_menu.addAction(import_action)

        add_btn = QPushButton("➕ 添加")
        add_btn.setMenu(add_menu)
        add_btn.setMinimumHeight(30)
        add_btn.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #E6F4EA;
                color: #1E8E3E;
                border: none;
                border-radius: 6px;
                padding: 5px 12px;
            }
            QPushButton:hover {
                background-color: #D3EDE6;
            }
            QPushButton:focus-visible {
                outline: 2px solid #1E8E3E;
                outline-offset: 2px;
            }
        """)
        toolbar.addWidget(add_btn)

        # 导出/刷新下拉菜单
        export_menu = QMenu(self)
        export_menu.setStyleSheet("""
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 6px;
                padding: 6px 0;
            }
            QMenu::item {
                padding: 8px 16px;
                font-size: 13px;
                color: #3C4043;
            }
            QMenu::item:hover {
                background-color: #E8F0FE;
                color: #1A73E8;
            }
        """)

        export_action = QAction("📤 导出题库", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self._export_questions)
        export_menu.addAction(export_action)

        backup_action = QAction("💾 备份数据库", self)
        backup_action.triggered.connect(self._backup_database)
        export_menu.addAction(backup_action)

        export_menu.addSeparator()

        refresh_action = QAction("🔄 刷新", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_current)
        export_menu.addAction(refresh_action)

        export_btn = QPushButton("📤 导出")
        export_btn.setMenu(export_menu)
        export_btn.setMinimumHeight(30)
        export_btn.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                color: #5F6368;
                border: 1px solid #E8EAED;
                border-radius: 6px;
                padding: 5px 12px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #DADCE0;
            }
            QPushButton:focus-visible {
                outline: 2px solid #1A73E8;
                outline-offset: 2px;
            }
        """)
        toolbar.addWidget(export_btn)
    
    def _create_status_bar(self):
        """创建状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("就绪")
    
    def _load_categories(self):
        """加载分类树"""
        self.category_tree.clear()
        categories = self.question_service.get_categories_tree()
        
        def add_category_item(parent, category):
            item = QTreeWidgetItem(parent)
            item.setText(0, category.name)
            item.setData(0, Qt.ItemDataRole.UserRole, category.id)
            
            for child in category.children:
                add_category_item(item, child)
        
        for cat in categories:
            add_category_item(self.category_tree, cat)
        
        # 添加"全部"选项
        all_item = QTreeWidgetItem(self.category_tree)
        all_item.setText(0, "📖 全部题目")
        all_item.setData(0, Qt.ItemDataRole.UserRole, None)
        self.category_tree.insertTopLevelItem(0, all_item)
    
    def _on_category_selected(self, item, column):
        """分类选择事件"""
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        self.current_category_id = category_id

        # 获取分类名称用于题型过滤
        category_name = item.text(0)

        # 更新题目列表（传递分类名称用于题型过滤）
        self.question_widget.load_questions(category_id, category_name)

        # 更新统计
        if category_id:
            cat = self.question_service.get_category(category_id)
            if cat:
                self.statusbar.showMessage(f"当前分类：{cat.name}")
        else:
            self.statusbar.showMessage("显示全部题目")

    def _show_category_context_menu(self, position):
        """显示分类右键菜单"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction

        item = self.category_tree.itemAt(position)
        if not item or item.text(0) == "📖 全部题目":
            return

        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not category_id:
            return

        menu = QMenu(self)

        # 添加编辑动作
        edit_action = QAction("编辑分类", self)
        edit_action.triggered.connect(lambda: self._edit_category(category_id))
        menu.addAction(edit_action)

        # 添加删除动作
        delete_action = QAction("删除分类", self)
        delete_action.triggered.connect(lambda: self._delete_category(category_id))
        menu.addAction(delete_action)

        menu.exec(self.category_tree.viewport().mapToGlobal(position))

    def _edit_category(self, category_id: int):
        """编辑分类"""
        cat = self.question_service.get_category(category_id)
        if not cat:
            return

        dialog = CategoryDialog(self, self.question_service.get_all_categories())
        dialog.name_input.setText(cat.name)
        dialog.setWindowTitle("编辑分类")

        if dialog.exec():
            name = dialog.get_category_name()
            parent_id = dialog.get_parent_id()

            if name and name != cat.name:
                self.question_service.update_category(category_id, name, parent_id)
                self._load_categories()
                self.statusbar.showMessage(f"已更新分类：{name}")

    def _delete_category(self, category_id: int):
        """删除分类"""
        cat = self.question_service.get_category(category_id)
        if not cat:
            return

        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除分类 '{cat.name}' 吗？\n\n该分类下的所有题目也会被删除！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.question_service.delete_category(category_id)
            self._load_categories()
            self.statusbar.showMessage(f"已删除分类：{cat.name}")

    def _add_category(self):
        """添加分类"""
        dialog = CategoryDialog(self, self.question_service.get_all_categories())
        if dialog.exec():
            name = dialog.get_category_name()
            parent_id = dialog.get_parent_id()
            
            if name:
                self.question_service.create_category(name, parent_id)
                self._load_categories()
                self.statusbar.showMessage(f"已添加分类：{name}")
    
    def _add_question(self):
        """添加题目"""
        categories = self.question_service.get_all_categories()
        dialog = QuestionDialog(self, categories=categories)
        
        if dialog.exec():
            question = dialog.get_question()
            if question:
                self.question_service.create_question(question)
                self._refresh_current()
                self.statusbar.showMessage("题目已添加")
    
    def _import_questions(self):
        """导入题目"""
        dialog = ImportDialog(self)
        if dialog.exec():
            file_path = dialog.get_file_path()
            if file_path:
                try:
                    # 显示加载状态
                    self.start_loading("正在导入题目，请稍候...")

                    questions = self.import_service.import_from_file(file_path)
                    count = self.question_service.batch_import_questions(questions)

                    # 隐藏加载状态
                    self.stop_loading()

                    self._load_categories()
                    self._refresh_current()

                    # 显示成功提示
                    self.show_snackbar(f"成功导入 {count} 道题目", "success")
                except Exception as e:
                    self.stop_loading()
                    # 显示错误提示
                    self.show_snackbar(f"导入失败：{str(e)}", "error", 5000)
    
    def _export_questions(self):
        """导出题目"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出题库", "", "CSV 文件 (*.csv);;Excel 文件 (*.xlsx)"
        )

        if file_path:
            try:
                # 显示加载状态
                self.start_loading("正在导出题目，请稍候...")

                questions = self.question_service.export_questions(self.current_category_id)
                self._do_export(file_path, questions)

                # 隐藏加载状态
                self.stop_loading()

                # 显示成功提示
                self.show_snackbar(f"已导出 {len(questions)} 道题目", "success")
            except Exception as e:
                self.stop_loading()
                # 显示错误提示
                self.show_snackbar(f"导出失败：{str(e)}", "error", 5000)

    def _do_export(self, file_path: str, questions: list):
        """执行导出"""
        import csv
        import json

        if file_path.endswith('.csv'):
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['题目', '选项 A', '选项 B', '选项 C', '选项 D', '选项 E', '选项 F',
                               '答案', '解析', '分类', '难度', '题型', '标签'])
                for q in questions:
                    cat = self.question_service.get_category(q['category_id'])
                    writer.writerow([
                        q['question_text'],
                        q['options'].get('A', ''),
                        q['options'].get('B', ''),
                        q['options'].get('C', ''),
                        q['options'].get('D', ''),
                        q['options'].get('E', ''),
                        q['options'].get('F', ''),
                        q['answer'],
                        q['explanation'],
                        cat.name if cat else '',
                        q['difficulty'],
                        q['question_type'],
                        ','.join(q['tags']) if isinstance(q['tags'], list) else q['tags']
                    ])
        elif file_path.endswith('.xlsx'):
            try:
                import pandas as pd
                data = []
                for q in questions:
                    cat = self.question_service.get_category(q['category_id'])
                    data.append({
                        '题目': q['question_text'],
                        '选项 A': q['options'].get('A', ''),
                        '选项 B': q['options'].get('B', ''),
                        '选项 C': q['options'].get('C', ''),
                        '选项 D': q['options'].get('D', ''),
                        '选项 E': q['options'].get('E', ''),
                        '选项 F': q['options'].get('F', ''),
                        '答案': q['answer'],
                        '解析': q['explanation'],
                        '分类': cat.name if cat else '',
                        '难度': q['difficulty'],
                        '题型': q['question_type'],
                        '标签': ','.join(q['tags']) if isinstance(q['tags'], list) else q['tags']
                    })
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False)
            except ImportError:
                raise ImportError("导出 Excel 需要安装 pandas 和 openpyxl: pip install pandas openpyxl")

    def _on_search_changed(self, text: str):
        """搜索框内容变化"""
        # 将搜索请求传递给题目组件
        if hasattr(self, 'question_widget'):
            self.question_widget.search_text = text

    def _backup_database(self):
        """备份数据库"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "备份数据库", "quizmaster_backup.db", "数据库文件 (*.db)"
        )
        
        if file_path:
            try:
                self.db.backup(file_path)
                QMessageBox.information(
                    self, "备份完成",
                    "数据库备份成功"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "备份失败",
                    f"备份过程中出错：{str(e)}"
                )
    
    def _refresh_current(self):
        """刷新当前视图"""
        self.question_widget.load_questions(self.current_category_id)
        self.stats_widget.load_stats()
        self.statusbar.showMessage("已刷新")
    
    def _show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, "关于 QuizMaster",
            "<h2>QuizMaster - 逢考必过</h2>"
            "<p>版本：1.5.5</p>"
            "<p>一款高效的题库管理和刷题工具</p>"
            "<p>技术栈：Python + PyQt6 + SQLite</p>"
            "<p>© 2026</p>"
        )

    def _show_settings(self):
        """显示设置对话框"""
        from ui.settings_dialog import SettingsDialog
        # 从题目组件获取当前设置
        settings = self.question_widget.settings
        dialog = SettingsDialog(self, settings)
        if dialog.exec():
            new_settings = dialog.get_settings()
            self.question_widget.settings = new_settings
            self.question_widget._save_settings(new_settings)
    
    def _apply_styles(self):
        """应用样式 - 加载外部样式表"""
        # 加载外部样式表文件
        style_path = Path(__file__).parent / "stylesheet.qss"
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            # 如果样式表文件不存在，使用内置样式
            self.setStyleSheet(self._get_builtin_styles())

    def _get_builtin_styles(self):
        """内置样式（备用）"""
        return """
            QMainWindow {
                background-color: #fafafa;
            }

            /* 菜单条 */
            QMenuBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E8EAED;
                padding: 6px 0;
            }
            QMenuBar::item:selected {
                background-color: #f8f9fa;
                border-radius: 6px;
            }

            /* 菜单 */
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 8px;
                padding: 8px 0;
            }
            QMenu::item {
                padding: 10px 20px;
                font-size: 13px;
                color: #3c4043;
            }
            QMenu::item:selected {
                background-color: #E8F0FE;
                color: #1A73E8;
            }
            QMenu::separator {
                height: 1px;
                background: #E8EAED;
                margin: 6px 0;
            }

            /* 状态栏 */
            QStatusBar {
                background-color: #FFFFFF;
                border-top: 1px solid #E8EAED;
                color: #5f6368;
                font-size: 12px;
            }

            /* 按钮 */
            QPushButton {
                background-color: #E8F0FE;
                color: #1A73E8;
                border: 1px solid #D2E3FC;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #D2E3FC;
            }
            QPushButton:pressed {
                background-color: #BHD0FB;
            }
            QPushButton:disabled {
                background-color: #F1F3F4;
                color: #9AA0A6;
                border-color: #E8EAED;
            }

            /* 输入框 */
            QLineEdit, QTextEdit {
                border: 1px solid #E8EAED;
                border-radius: 8px;
                padding: 10px 14px;
                background-color: #FFFFFF;
                font-size: 13px;
                color: #3C4043;
                selection-background-color: #D2E3FC;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #1A73E8;
                outline: none;
            }

            /* 下拉框 */
            QComboBox {
                border: 1px solid #E8EAED;
                border-radius: 8px;
                padding: 8px 14px;
                background-color: #FFFFFF;
                font-size: 13px;
            }
            QComboBox:focus {
                border-color: #1A73E8;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E8EAED;
                border-radius: 8px;
                background-color: #FFFFFF;
                selection-background-color: #E8F0FE;
                selection-color: #5F6368;
            }

            /* 进度条 */
            QProgressBar {
                border: none;
                border-radius: 10px;
                text-align: center;
                background-color: #E8EAED;
                height: 24px;
                font-size: 12px;
                color: #5F6368;
            }
            QProgressBar::chunk {
                background-color: #81C995;
                border-radius: 10px;
            }

            /* 滚动条 */
            QScrollBar:vertical {
                background-color: #F1F3F4;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #DADCE0;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #BDC1C6;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }

            /* 标签 */
            QLabel {
                color: #202124;
                background-color: transparent;
            }
        """

    def show_snackbar(self, message: str, status: str = "info", duration: int = 3000):
        """显示 Snackbar 提示

        Args:
            message: 提示消息
            status: 状态类型 (info, success, error, warning)
            duration: 显示时长 (毫秒)
        """
        # 创建 snackbar 框架
        self.snackbar = QFrame()
        self.snackbar.setObjectName("snackbar")
        self.snackbar.setProperty("status", status)
        self.snackbar.setFixedHeight(50)
        self.snackbar.setStyleSheet("""
            QFrame#snackbar {
                background-color: #3C4043;
                color: #FFFFFF;
                border-radius: 8px;
                padding: 12px 16px;
            }
            QFrame#snackbar[status="success"] {
                background-color: #1E8E3E;
            }
            QFrame#snackbar[status="error"] {
                background-color: #D93025;
            }
            QFrame#snackbar[status="warning"] {
                background-color: #F9AB00;
                color: #202124;
            }
        """)

        # 添加阴影效果
        from PyQt6.QtGui import QDropShadow
        shadow = QGraphicsOpacityEffect()
        self.snackbar.setGraphicsEffect(shadow)

        # 布局
        layout = QVBoxLayout(self.snackbar)
        label = QLabel(message)
        label.setStyleSheet("color: inherit; font-size: 14px;")
        layout.addWidget(label)

        # 定位在底部中央
        self.snackbar.setParent(self.centralWidget())
        self.snackbar.show()

        # 设置定时器自动隐藏
        QTimer.singleShot(duration, self.snackbar.deleteLater)

    def start_loading(self, message: str = "加载中..."):
        """显示加载状态

        Args:
            message: 加载提示文字
        """
        # 创建加载面板
        self.loading_overlay = QFrame()
        self.loading_overlay.setObjectName("loading_panel")
        self.loading_overlay.setGeometry(self.centralWidget().rect())
        self.loading_overlay.setStyleSheet("""
            QFrame#loading_panel {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 24px;
            }
        """)

        # 加载文字
        layout = QVBoxLayout(self.loading_overlay)
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #5F6368; font-size: 14px;")
        layout.addWidget(label)

        self.loading_overlay.raise_()
        self.loading_overlay.show()

    def stop_loading(self):
        """隐藏加载状态"""
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.hide()
            self.loading_overlay.deleteLater()

    def closeEvent(self, event):
        """关闭事件"""
        self.db.close()
        event.accept()

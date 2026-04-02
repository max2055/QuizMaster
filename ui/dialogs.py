"""
对话框 - 各种弹窗对话框
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QFileDialog,
    QTextEdit, QButtonGroup, QRadioButton, QWidget,
    QScrollArea, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from database.models import Question, Category


class CategoryDialog(QDialog):
    """添加/编辑分类对话框"""

    def __init__(self, parent=None, categories=None):
        super().__init__(parent)
        self.setWindowTitle("添加分类")
        self.setMinimumWidth(450)
        self.setMinimumHeight(280)

        # 设置浅色主题
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
            QLabel {
                color: #3C4043;
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #DADCE0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: #F8F9FA;
                font-size: 13px;
                color: #3C4043;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #1A73E8;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        # 标题
        title_label = QLabel("添加分类")
        title_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #3C4043; padding-bottom: 8px;")
        layout.addWidget(title_label)

        # 分类名称
        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入分类名称")
        self.name_input.setMinimumHeight(36)
        form_layout.addRow("分类名称:", self.name_input)

        # 父分类
        self.parent_combo = QComboBox()
        self.parent_combo.addItem("无（作为顶级分类）", None)
        self.parent_combo.setMinimumHeight(36)

        if categories:
            for cat in categories:
                self.parent_combo.addItem(cat.name, cat.id)

        form_layout.addRow("父分类:", self.parent_combo)

        layout.addLayout(form_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.setMinimumHeight(36)
        cancel_btn.setMinimumWidth(80)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #5F6368;
                border: 1px solid #DADCE0;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #5F6368;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("确定")
        ok_btn.setMinimumHeight(36)
        ok_btn.setMinimumWidth(80)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_category_name(self) -> str:
        """获取分类名称"""
        return self.name_input.text().strip()

    def get_parent_id(self):
        """获取父分类 ID"""
        return self.parent_combo.currentData()


class QuestionDialog(QDialog):
    """添加/编辑题目对话框"""

    def __init__(self, parent=None, question: Question = None, categories=None):
        super().__init__(parent)
        self.setWindowTitle("编辑题目" if question else "添加题目")
        self.setMinimumSize(650, 550)

        self.question = question

        # 设置浅色主题
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
            QLabel {
                color: #3C4043;
                font-size: 13px;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #DADCE0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: #F8F9FA;
                font-size: 13px;
                color: #3C4043;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #1A73E8;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_label = QLabel("编辑题目" if question else "添加题目")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #3C4043; padding-bottom: 10px;")
        layout.addWidget(title_label)

        # 使用滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #FFFFFF; border: none;")

        container = QWidget()
        container.setStyleSheet("background-color: #FFFFFF;")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # 题目内容
        self.question_text = QTextEdit()
        self.question_text.setPlaceholderText("输入题目内容...")
        self.question_text.setMinimumHeight(100)
        if question:
            self.question_text.setText(question.question_text)
        form_layout.addRow("题目内容:", self.question_text)

        # 分类
        self.category_combo = QComboBox()
        if categories:
            for cat in categories:
                self.category_combo.addItem(cat.name, cat.id)
        if question and question.category_id:
            index = self.category_combo.findData(question.category_id)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        form_layout.addRow("所属分类:", self.category_combo)

        # 题型
        self.type_combo = QComboBox()
        self.type_combo.addItems(["单选题", "多选题", "判断题", "填空题"])
        self.type_map = {'single': 0, 'multi': 1, 'true_false': 2, 'fill': 3}
        self.type_map_rev = {0: 'single', 1: 'multi', 2: 'true_false', 3: 'fill'}
        if question:
            self.type_combo.setCurrentIndex(self.type_map.get(question.question_type, 0))
        form_layout.addRow("题型:", self.type_combo)

        # 难度
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["简单", "中等", "困难"])
        self.diff_map = {'easy': 0, 'medium': 1, 'hard': 2}
        self.diff_map_rev = {0: 'easy', 1: 'medium', 2: 'hard'}
        if question:
            self.difficulty_combo.setCurrentIndex(self.diff_map.get(question.difficulty, 1))
        form_layout.addRow("难度:", self.difficulty_combo)

        # 选项
        options_widget = QWidget()
        options_layout = QVBoxLayout(options_widget)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(8)

        self.option_inputs = {}
        for opt in ['A', 'B', 'C', 'D', 'E', 'F']:
            opt_layout = QHBoxLayout()
            opt_layout.setSpacing(8)
            opt_label = QLabel(f"选项{opt}:")
            opt_label.setStyleSheet("color: #555; font-size: 12px;")
            opt_label.setMinimumWidth(50)
            opt_input = QLineEdit()
            opt_input.setPlaceholderText(f"输入选项{opt}的内容")
            opt_input.setMinimumHeight(32)

            if question and opt in question.options:
                opt_input.setText(question.options[opt])

            self.option_inputs[opt] = opt_input
            opt_layout.addWidget(opt_label)
            opt_layout.addWidget(opt_input, 1)  #  stretch factor 1
            options_layout.addLayout(opt_layout)

        form_layout.addRow("选项:", options_widget)

        # 答案
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("例如：A 或 ABC")
        self.answer_input.setMinimumHeight(32)
        if question:
            self.answer_input.setText(question.answer)
        form_layout.addRow("正确答案:", self.answer_input)

        # 解析
        self.explanation_input = QTextEdit()
        self.explanation_input.setPlaceholderText("输入答案解析（可选）")
        self.explanation_input.setMinimumHeight(80)
        if question:
            self.explanation_input.setText(question.explanation)
        form_layout.addRow("答案解析:", self.explanation_input)

        # 标签
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("用逗号分隔，例如：数学，代数，方程")
        self.tags_input.setMinimumHeight(32)
        if question:
            self.tags_input.setText(','.join(question.tags))
        form_layout.addRow("标签:", self.tags_input)

        container.setLayout(form_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.setMinimumHeight(36)
        cancel_btn.setMinimumWidth(80)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #5F6368;
                border: 1px solid #DADCE0;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #5F6368;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("保存")
        ok_btn.setMinimumHeight(36)
        ok_btn.setMinimumWidth(80)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        ok_btn.clicked.connect(self._on_accept)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _on_accept(self):
        """确定按钮处理"""
        # 验证必填字段
        if not self.question_text.toPlainText().strip():
            return
        if not self.answer_input.text().strip():
            return

        self.accept()

    def get_question(self) -> Question:
        """获取题目数据"""
        # 构建选项
        options = {}
        for opt, input_widget in self.option_inputs.items():
            text = input_widget.text().strip()
            if text:
                options[opt] = text

        # 获取标签
        tags_text = self.tags_input.text().strip()
        tags = [t.strip() for t in tags_text.split(',') if t.strip()] if tags_text else []

        question = Question(
            id=self.question.id if self.question else None,
            category_id=self.category_combo.currentData(),
            question_text=self.question_text.toPlainText().strip(),
            question_type=self.type_map_rev[self.type_combo.currentIndex()],
            options=options,
            answer=self.answer_input.text().strip().upper(),
            explanation=self.explanation_input.toPlainText().strip(),
            difficulty=self.diff_map_rev[self.difficulty_combo.currentIndex()],
            tags=tags
        )

        return question


class ImportDialog(QDialog):
    """导入题目对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("导入题目")
        self.setMinimumWidth(500)
        self.setMinimumHeight(350)

        self.file_path = None

        # 设置浅色主题
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
            QLabel {
                color: #3C4043;
                font-size: 13px;
            }
            QLineEdit {
                border: 1px solid #DADCE0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: #F8F9FA;
                font-size: 13px;
                color: #3C4043;
            }
            QLineEdit:focus {
                border-color: #1A73E8;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 20, 24, 20)

        # 标题
        title_label = QLabel("导入题目")
        title_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #3C4043; padding-bottom: 8px;")
        layout.addWidget(title_label)

        # 说明
        info_label = QLabel(
            "<p style='color: #5F6368;'>支持从 Excel、CSV 或 Word 文件导入题目。</p>"
            "<p style='color: #5F6368;'><b>Excel/CSV 格式要求：</b></p>"
            "<ul style='color: #5F6368;'>"
            "<li>题目（必需）</li>"
            "<li>选项 A、B、C、D 等（可选）</li>"
            "<li>答案（必需）</li>"
            "<li>解析、分类、难度（可选）</li>"
            "</ul>"
        )
        info_label.setWordWrap(True)
        info_label.setOpenExternalLinks(True)
        info_label.setStyleSheet("color: #5F6368; line-height: 1.6;")
        layout.addWidget(info_label)

        # 文件选择
        file_layout = QHBoxLayout()
        file_layout.setSpacing(10)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("选择要导入的文件...")
        self.file_input.setReadOnly(True)
        self.file_input.setMinimumHeight(36)
        file_layout.addWidget(self.file_input, 1)

        browse_btn = QPushButton("浏览...")
        browse_btn.setMinimumHeight(36)
        browse_btn.setMinimumWidth(80)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #5F6368;
                border: 1px solid #DADCE0;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #5F6368;
            }
        """)
        browse_btn.clicked.connect(self._browse_file)
        file_layout.addWidget(browse_btn)

        layout.addLayout(file_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.setMinimumHeight(36)
        cancel_btn.setMinimumWidth(80)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #5F6368;
                border: 1px solid #DADCE0;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #5F6368;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("导入")
        ok_btn.setMinimumHeight(36)
        ok_btn.setMinimumWidth(80)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        ok_btn.clicked.connect(self._on_accept)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _browse_file(self):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "",
            "所有支持的文件 (*.xlsx *.xls *.csv *.docx *.doc);;"
            "Excel 文件 (*.xlsx *.xls);;"
            "CSV 文件 (*.csv);;"
            "Word 文件 (*.docx *.doc)"
        )

        if file_path:
            self.file_path = file_path
            self.file_input.setText(file_path)

    def _on_accept(self):
        """确定按钮处理"""
        if not self.file_path:
            return
        self.accept()

    def get_file_path(self) -> str:
        """获取文件路径"""
        return self.file_path

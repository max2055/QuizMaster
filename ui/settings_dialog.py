"""设置对话框 - 应用配置设置"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QSpinBox, QFrame, QWidget, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, parent=None, settings=None):
        super().__init__(parent)

        # 默认设置
        self.settings = settings or {
            'auto_next': False,
            'auto_next_delay': 500,
            'show_answer_after_submit': True,
            'confirm_before_submit': True,
            'remember_window_size': True,
            'questions_per_session': 50,
        }

        self.setWindowTitle("设置")
        self.setMinimumSize(480, 500)
        self.resize(520, 550)
        self.setSizeGripEnabled(True)
        self.setModal(True)

        self._init_ui()

    def _init_ui(self):
        """初始化界面"""
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # 标题栏
        title_widget = QWidget()
        title_widget.setStyleSheet("""
            QWidget {
                background-color: #FAFBFC;
                border-bottom: 1px solid #E8EAED;
            }
        """)
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(20, 12, 20, 12)

        title = QLabel("⚙ 偏好设置")
        title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title.setStyleSheet("color: #3C4043;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addWidget(title_widget)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: #FFFFFF; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(4)  # 从 8 改为 4，缩短间距
        content_layout.setContentsMargins(8, 8, 8, 8)  # 从 12 改为 8

        # 答题设置组
        self._create_section(content_layout, "📝 答题设置", self._create_practice_settings)

        # 显示设置组
        self._create_section(content_layout, "🖥️ 显示设置", self._create_display_settings)

        # 窗口设置组
        self._create_section(content_layout, "🪟 窗口设置", self._create_window_settings)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll, 1)

        # 按钮栏
        button_widget = QWidget()
        button_widget.setStyleSheet("""
            QWidget {
                background-color: #FAFBFC;
                border-top: 1px solid #E8EAED;
            }
        """)
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(20, 16, 20, 16)
        button_layout.addStretch()

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(80, 36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #5F6368;
                border: 1px solid #DADCE0;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #5F6368;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        # 确定按钮
        ok_btn = QPushButton("确定")
        ok_btn.setFixedSize(80, 36)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)

        layout.addWidget(button_widget)

    def _create_section(self, parent_layout, title, content_func):
        """创建设置区域"""
        section_widget = QWidget()
        section_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 8px;
            }
        """)
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(8, 4, 8, 4)
        section_layout.setSpacing(2)

        # 标题 - 图标和文字之间增加间距
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #3C4043; letter-spacing: 0.5px;")
        section_layout.addWidget(title_label)

        # 内容
        content_func(section_layout)

        parent_layout.addWidget(section_widget)

    def _create_practice_settings(self, layout):
        """创建答题设置"""
        # 自动下一题
        self.auto_next_cb = self._create_check_box("答题后自动跳转到下一题", self.settings.get('auto_next', False))
        layout.addWidget(self.auto_next_cb)

        # 延迟设置 - 紧凑布局
        delay_widget = QWidget()
        delay_layout = QHBoxLayout(delay_widget)
        delay_layout.setContentsMargins(20, 2, 0, 2)
        delay_layout.setSpacing(6)

        delay_label = QLabel("延迟：")
        delay_label.setStyleSheet("color: #5F6368; font-size: 13px;")
        delay_layout.addWidget(delay_label)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(100, 3000)
        self.delay_spin.setSingleStep(100)
        self.delay_spin.setValue(self.settings.get('auto_next_delay', 500))
        self.delay_spin.setFixedWidth(90)
        delay_layout.addWidget(self.delay_spin)

        delay_unit = QLabel("毫秒")
        delay_unit.setStyleSheet("color: #5F6368; font-size: 11px;")
        delay_unit.setFixedWidth(35)
        delay_layout.addWidget(delay_unit)

        delay_layout.addStretch()
        layout.addWidget(delay_widget)

        # 联动
        self.auto_next_cb.toggled.connect(self.delay_spin.setEnabled)

        # 每次刷题数量 - 紧凑布局
        quantity_widget = QWidget()
        quantity_layout = QHBoxLayout(quantity_widget)
        quantity_layout.setContentsMargins(20, 2, 0, 2)
        quantity_layout.setSpacing(6)

        quantity_label = QLabel("数量：")
        quantity_label.setStyleSheet("color: #5F6368; font-size: 13px;")
        quantity_layout.addWidget(quantity_label)

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(10, 500)
        self.quantity_spin.setSingleStep(10)
        self.quantity_spin.setValue(self.settings.get('questions_per_session', 50))
        self.quantity_spin.setFixedWidth(90)
        quantity_layout.addWidget(self.quantity_spin)

        quantity_unit = QLabel("题")
        quantity_unit.setStyleSheet("color: #5F6368; font-size: 11px;")
        quantity_unit.setFixedWidth(20)
        quantity_layout.addWidget(quantity_unit)

        quantity_layout.addStretch()
        layout.addWidget(quantity_widget)

    def _create_display_settings(self, layout):
        """创建显示设置"""
        self.show_answer_cb = self._create_check_box("提交后显示答案和解析", self.settings.get('show_answer_after_submit', True))
        layout.addWidget(self.show_answer_cb)

        self.confirm_submit_cb = self._create_check_box("提交前显示确认对话框", self.settings.get('confirm_before_submit', True))
        layout.addWidget(self.confirm_submit_cb)

    def _create_window_settings(self, layout):
        """创建窗口设置"""
        self.remember_size_cb = self._create_check_box("记住窗口大小和位置", self.settings.get('remember_window_size', True))
        layout.addWidget(self.remember_size_cb)

    def _create_check_box(self, text: str, checked: bool = False) -> QCheckBox:
        """创建复选框"""
        cb = QCheckBox(text)
        cb.setChecked(checked)
        cb.setFont(QFont("Arial", 11))
        cb.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        cb.setStyleSheet("""
            QCheckBox {
                color: #3C4043;
                spacing: 8px;
                margin-top: 0px;
                margin-bottom: 0px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #DADCE0;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:hover {
                border-color: #1A73E8;
            }
            QCheckBox::indicator:checked {
                background-color: #1A73E8;
                border-color: #1A73E8;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOSAxNi4yTDQuOCAxMmwtMS40IDEuNEw5IDE5IDIxIDdsLTEuNC0xLjRMOSAxNi4yeiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=);
            }
            QCheckBox::indicator:checked:hover {
                background-color: #1557B0;
                border-color: #1557B0;
            }
        """)
        return cb

    def get_settings(self) -> dict:
        """获取设置"""
        return {
            'auto_next': self.auto_next_cb.isChecked(),
            'auto_next_delay': self.delay_spin.value(),
            'show_answer_after_submit': self.show_answer_cb.isChecked(),
            'confirm_before_submit': self.confirm_submit_cb.isChecked(),
            'remember_window_size': self.remember_size_cb.isChecked(),
            'questions_per_session': self.quantity_spin.value(),
        }

"""题目显示组件 - 刷题练习界面"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QRadioButton, QButtonGroup, QFrame,
    QScrollArea, QLineEdit, QMessageBox, QDialog, QCheckBox,
    QGridLayout, QSizePolicy, QMenu
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSettings
from PyQt6.QtGui import QFont, QAction

from database.models import Question
from services.question_service import QuestionService
from services.practice_service import PracticeService
from ui.settings_dialog import SettingsDialog


class ResultSummaryDialog(QDialog):
    """提交结果汇总对话框"""
    question_clicked = pyqtSignal(int)
    
    def __init__(self, parent=None, questions=None, user_answers=None, answer_results=None):
        super().__init__(parent)
        self.questions = questions or []
        self.user_answers = user_answers or {}
        self.answer_results = answer_results or {}
        
        self.setWindowTitle("练习结果汇总")
        self.setMinimumSize(800, 600)
        
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("📊 练习结果汇总")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3C4043; padding: 10px;")
        layout.addWidget(title)
        
        # 统计信息
        total = len(self.questions)
        answered = len(self.user_answers)
        correct = sum(1 for v in self.answer_results.values() if v)
        wrong = answered - correct
        accuracy = (correct / answered * 100) if answered > 0 else 0

        stats = [
            ("总题数", total, "#5F6368", "#F8F9FA"),
            ("已作答", answered, "#1A73E8", "#E8F0FE"),
            ("正确", correct, "#1E8E3E", "#E6F4EA"),
            ("错误", wrong, "#D93025", "#FCE8E6"),
            ("正确率", f"{accuracy:.1f}%", "#F9AB00", "#FEF7E0")
        ]

        # 统计卡片横向布局
        stats_layout_widget = QWidget()
        stats_layout = QHBoxLayout(stats_layout_widget)
        stats_layout.setSpacing(10)
        stats_layout.setContentsMargins(10, 10, 10, 10)

        for label, value, color, bg_color in stats:
            card = QFrame()
            card.setObjectName(f"stats_card_{label}")
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border: 2px solid {color};
                    border-radius: 8px;
                    padding: 15px;
                }}
            """)
            card_layout = QVBoxLayout(card)

            lbl = QLabel(label)
            lbl.setFont(QFont("Arial", 11))
            lbl.setStyleSheet(f"color: {color};")
            card_layout.addWidget(lbl)

            val = QLabel(str(value))
            val.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            val.setStyleSheet(f"color: {color};")
            val.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(val)

            stats_layout.addWidget(card)

        layout.addWidget(stats_layout_widget)

        # 题目列表
        list_label = QLabel("📋 题目详情（点击题号查看解析）")
        list_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        list_label.setStyleSheet("color: #3C4043; padding: 10px 0;")
        layout.addWidget(list_label)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        
        for idx, question in enumerate(self.questions):
            row = QHBoxLayout()
            row.setSpacing(10)

            # 题号按钮 - 使用 QLabel 确保文本完整显示
            num_container = QWidget()
            num_container.setFixedSize(90, 35)
            num_container.setStyleSheet("""
                QWidget {
                    border-radius: 4px;
                }
            """)
            num_container.setCursor(Qt.CursorShape.PointingHandCursor)

            # 创建布局
            num_layout = QVBoxLayout(num_container)
            num_layout.setContentsMargins(0, 0, 0, 0)

            # 标签显示文字 - 使用连续编号
            serial = question.serial_number or (idx + 1)
            num_label = QLabel(f"第{serial}题")
            num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            num_label.setFont(QFont("Arial", 11, QFont.Weight.Medium))

            # 设置背景色
            if idx in self.user_answers:
                if self.answer_results.get(idx, False):
                    num_label.setStyleSheet("""
                        QLabel {
                            background-color: #1E8E3E;
                            color: white;
                            border-radius: 4px;
                        }
                    """)
                    status = "✓ 正确"
                    status_color = "#1E8E3E"
                else:
                    num_label.setStyleSheet("""
                        QLabel {
                            background-color: #D93025;
                            color: white;
                            border-radius: 4px;
                        }
                    """)
                    status = "✗ 错误"
                    status_color = "#D93025"
            else:
                num_label.setStyleSheet("""
                    QLabel {
                        background-color: #5F6368;
                        color: white;
                        border-radius: 4px;
                    }
                """)
                status = "未作答"
                status_color = "#5F6368"

            num_layout.addWidget(num_label)

            # 点击事件
            num_container.mousePressEvent = lambda e, i=idx: self._on_question_clicked(i)
            row.addWidget(num_container)
            
            # 状态
            status_label = QLabel(status)
            status_label.setFont(QFont("Arial", 11))
            status_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")
            status_label.setFixedWidth(80)
            row.addWidget(status_label)
            
            # 用户答案
            if idx in self.user_answers:
                user_ans = QLabel(f"你的答案: {self.user_answers[idx]}")
                user_ans.setFont(QFont("Arial", 11))
                user_ans.setStyleSheet("color: #3C4043;")
                row.addWidget(user_ans)
                
                correct_ans = QLabel(f"正确答案: {question.answer.upper()}")
                correct_ans.setFont(QFont("Arial", 11))
                correct_ans.setStyleSheet("color: #1A73E8;")
                row.addWidget(correct_ans)
            
            row.addStretch()
            container_layout.addLayout(row)
        
        scroll.setWidget(container)
        layout.addWidget(scroll, 1)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
    
    def _on_question_clicked(self, index):
        """点击题号"""
        self.question_clicked.emit(index)
        self.accept()


class QuestionWidget(QWidget):
    """题目练习组件"""

    def __init__(self, question_service, practice_service):
        super().__init__()

        self.question_service = question_service
        self.practice_service = practice_service

        self.questions = []
        self.all_questions = []  # 存储所有题目，用于分页
        self.current_index = 0
        self.current_question = None
        self.user_answers = {}
        self.answer_results = {}
        self.marked_questions = set()
        self.start_time = None
        self.current_session_id = None
        self.session_submitted = False
        self.practice_mode = "sequence"

        # 刷题进度
        self.current_offset = 0  # 当前题号偏移量
        self.questions_per_session = 50  # 每次刷题数量

        # 当前分类信息（用于题型过滤）
        self.current_category_id = None
        self.current_category_name = None

        # 加载设置
        self.settings = self._load_settings()
        self.auto_next = self.settings.get('auto_next', False)
        self.auto_next_delay = self.settings.get('auto_next_delay', 500)
        self.questions_per_session = self.settings.get('questions_per_session', 50)
        self.continue_last_session = self.settings.get('continue_last_session', False)

        self._init_ui()
        self._setup_shortcuts()
        self._load_marked_questions()

    def _load_settings(self) -> dict:
        """加载设置"""
        settings = QSettings('QuizMaster', 'Settings')
        return {
            'auto_next': settings.value('auto_next', False, type=bool),
            'auto_next_delay': settings.value('auto_next_delay', 500, type=int),
            'show_answer_after_submit': settings.value('show_answer_after_submit', True, type=bool),
            'confirm_before_submit': settings.value('confirm_before_submit', True, type=bool),
            'remember_window_size': settings.value('remember_window_size', True, type=bool),
            'questions_per_session': settings.value('questions_per_session', 50, type=int),
            'continue_last_session': settings.value('continue_last_session', False, type=bool),
            'start_from_question_single': settings.value('start_from_question_single', 1, type=int),
            'start_from_question_multi': settings.value('start_from_question_multi', 1, type=int),
            'start_from_question_judge': settings.value('start_from_question_judge', 1, type=int),
            'start_from_question_fill': settings.value('start_from_question_fill', 1, type=int),
            'last_practice_offset': settings.value('last_practice_offset', 0, type=int),
            'last_practice_mode': settings.value('last_practice_mode', 'sequence', type=str),
        }

    def _save_settings(self, settings: dict):
        """保存设置"""
        qsettings = QSettings('QuizMaster', 'Settings')
        for key, value in settings.items():
            qsettings.setValue(key, value)

    def _save_progress(self):
        """保存当前进度"""
        qsettings = QSettings('QuizMaster', 'Settings')
        qsettings.setValue('last_practice_offset', self.current_offset + self.current_index)
        qsettings.setValue('last_practice_mode', self.practice_mode)

    def _load_marked_questions(self):
        """加载已标记的题目"""
        try:
            self.marked_questions = self.practice_service.get_marked_questions()
        except Exception as e:
            print(f"加载标记题目失败：{e}")
            self.marked_questions = set()

    def _init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 左侧：主内容区
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部控制栏 - 整合模式按钮、开始练习、设置
        control_widget = QWidget()
        control_widget.setObjectName("control_widget")
        control_widget.setStyleSheet("""
            QWidget#control_widget {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E8EAED;
            }
        """)
        control_layout = QHBoxLayout(control_widget)
        control_layout.setSpacing(8)
        control_layout.setContentsMargins(10, 6, 10, 6)

        # 模式切换 - 分段按钮样式（缩小版）
        mode_container = QWidget()
        mode_layout = QHBoxLayout(mode_container)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(0)

        self.mode_btns = {}
        for i, (mode, label) in enumerate([("sequence", "顺序"), ("random", "随机"), ("wrong", "错题")]):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=mode: self._set_mode(m))
            btn.setMinimumHeight(28)
            btn.setMinimumWidth(55)
            btn.setFont(QFont("Arial", 10))

            # 分段按钮样式
            if i == 0:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #F8F9FA;
                        color: #5F6368;
                        border: 1px solid #DADCE0;
                        border-right: none;
                        border-top-left-radius: 4px;
                        border-bottom-left-radius: 4px;
                    }
                    QPushButton:checked {
                        background-color: #1A73E8;
                        color: white;
                        border-color: #1A73E8;
                    }
                    QPushButton:hover:!checked {
                        background-color: #F1F3F4;
                    }
                """)
            elif i == 2:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #F8F9FA;
                        color: #5F6368;
                        border: 1px solid #DADCE0;
                        border-left: none;
                        border-top-right-radius: 4px;
                        border-bottom-right-radius: 4px;
                    }
                    QPushButton:checked {
                        background-color: #1A73E8;
                        color: white;
                        border-color: #1A73E8;
                    }
                    QPushButton:hover:!checked {
                        background-color: #F1F3F4;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #F8F9FA;
                        color: #5F6368;
                        border: 1px solid #DADCE0;
                        border-left: none;
                        border-right: none;
                    }
                    QPushButton:checked {
                        background-color: #1A73E8;
                        color: white;
                        border-color: #1A73E8;
                    }
                    QPushButton:hover:!checked {
                        background-color: #F1F3F4;
                    }
                """)

            mode_layout.addWidget(btn)
            self.mode_btns[mode] = btn

        self.mode_btns["sequence"].setChecked(True)
        control_layout.addWidget(mode_container)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("background-color: #E8EAED; min-width: 1px; max-width: 1px;")
        control_layout.addWidget(separator)

        # 开始练习按钮
        self.start_btn = QPushButton("▶ 开始练习")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self._start_practice)
        self.start_btn.setMinimumHeight(28)
        self.start_btn.setMinimumWidth(80)
        self.start_btn.setFont(QFont("Arial", 10, QFont.Weight.Medium))
        self.start_btn.setStyleSheet("""
            QPushButton#start_btn {
                background-color: #1A73E8;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton#start_btn:hover {
                background-color: #1557B0;
            }
        """)
        control_layout.addWidget(self.start_btn)

        # 设置按钮
        self.settings_btn = QPushButton("⚙ 设置")
        self.settings_btn.setMinimumHeight(28)
        self.settings_btn.setMinimumWidth(50)
        self.settings_btn.setFont(QFont("Arial", 10))
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                color: #5F6368;
                border: 1px solid #DADCE0;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #1A73E8;
                color: #1A73E8;
            }
        """)
        self.settings_btn.clicked.connect(self._show_settings)
        control_layout.addWidget(self.settings_btn)

        control_layout.addStretch()
        left_layout.addWidget(control_widget)

        # 题目区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #FFFFFF;
            }
        """)

        self.question_container = QWidget()
        self.question_container.setObjectName("question_container")
        self.question_container.setStyleSheet("""
            QWidget#question_container {
                background-color: #FFFFFF;
            }
        """)
        self.question_layout = QVBoxLayout(self.question_container)
        self.question_layout.setSpacing(10)
        self.question_layout.setContentsMargins(12, 12, 12, 12)

        scroll.setWidget(self.question_container)
        left_layout.addWidget(scroll, 1)

        # 题目内容 - 淡雅平面风格
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Arial", 18, QFont.Weight.Medium))
        self.question_label.setObjectName("question_label")
        self.question_label.setStyleSheet("""
            QLabel#question_label {
                padding: 16px 20px;
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 8px;
                color: #3C4043;
                line-height: 1.6;
            }
        """)
        self.question_layout.addWidget(self.question_label)

        # 选项区域
        self.option_group = QButtonGroup(self)
        self.option_buttons = []

        self.options_layout = QVBoxLayout()
        self.options_layout.setSpacing(6)

        # 选项按钮样式 - 淡雅平面风格
        radio_style = """
            QRadioButton {
                background-color: #FFFFFF;
                border: 1px solid #DADCE0;
                border-radius: 8px;
                color: #3C4043;
                min-height: 50px;
                padding: 12px 14px;
                font-size: 16px;
            }
            QRadioButton:hover {
                border-color: #1A73E8;
                background-color: #E8F0FE;
            }
            QRadioButton:checked {
                border-color: #1A73E8;
                background-color: #E8F0FE;
                color: #1A73E8;
                font-weight: 600;
                border-width: 2px;
            }
            QRadioButton::indicator {
                width: 0px;
                height: 0px;
            }
        """

        checkbox_style = """
            QCheckBox {
                background-color: #FFFFFF;
                border: 1px solid #DADCE0;
                border-radius: 8px;
                color: #3C4043;
                min-height: 50px;
                padding: 12px 14px;
                font-size: 16px;
            }
            QCheckBox:hover {
                border-color: #1A73E8;
                background-color: #E8F0FE;
            }
            QCheckBox:checked {
                border-color: #1A73E8;
                background-color: #E8F0FE;
                color: #1A73E8;
                font-weight: 600;
                border-width: 2px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #DADCE0;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #1A73E8;
                border-color: #1A73E8;
            }
        """

        # 判断题按钮样式 - 淡雅平面风格
        true_false_btn_style = """
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #DADCE0;
                border-radius: 8px;
                color: #3C4043;
                min-height: 40px;
                padding: 12px 14px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                border-color: #1A73E8;
                background-color: #E8F0FE;
            }
            QPushButton:checked {
                border-color: #1A73E8;
                background-color: #E8F0FE;
                color: #1A73E8;
            }
        """

        self.radio_style = radio_style
        self.checkbox_style = checkbox_style
        self.true_false_btn_style = true_false_btn_style

        # 当前题型（用于动态创建选项按钮）
        self.current_question_type = "single"

        # 答题状态提示
        self.answer_status_label = QLabel("")
        self.answer_status_label.setFont(QFont("Arial", 12, QFont.Weight.Medium))
        self.answer_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answer_status_label.setFixedHeight(28)
        self.answer_status_label.setStyleSheet("""
            QLabel {
                color: #5F6368;
                font-weight: 500;
            }
        """)
        self.options_layout.addWidget(self.answer_status_label)

        self.question_layout.addLayout(self.options_layout)

        # 结果区域 - 淡雅平面风格
        self.result_frame = QFrame()
        self.result_frame.setVisible(False)
        self.result_frame.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 6px;
                padding: 12px;
                border: 1px solid #E8EAED;
            }
        """)

        result_layout = QVBoxLayout(self.result_frame)
        self.result_label = QLabel()
        self.result_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.result_label.setStyleSheet("color: #3C4043; padding: 4px 0;")
        result_layout.addWidget(self.result_label)

        self.explanation_label = QLabel()
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setFont(QFont("Arial", 12))
        self.explanation_label.setStyleSheet("""
            color: #5F6368;
            padding: 10px;
            background-color: #FFFFFF;
            border-radius: 6px;
            line-height: 1.6;
            border: 1px solid #E8EAED;
        """)
        result_layout.addWidget(self.explanation_label)

        left_layout.addWidget(self.result_frame)

        # 按钮区域
        btn_widget = QWidget()
        btn_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-top: 1px solid #E8EAED;
            }
        """)
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setSpacing(10)
        btn_layout.setContentsMargins(12, 8, 12, 8)

        # 左侧按钮组
        left_btn_layout = QHBoxLayout()
        left_btn_layout.setSpacing(8)

        self.mark_btn = QPushButton("📌 标记")
        self.mark_btn.setObjectName("mark_btn")
        self.mark_btn.clicked.connect(self._toggle_mark)
        self.mark_btn.setCheckable(True)
        self.mark_btn.setMinimumHeight(36)
        self.mark_btn.setMinimumWidth(80)
        self.mark_btn.setFont(QFont("Arial", 11))
        self.mark_btn.setStyleSheet("""
            QPushButton#mark_btn {
                background-color: #F8F9FA;
                color: #5F6368;
                border: 1px solid #E8EAED;
                border-radius: 6px;
            }
            QPushButton#mark_btn:hover {
                background-color: #F1F3F4;
                border-color: #DADCE0;
            }
            QPushButton#mark_btn:checked {
                background-color: #FEF7E0;
                color: #B06000;
                border-color: #F9D884;
            }
        """)
        left_btn_layout.addWidget(self.mark_btn)

        # 错题掌握按钮
        self.mastered_btn = QPushButton("✅ 已掌握")
        self.mastered_btn.setObjectName("mastered_btn")
        self.mastered_btn.clicked.connect(self._toggle_mastered)
        self.mastered_btn.setCheckable(True)
        self.mastered_btn.setMinimumHeight(36)
        self.mastered_btn.setMinimumWidth(90)
        self.mastered_btn.setFont(QFont("Arial", 11))
        self.mastered_btn.setVisible(False)
        self.mastered_btn.setStyleSheet("""
            QPushButton#mastered_btn {
                background-color: #F8F9FA;
                color: #1E8E3E;
                border: 1px solid #E8EAED;
                border-radius: 6px;
            }
            QPushButton#mastered_btn:hover {
                background-color: #E6F4EA;
                border-color: #81C995;
            }
            QPushButton#mastered_btn:checked {
                background-color: #E6F4EA;
                color: #1E8E3E;
                border-color: #81C995;
            }
        """)
        left_btn_layout.addWidget(self.mastered_btn)
        left_btn_layout.addStretch()

        btn_layout.addLayout(left_btn_layout, 1)

        # 中间导航按钮组
        nav_btn_layout = QHBoxLayout()
        nav_btn_layout.setSpacing(8)

        self.prev_btn = QPushButton("← 上一题")
        self.prev_btn.clicked.connect(self._prev_question)
        self.prev_btn.setEnabled(False)
        self.prev_btn.setMinimumHeight(36)
        self.prev_btn.setMinimumWidth(85)
        self.prev_btn.setFont(QFont("Arial", 11))
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                color: #5F6368;
                border: 1px solid #E8EAED;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #DADCE0;
            }
            QPushButton:disabled {
                background-color: #F1F3F4;
                color: #9AA0A6;
                border-color: #E8EAED;
            }
        """)
        nav_btn_layout.addWidget(self.prev_btn)

        self.next_btn = QPushButton("下一题 →")
        self.next_btn.clicked.connect(self._next_question)
        self.next_btn.setEnabled(False)
        self.next_btn.setMinimumHeight(36)
        self.next_btn.setMinimumWidth(85)
        self.next_btn.setFont(QFont("Arial", 11))
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                color: #5F6368;
                border: 1px solid #E8EAED;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #DADCE0;
            }
            QPushButton:disabled {
                background-color: #F1F3F4;
                color: #9AA0A6;
                border-color: #E8EAED;
            }
        """)
        nav_btn_layout.addWidget(self.next_btn)

        # 查看答案按钮 - 放在导航按钮右侧
        self.show_answer_btn = QPushButton("查看答案")
        self.show_answer_btn.clicked.connect(self._show_current_answer)
        self.show_answer_btn.setMinimumHeight(36)
        self.show_answer_btn.setMinimumWidth(90)
        self.show_answer_btn.setFont(QFont("Arial", 11))
        self.show_answer_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                color: #5F6368;
                border: 1px solid #E8EAED;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
                border-color: #DADCE0;
            }
        """)
        nav_btn_layout.addWidget(self.show_answer_btn)

        btn_layout.addLayout(nav_btn_layout)

        # 右侧提交按钮组
        right_btn_layout = QHBoxLayout()
        right_btn_layout.setSpacing(10)
        right_btn_layout.addStretch()

        self.submit_all_btn = QPushButton("✓ 提交答案")
        self.submit_all_btn.setObjectName("submit_all_btn")
        self.submit_all_btn.clicked.connect(self._submit_all_answers)
        self.submit_all_btn.setMinimumHeight(36)
        self.submit_all_btn.setMinimumWidth(90)
        self.submit_all_btn.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        self.submit_all_btn.setVisible(False)
        self.submit_all_btn.setStyleSheet("""
            QPushButton#submit_all_btn {
                background-color: #1A73E8;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton#submit_all_btn:hover {
                background-color: #1557B0;
            }
        """)
        right_btn_layout.addWidget(self.submit_all_btn)

        # 返回统计按钮
        self.back_to_summary_btn = QPushButton("📊 查看结果")
        self.back_to_summary_btn.clicked.connect(self._show_summary_dialog)
        self.back_to_summary_btn.setMinimumHeight(36)
        self.back_to_summary_btn.setMinimumWidth(90)
        self.back_to_summary_btn.setFont(QFont("Arial", 11))
        self.back_to_summary_btn.setVisible(False)
        self.back_to_summary_btn.setStyleSheet("""
            QPushButton {
                background-color: #E8F0FE;
                color: #1A73E8;
                border: 1px solid #D2E3FC;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #D2E3FC;
            }
        """)
        right_btn_layout.addWidget(self.back_to_summary_btn)

        btn_layout.addLayout(right_btn_layout, 1)
        left_layout.addWidget(btn_widget)

        # 底部统计 - 简化配色
        stats_widget = QWidget()
        stats_widget.setStyleSheet("""
            QWidget {
                background-color: #FAFBFC;
                border-top: 1px solid #E1E4E8;
            }
        """)
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setContentsMargins(20, 10, 20, 10)
        stats_layout.setSpacing(32)

        # 统计卡片样式 - 统一配色
        stat_card_style = """
            QLabel {
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 6px;
                padding: 8px 16px;
            }
        """

        self.accuracy_label = QLabel("正确率：--")
        self.accuracy_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.accuracy_label.setStyleSheet(stat_card_style + "color: #3C4043;")
        stats_layout.addWidget(self.accuracy_label)

        # 用时统计已移除，避免给用户造成压力
        # self.time_label = QLabel("用时：0s")
        # self.time_label.setFont(QFont("Arial", 12))
        # self.time_label.setStyleSheet(stat_card_style + "color: #3C4043;")
        # stats_layout.addWidget(self.time_label)
        stats_layout.addStretch()
        left_layout.addWidget(stats_widget)

        main_layout.addLayout(left_layout)

        # 右侧：答题卡侧边栏
        right_widget = QWidget()
        right_widget.setMinimumWidth(180)
        right_widget.setMaximumWidth(180)
        right_widget.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-left: 1px solid #E8EAED;
            }
        """)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(2, 2, 2, 2)
        right_layout.setSpacing(2)

        # 答题卡标题
        card_title = QLabel("答题卡")
        card_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_title.setStyleSheet("""
            QLabel {
                color: #3C4043;
                padding: 8px;
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 6px;
            }
        """)
        right_layout.addWidget(card_title)

        # 图例 - 改进布局，使用网格更清晰地排列
        legend_widget = QWidget()
        legend_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 6px;
                border: 1px solid #E8EAED;
            }
        """)
        legend_layout = QGridLayout(legend_widget)
        legend_layout.setContentsMargins(8, 8, 8, 8)
        legend_layout.setSpacing(4)

        # 图例项 - 2x2网格布局
        legend_items = [
            ("未答", "#9AA0A6"),
            ("已答", "#1A73E8"),
            ("正确", "#1E8E3E"),
            ("错误", "#D93025"),
        ]
        for i, (text, color) in enumerate(legend_items):
            row = i // 2
            col = i % 2

            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(4, 4, 4, 4)
            item_layout.setSpacing(8)

            color_box = QLabel()
            color_box.setFixedSize(16, 16)
            color_box.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
            item_layout.addWidget(color_box)

            lbl = QLabel(text)
            lbl.setFont(QFont("Arial", 11))
            lbl.setStyleSheet(f"color: {color};")
            item_layout.addWidget(lbl)
            item_layout.addStretch()

            legend_layout.addWidget(item_widget, row, col)

        right_layout.addWidget(legend_widget)

        # 当前进度
        self.progress_info_label = QLabel("第 0/0 题")
        self.progress_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_info_label.setFont(QFont("Arial", 12, QFont.Weight.Medium))
        self.progress_info_label.setStyleSheet("""
            QLabel {
                color: #3C4043;
                padding: 8px;
                background-color: #FFFFFF;
                border: 1px solid #E8EAED;
                border-radius: 6px;
            }
        """)
        right_layout.addWidget(self.progress_info_label)

        # 答题卡网格
        self.answer_card_scroll = QScrollArea()
        self.answer_card_scroll.setWidgetResizable(True)
        self.answer_card_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.answer_card_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.answer_card_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #F8F9FA;
                border: none;
            }
        """)

        self.answer_card_container = QWidget()
        # 容器宽度计算：right_widget(180) - 边距 (2×2) = 176px 可用
        # 5 个按钮×30 + 4 个间距×5 + 2 边距×3 = 150+20+6 = 176px
        self.answer_card_container.setMinimumWidth(175)
        self.answer_card_container.setStyleSheet("background-color: #F8F9FA;")
        self.answer_card_layout = QGridLayout(self.answer_card_container)
        self.answer_card_layout.setSpacing(4)
        self.answer_card_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.answer_card_layout.setContentsMargins(3, 3, 3, 3)

        self.answer_card_scroll.setWidget(self.answer_card_container)
        right_layout.addWidget(self.answer_card_scroll, 1)

        main_layout.addWidget(right_widget)

        self.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.elapsed_time = 0

        # 答题卡按钮列表
        self.answer_card_buttons = []

    def _create_answer_card_button(self, index: int) -> QWidget:
        """创建答题卡按钮 - 使用 QWidget 容器确保数字完整显示"""
        from PyQt6.QtWidgets import QSizePolicy
        from PyQt6.QtCore import QEvent

        # 创建容器 widget
        container = QWidget()
        container.setFixedSize(30, 30)
        container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        container.setProperty("status", "none")

        # 创建布局
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建标签显示序号（连续编号）
        question = self.questions[index] if self.questions else None
        serial = question.serial_number if question and question.serial_number else (index + 1)
        self.label = QLabel(f"{serial}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 10))
        self.label.setCursor(Qt.CursorShape.PointingHandCursor)

        # 如果是标记题目，添加 📌 标识
        is_marked = question.id in self.marked_questions if question else False
        if is_marked:
            self.label.setText(f"{serial}📌")

        # 默认样式
        self._apply_card_button_style(self.label, "none")

        container.mousePressEvent = lambda e: self._on_card_button_clicked(index)

        # 存储 label 以便后续更新状态
        container.label = self.label
        container.index = index

        layout.addWidget(self.label)
        return container

    def _apply_card_button_style(self, label: QLabel, status: str):
        """应用答题卡按钮样式"""
        styles = {
            "none": "background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 4px; color: #5F6368;",
            "hover": "background-color: #E8F0FE; border: 1px solid #1A73E8; border-radius: 4px; color: #1A73E8;",
            "answered": "background-color: #E8F0FE; border: 1px solid #1A73E8; border-radius: 4px; color: #1A73E8; font-weight: bold;",
            "correct": "background-color: #E6F4EA; border: 1px solid #1E8E3E; border-radius: 4px; color: #1E8E3E; font-weight: bold;",
            "wrong": "background-color: #FCE8E6; border: 1px solid #D93025; border-radius: 4px; color: #D93025; font-weight: bold;",
        }
        label.setStyleSheet(styles.get(status, styles["none"]))

    def _on_card_button_clicked(self, index: int):
        """点击答题卡"""
        if 0 <= index < len(self.questions):
            self.current_index = index
            self._show_question(self.current_index)

    def _show_true_false_buttons(self):
        """显示判断题按钮 - 现代化版"""
        self.option_buttons = []

        # 正确按钮
        true_btn = QPushButton("✓ 正确")
        true_btn.setObjectName("true_btn")
        true_btn.setStyleSheet(self.true_false_btn_style)
        true_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        true_btn.setCheckable(True)
        true_btn.clicked.connect(self._on_option_clicked)
        self.option_buttons.append(true_btn)
        self.options_layout.addWidget(true_btn)

        # 错误按钮
        false_btn = QPushButton("✗ 错误")
        false_btn.setObjectName("false_btn")
        false_btn.setStyleSheet(self.true_false_btn_style)
        false_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        false_btn.setCheckable(True)
        false_btn.clicked.connect(self._on_option_clicked)
        self.option_buttons.append(false_btn)
        self.options_layout.addWidget(false_btn)

    def _show_fill_input(self):
        """显示填空题输入框"""
        from PyQt6.QtWidgets import QTextEdit

        self.option_buttons = []

        # 创建输入框容器
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 4, 0, 0)
        input_layout.setSpacing(8)

        # 标签
        label = QLabel("你的答案：")
        label.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        label.setStyleSheet("color: #5f6368; padding: 4px 0;")
        input_layout.addWidget(label)

        # 文本输入框
        self.fill_input = QTextEdit()
        self.fill_input.setObjectName("fill_input")
        self.fill_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E8EAED;
                border-radius: 8px;
                padding: 12px;
                background-color: #FFFFFF;
                font-size: 14px;
                min-height: 100px;
                color: #3c4043;
            }
            QTextEdit:focus {
                border-color: #1a73e8;
            }
        """)
        self.fill_input.setPlaceholderText("在此输入答案...")
        self.fill_input.textChanged.connect(self._on_fill_text_changed)
        input_layout.addWidget(self.fill_input)

        self.options_layout.addWidget(input_container)
        self.option_buttons.append(input_container)

    def _update_answer_card(self):
        """更新答题卡显示"""
        # 清除现有按钮
        for i in reversed(range(self.answer_card_layout.count())):
            widget = self.answer_card_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.answer_card_buttons.clear()

        # 更新进度信息（显示序号范围）
        if self.questions:
            start_serial = self.questions[0].serial_number or 1
            end_serial = self.questions[-1].serial_number or len(self.questions)
            current_serial = self.questions[self.current_index].serial_number or (self.current_index + 1)
            self.progress_info_label.setText(f"第 {current_serial} 题 (共 {start_serial}-{end_serial})")
        else:
            self.progress_info_label.setText("第 0/0 题")

        # 创建新按钮
        for idx in range(len(self.questions)):
            btn = self._create_answer_card_button(idx)
            question = self.questions[idx]
            serial = question.serial_number or (idx + 1)
            question_id = question.id

            # 设置状态
            if self.session_submitted:
                if idx in self.answer_results:
                    if self.answer_results[idx]:
                        self._apply_card_button_style(btn.label, "correct")
                        btn.setToolTip(f"第{serial}题：正确")
                    else:
                        self._apply_card_button_style(btn.label, "wrong")
                        btn.setToolTip(f"第{serial}题：错误")
                else:
                    btn.setToolTip(f"第{serial}题：未作答")
            elif idx in self.user_answers:
                self._apply_card_button_style(btn.label, "answered")
                btn.setToolTip(f"第{serial}题：已选择 {self.user_answers[idx]}")
            else:
                btn.setToolTip(f"第{serial}题：未作答")

            # 高亮当前题目
            if idx == self.current_index:
                btn.label.setStyleSheet("""
                    background-color: #E8F0FE;
                    border: 2px solid #1A73E8;
                    border-radius: 4px;
                    color: #1A73E8;
                    font-weight: bold;
                """)

            self.answer_card_buttons.append(btn)
            self.answer_card_layout.addWidget(btn, idx // 5, idx % 5)
    
    def _setup_shortcuts(self):
        """设置键盘快捷键"""
        pass  # 使用 handle_key_event 方法处理快捷键

    def keyPressEvent(self, event):
        """键盘按键事件处理"""
        self.handle_key_event(event)

    def handle_key_event(self, event):
        key = event.key()
        modifier = event.modifiers()

        # 快捷键：Ctrl+S 编辑当前题目
        if modifier == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_S:
            if self.current_question:
                self._edit_current_question()
            return

        # 快捷键：Ctrl+D 删除当前题目
        if modifier == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_D:
            if self.current_question:
                self._delete_current_question()
            return

        # 快捷键：Ctrl+Enter 提交答案
        if modifier == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Return:
            if self.submit_all_btn.isVisible() and self.submit_all_btn.isEnabled():
                self._submit_all_answers()
            return

        # 数字键 1-6 选择选项 A-F
        if Qt.Key.Key_1 <= key <= Qt.Key.Key_6:
            opt_index = key - Qt.Key.Key_1
            if opt_index < len(self.option_buttons) and self.option_buttons[opt_index].isVisible():
                self.option_buttons[opt_index].setChecked(True)
                self._on_option_clicked()
            return

        # 方向键：→ 下一题
        if key == Qt.Key.Key_Right:
            if self.next_btn.isEnabled():
                self._next_question()
            return

        # 方向键：← 上一题
        if key == Qt.Key.Key_Left:
            if self.prev_btn.isEnabled():
                self._prev_question()
            return

        # Enter 键：提交答案（如果在练习中）或 下一题
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            if self.submit_all_btn.isVisible() and self.submit_all_btn.isEnabled():
                # Shift+Enter 提交，Enter 下一题
                if modifier == Qt.KeyboardModifier.ShiftModifier:
                    self._submit_all_answers()
                elif self.next_btn.isEnabled():
                    self._next_question()
            elif self.session_submitted and self.next_btn.isEnabled():
                self._next_question()
            return

        # 空格键：标记/取消标记
        if key == Qt.Key.Key_Space:
            if self.current_question and not self.session_submitted:
                self._toggle_mark()
            return

    def load_questions(self, category_id=None, category_name=None):
        """加载题目列表 - 支持分页和题型过滤"""
        try:
            import random

            # 保存当前分类信息
            self.current_category_id = category_id
            self.current_category_name = category_name

            # 错题模式下不受分页和题型过滤限制
            if self.practice_mode == 'wrong':
                self.questions = self.practice_service.get_wrong_questions(limit=1000)
                self.all_questions = self.questions
                self.current_offset = 0
            else:
                # 根据分类名称确定题型过滤
                question_type_filter = None
                if category_name:
                    # 去除图标和空格
                    clean_name = category_name.replace('📚', '').replace('📖', '').strip()
                    if '单选' in clean_name:
                        question_type_filter = '单选'
                    elif '多选' in clean_name:
                        question_type_filter = '多选'
                    elif '判断' in clean_name:
                        question_type_filter = '判断'
                    elif '填空' in clean_name:
                        question_type_filter = '填空'
                    # "全部题目"不过滤

                # 获取所有题目（按分类或全部），附带连续编号
                if category_id:
                    self.all_questions = self.question_service.get_questions_with_serial(
                        category_id, question_type_filter
                    )
                else:
                    # 全部题目模式：不过滤题型，但按题型分组编号
                    self.all_questions = self.question_service.get_questions_with_serial(
                        None, None
                    )

                # 随机模式：打乱题目顺序（过滤后）
                if self.practice_mode == 'random':
                    random.shuffle(self.all_questions)
                    # 重新编号（随机后不保持连续编号，使用索引 +1）
                    for idx, q in enumerate(self.all_questions, start=1):
                        q.serial_number = idx

                # 根据设置决定起始位置（支持自定义起始题号，按题型区分）
                start_type_map = {
                    '单选': 'start_from_question_single',
                    '多选': 'start_from_question_multi',
                    '判断': 'start_from_question_judge',
                    '填空': 'start_from_question_fill',
                }
                start_key = start_type_map.get(question_type_filter, 'start_from_question_single')
                start_from = self.settings.get(start_key, 1)
                if start_from > 1 and start_from <= len(self.all_questions):
                    self.current_offset = start_from - 1
                else:
                    self.current_offset = 0

                # 截取当前批次
                end_index = min(self.current_offset + self.questions_per_session, len(self.all_questions))
                self.questions = self.all_questions[self.current_offset:end_index]

            # 重置状态
            self.current_index = 0
            self.user_answers = {}
            self.answer_results = {}
            self.elapsed_time = 0
            self.session_submitted = False

            # 更新 UI
            self._update_answer_card()

            # 清空当前显示
            self._clear_question_area()

            # 重置按钮状态 - 不自动开始，等待用户点击
            self.start_btn.setText("▶ 开始练习")
            self.submit_all_btn.setVisible(False)
            self.back_to_summary_btn.setVisible(False)
            self.show_answer_btn.setVisible(False)
            self.progress_info_label.setText("第 0/0 题")

        except Exception as e:
            print(f"加载题目失败：{e}")
            import traceback
            traceback.print_exc()

    def _get_question_type_aliases(self, question_type: str) -> list:
        """获取题型别名列表（已废弃，保留兼容）"""
        return [question_type]

    def _clear_question_area(self):
        """清空题目显示区域"""
        self.question_label.clear()
        for item in self.option_buttons:
            # 处理元组结构：(btn, container, text_label)
            if isinstance(item, tuple):
                container = item[1]
            else:
                container = item
            container.deleteLater()
        self.option_buttons.clear()

    # 搜索文本属性（由主窗口设置）
    search_text = ''

    def _set_mode(self, mode):
        """切换练习模式"""
        self.practice_mode = mode
        for m, btn in self.mode_btns.items():
            btn.setChecked(m == mode)

        # 错题模式下显示"已掌握"按钮
        is_wrong_mode = (mode == 'wrong')
        self.mastered_btn.setVisible(is_wrong_mode)

        # 使用保存的分类信息加载题目
        self.load_questions(self.current_category_id, self.current_category_name)
    
    def _start_practice(self):
        """开始练习 - 支持分页"""
        if not self.questions:
            return

        # 检查是否已答题，如果有则显示确认对话框
        if self.user_answers:
            confirmed = self._show_confirmation_dialog(
                "确认重新开始",
                f"当前已有 {len(self.user_answers)} 道题的答案，重新开始将清空所有进度。\n\n确定要重新开始吗？"
            )

            if not confirmed:
                return

        self._start_practice_internal()

    def _start_practice_internal(self):
        """内部开始练习方法（无确认）"""
        try:
            self.current_index = 0
            self.user_answers = {}
            self.answer_results = {}
            # 注意：不要清空 marked_questions，因为它是持久化的
            self.elapsed_time = 0
            self.session_submitted = False

            parent = self.parent()
            category_id = None
            if parent and hasattr(parent, "current_category_id"):
                category_id = parent.current_category_id

            # 计算全局起始题号
            global_start = self.current_offset + 1
            global_end = min(self.current_offset + len(self.questions), len(self.all_questions) if self.all_questions else len(self.questions))

            self.current_session_id = self.practice_service.create_session(
                self.practice_mode,
                category_id,
                global_end - global_start + 1
            )

            self.timer.start(1000)
            self._show_question(self.current_index)
            self.start_btn.setText("🔄 重新开始")
            self.submit_all_btn.setVisible(True)
            self.back_to_summary_btn.setVisible(False)
            self.show_answer_btn.setVisible(True)
        except Exception as e:
            print(f"开始练习失败：{e}")
            import traceback
            traceback.print_exc()
    
    def _show_question(self, index):
        if index < 0 or index >= len(self.questions):
            return

        self.current_question = self.questions[index]
        # 显示序号（连续编号）和题目内容
        serial = self.current_question.serial_number or (index + 1)
        self.question_label.setText(f"<b>[{serial}]</b> {self.current_question.question_text}")

        # 根据题型创建选项按钮
        question_type = self.current_question.question_type
        self.current_question_type = question_type

        # 清除旧的选项按钮
        for item in self.option_buttons:
            if isinstance(item, tuple):
                btn = item[0]  # 第一个元素是按钮
                container = item[1]  # 第二个元素是容器
                btn.deleteLater()
                container.deleteLater()
            else:
                item.deleteLater()
        self.option_buttons.clear()

        options = self.current_question.options

        # 根据题型创建对应的按钮 - 支持中文和英文值
        is_multi = question_type in ('multi', '多选')
        is_true_false = question_type in ('true_false', '判断题')
        is_fill = question_type in ('fill', '填空题')

        # 判断题特殊处理
        if is_true_false:
            self._show_true_false_buttons()
        # 填空题特殊处理
        elif is_fill:
            self._show_fill_input()
        # 单选题/多选题处理 - 使用 QWidget 容器+QLabel 实现自动换行
        else:
            self.option_buttons = []  # 存储 (button, container, letter) 元组

            for i, opt_letter in enumerate(["A", "B", "C", "D", "E", "F"]):
                if opt_letter not in options:
                    continue

                # 创建容器
                container = QWidget()
                container.setObjectName(f"option_container_{opt_letter}")
                container.setCursor(Qt.CursorShape.PointingHandCursor)
                container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

                container_layout = QHBoxLayout(container)
                container_layout.setContentsMargins(14, 10, 14, 10)
                container_layout.setSpacing(10)

                # 选项字母标签 (A. B. 等)
                letter_label = QLabel(f"{opt_letter}.")
                letter_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
                letter_label.setStyleSheet("color: #3C4043; border: none; background: transparent;")
                letter_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                letter_label.setMinimumWidth(28)
                container_layout.addWidget(letter_label)

                # 选项内容标签（支持自动换行）
                text_label = QLabel(options[opt_letter])
                text_label.setFont(QFont("Arial", 17))
                text_label.setWordWrap(True)  # 启用自动换行
                text_label.setStyleSheet("color: #3C4043; padding: 4px 0; border: none; background: transparent;")
                text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                text_label.setCursor(Qt.CursorShape.PointingHandCursor)
                container_layout.addWidget(text_label, 1)

                # 隐藏的 RadioButton 用于状态跟踪
                btn = QRadioButton()
                btn.setVisible(False)
                btn.clicked.connect(self._on_option_clicked)

                # 容器基础样式 - 带边框
                container.setStyleSheet(
                    "background-color: #FFFFFF; "
                    "border: 1px solid #DADCE0; "
                    "border-radius: 8px; "
                    "min-height: 44px;"
                )

                # 点击容器切换选中状态
                def on_container_click(event, b=btn, c=container):
                    new_state = not b.isChecked()
                    b.setChecked(new_state)
                    # 更新样式
                    if new_state:
                        c.setStyleSheet(
                            "background-color: #E8F0FE; "
                            "border: 2px solid #1A73E8; "
                            "border-radius: 8px; "
                            "min-height: 44px;"
                        )
                    else:
                        c.setStyleSheet(
                            "background-color: #FFFFFF; "
                            "border: 1px solid #DADCE0; "
                            "border-radius: 8px; "
                            "min-height: 44px;"
                        )
                    self._on_option_clicked()

                container.mousePressEvent = on_container_click
                text_label.mousePressEvent = lambda event, b=btn, c=container: on_container_click(None, b=b, c=c)

                self.option_buttons.append((btn, container, opt_letter))
                self.options_layout.addWidget(container)

            # 单选题需要加入 ButtonGroup 实现互斥
            if not is_multi:
                for btn, container, letter in self.option_buttons:
                    self.option_group.addButton(btn)

        # 恢复之前的选择
        if index in self.user_answers:
            selected = self.user_answers[index]
            is_true_false = self.current_question_type in ('true_false', '判断题')
            is_fill = self.current_question_type in ('fill', '填空题')

            if is_multi and isinstance(selected, list):
                # 多选题答案
                for btn, container, letter in self.option_buttons:
                    if letter in selected:
                        btn.setChecked(True)
                        container.setStyleSheet(
                            "background-color: #E8F0FE; "
                            "border: 2px solid #1A73E8; "
                            "border-radius: 8px; "
                            "min-height: 50px;"
                        )
            elif is_true_false:
                # 判断题答案：A=正确，B=错误
                btn_index = 0 if selected == "A" else 1
                if 0 <= btn_index < len(self.option_buttons):
                    self.option_buttons[btn_index][0].setChecked(True)
            elif is_fill:
                # 填空题答案
                if hasattr(self, 'fill_input'):
                    self.fill_input.setText(selected)
            else:
                # 单选题答案
                for btn, container, letter in self.option_buttons:
                    if letter == selected:
                        btn.setChecked(True)
                        container.setStyleSheet(
                            "background-color: #E8F0FE; "
                            "border: 2px solid #1A73E8; "
                            "border-radius: 8px; "
                            "min-height: 50px;"
                        )
                        break

            if self.session_submitted:
                is_correct = self.answer_results.get(index, False)
                if is_correct:
                    self.answer_status_label.setText("✓ 回答正确")
                    self.answer_status_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
                else:
                    correct = self.current_question.answer.upper()
                    self.answer_status_label.setText(f"✗ 正确答案：{correct}")
                    self.answer_status_label.setStyleSheet("color: #c62828; font-weight: bold;")
            else:
                ans_text = selected if isinstance(selected, str) else ','.join(selected)
                self.answer_status_label.setText(f"已选择 {ans_text}")
                self.answer_status_label.setStyleSheet("color: #1976d2;")
        else:
            # 错题模式：只显示上次答案，不显示正确答案
            if self.practice_mode == 'wrong' and self.current_question:
                last_record = self.practice_service.get_question_record(self.current_question.id)
                if last_record and last_record.user_answer:
                    self.answer_status_label.setText(f"上次答案：{last_record.user_answer}")
                    self.answer_status_label.setStyleSheet("color: #5F6368; font-weight: 500;")
                else:
                    self.answer_status_label.setText("")
            else:
                self.answer_status_label.setText("")

        is_marked = self.current_question.id in self.marked_questions
        self.mark_btn.setChecked(is_marked)
        self.mark_btn.setText("已标记" if is_marked else "标记")

        # 更新已掌握按钮状态（错题模式）
        if self.practice_mode == 'wrong':
            is_mastered = self._is_question_mastered(self.current_question.id)
            self.mastered_btn.setChecked(is_mastered)
            self.mastered_btn.setText("✅ 已掌握" if is_mastered else "✅ 标记")

        if not self.session_submitted:
            self.result_frame.setVisible(False)

        self.prev_btn.setEnabled(index > 0)
        is_last = index >= len(self.questions) - 1
        self.next_btn.setEnabled(not is_last)

        self._update_progress()
        self._update_answer_card()
    
    def _update_progress(self):
        """更新进度 - 已通过答题卡显示"""
        answered = len(self.user_answers)
        if self.current_question:
            serial = self.current_question.serial_number or (self.current_index + 1)
            self.progress_info_label.setText(f"第 {serial} 题")
        else:
            self.progress_info_label.setText(f"第 0/{len(self.questions)} 题")

    def _edit_current_question(self):
        """编辑当前题目"""
        if not self.current_question:
            return

        from ui.dialogs import QuestionDialog
        categories = self.question_service.get_all_categories()
        dialog = QuestionDialog(self, question=self.current_question, categories=categories)

        if dialog.exec():
            question = dialog.get_question()
            if question:
                self.question_service.update_question(question)
                self.statusbar.showMessage("题目已更新")
                # 刷新题目列表
                parent = self.parent()
                category_id = None
                if parent and hasattr(parent, "current_category_id"):
                    category_id = parent.current_category_id
                self.load_questions(category_id)

    def _delete_current_question(self):
        """删除当前题目"""
        if not self.current_question:
            return

        reply = self._show_confirmation_dialog(
            "确认删除",
            "确定要删除这道题吗？"
        )

        if reply:
            self.question_service.delete_question(self.current_question.id)
            # 从列表中移除
            self.questions.pop(self.current_index)
            # 刷新显示
            if self.questions:
                self.current_index = min(self.current_index, len(self.questions) - 1)
                self._show_question(self.current_index)
            else:
                self.question_label.clear()
                for btn in self.option_buttons:
                    btn.setVisible(False)
                self.prev_btn.setEnabled(False)
                self.next_btn.setEnabled(False)
                self.progress_text_label.setText("暂无题目")
            # 更新答题卡
            self._update_answer_card()

    def _on_option_clicked(self):
        """选项点击处理"""
        if not self.current_question or self.session_submitted:
            return

        # 支持中文和英文的题型值
        is_multi = self.current_question_type in ('multi', '多选')
        is_true_false = self.current_question_type in ('true_false', '判断题')
        is_fill = self.current_question_type in ('fill', '填空题')

        # 填空题不需要此方法处理（由 textChanged 信号处理）
        if is_fill:
            return

        if is_multi:
            # 多选题：收集所有选中的选项
            selected_options = []
            for btn, container, letter in self.option_buttons:
                if btn.isChecked():
                    selected_options.append(letter)

            if selected_options:
                self.user_answers[self.current_index] = selected_options
                ans_text = ','.join(selected_options)
                self.answer_status_label.setText(f"已选择 {ans_text}")
                self.answer_status_label.setStyleSheet("color: #1976d2;")
            else:
                # 没有选中任何选项
                if self.current_index in self.user_answers:
                    del self.user_answers[self.current_index]
                self.answer_status_label.setText("")
        elif is_true_false:
            # 判断题处理 - 直接使用按钮
            selected_letter = None
            for i, btn in enumerate(self.option_buttons):
                if btn.isChecked():
                    # 清除其他按钮的选中状态
                    for j, other_btn in enumerate(self.option_buttons):
                        if i != j:
                            other_btn.setChecked(False)
                    selected_letter = "A" if i == 0 else "B"  # A=正确，B=错误
                    btn.setChecked(True)
                    break

            if selected_letter:
                self.user_answers[self.current_index] = selected_letter
                ans_text = "正确" if selected_letter == "A" else "错误"
                self.answer_status_label.setText(f"已选择 {ans_text}")
                self.answer_status_label.setStyleSheet("color: #1976d2;")
        else:
            # 单选题 - 从按钮获取选中的选项
            selected_letter = None
            for btn, container, letter in self.option_buttons:
                if btn.isChecked():
                    selected_letter = letter
                    break

            if not selected_letter:
                return

            # 只保存选择，不显示答案
            self.user_answers[self.current_index] = selected_letter
            self.answer_status_label.setText(f"已选择 {selected_letter}")
            self.answer_status_label.setStyleSheet("color: #1976d2;")

        self._update_progress()
        self._update_answer_card()

        # 自动下一题功能 - 多选题不自动跳转（需要时间选择多个选项）
        if self.auto_next and not self.session_submitted and not is_multi:
            QTimer.singleShot(self.auto_next_delay, self._next_question)

    def _on_fill_text_changed(self):
        """填空题文本变化处理"""
        if not self.current_question or self.session_submitted:
            return

        if hasattr(self, 'fill_input'):
            text = self.fill_input.toPlainText().strip()
            if text:
                self.user_answers[self.current_index] = text
                self.answer_status_label.setText(f"已输入 {len(text)} 字符")
                self.answer_status_label.setStyleSheet("color: #1976d2;")
            else:
                if self.current_index in self.user_answers:
                    del self.user_answers[self.current_index]
                self.answer_status_label.setText("")

        self._update_progress()
        self._update_answer_card()
    
    def _submit_all_answers(self):
        """统一提交所有答案"""
        if not self.questions or self.session_submitted:
            return

        # 检查是否全部作答
        unanswered = [i+1 for i in range(len(self.questions)) if i not in self.user_answers]

        if unanswered:
            message = f"你还有 {len(unanswered)} 道题未作答，确定要提交吗？"
        else:
            message = "所有题目已作答，确定提交？"

        confirmed = self._show_confirmation_dialog("确认提交", message)

        if confirmed:
            self._do_submit_all()
    
    def _do_submit_all(self):
        """执行统一提交"""
        correct_count = 0
        wrong_count = 0

        for idx, question in enumerate(self.questions):
            if idx in self.user_answers:
                user_answer = self.user_answers[idx]
                correct_answer = question.answer.upper()

                # 判断答案是否正确 - 支持中文和英文值
                is_multi = question.question_type in ('multi', '多选')

                if is_multi:
                    # 多选题：用户答案可能是列表或逗号分隔的字符串
                    if isinstance(user_answer, list):
                        user_ans_set = set([a.upper() for a in user_answer])
                    else:
                        user_ans_set = set([a.strip().upper() for a in user_answer.replace(',', ',').split(',')])

                    # 正确答案集合
                    correct_set = set([a.strip().upper() for a in correct_answer.replace(',', ',').split(',')])

                    # 完全匹配才算正确
                    is_correct = user_ans_set == correct_set
                else:
                    # 单选题
                    if isinstance(user_answer, list):
                        user_answer = user_answer[0] if user_answer else ''
                    is_correct = str(user_answer).upper() in correct_answer.upper()

                self.answer_results[idx] = is_correct

                # 记录到数据库
                ans_str = ','.join(user_answer) if isinstance(user_answer, list) else user_answer
                self.practice_service.record_answer(
                    question.id,
                    ans_str,
                    is_correct,
                    self.elapsed_time,
                    self.current_session_id,
                    question.id in self.marked_questions
                )

                if is_correct:
                    correct_count += 1
                else:
                    wrong_count += 1

        self.session_submitted = True
        self.practice_service.complete_session(self.current_session_id)

        # 保存进度
        self._save_progress()

        # 显示汇总对话框
        self._show_summary_dialog()

        # 更新按钮显示
        self.submit_all_btn.setVisible(False)
        self.back_to_summary_btn.setVisible(True)
        self.show_answer_btn.setVisible(False)

        # 更新当前题目显示
        self._show_question(self.current_index)
    
    def _show_summary_dialog(self):
        """显示汇总对话框"""
        if not self.answer_results:
            return
        
        dialog = ResultSummaryDialog(
            self,
            self.questions,
            self.user_answers,
            self.answer_results
        )
        dialog.question_clicked.connect(self._on_result_question_clicked)
        dialog.exec()
    
    def _on_result_question_clicked(self, index):
        """从汇总对话框点击题号"""
        self.current_index = index
        self._show_question(index)

        # 显示该题的解析
        question = self.questions[index]

        # 检查是否已作答
        if index in self.user_answers:
            # 已作答：显示正确/错误状态
            if index in self.answer_results:
                is_correct = self.answer_results[index]

                if is_correct:
                    self.result_label.setText("✅ 回答正确！")
                    self.result_label.setStyleSheet("color: #2e7d32; font-size: 16px;")
                else:
                    correct = question.answer.upper()
                    self.result_label.setText(f"❌ 回答错误！正确答案：{correct}")
                    self.result_label.setStyleSheet("color: #c62828; font-size: 16px;")
            else:
                # 已作答但未提交（理论上不应该发生）
                self.result_label.setText("⚠️ 已作答但未提交")
                self.result_label.setStyleSheet("color: #F9AB00; font-size: 16px;")
        else:
            # 未作答：显示"未作答"状态
            self.result_label.setText(f"⚪ 未作答 | 正确答案：{question.answer.upper()}")
            self.result_label.setStyleSheet("color: #5F6368; font-size: 16px;")

        # 显示解析
        if question.explanation:
            self.explanation_label.setText(f"<b>解析：</b>{question.explanation}")
            self.explanation_label.setVisible(True)
        else:
            self.explanation_label.setVisible(False)

        self.result_frame.setVisible(True)
    
    def _show_info_dialog(self, title: str, message: str):
        """显示信息对话框 - 使用 QDialog 代替 QMessageBox 避免 Windows 闪烁"""
        from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 消息标签
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("padding: 10px; font-size: 14px; color: #3C4043;")
        layout.addWidget(msg_label)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # 确定按钮
        ok_btn = QPushButton("确定")
        ok_btn.setFixedSize(100, 36)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)
        dialog.exec()

    def _next_question(self):
        """下一题 - 支持加载下一批次"""
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self._show_question(self.current_index)
        elif self.practice_mode != 'wrong' and self.all_questions:
            # 到达当前批次末尾，检查是否有下一批
            next_offset = self.current_offset + len(self.questions)
            if next_offset < len(self.all_questions):
                # 加载下一批
                self._load_next_batch(next_offset)
            else:
                # 已经是最后一题
                self._show_info_dialog("提示", "已经是最后一题了，点击提交答案结束练习")

    def _load_next_batch(self, offset: int):
        """加载下一批题目"""
        try:
            self.current_offset = offset
            end_index = min(offset + self.questions_per_session, len(self.all_questions))
            self.questions = self.all_questions[offset:end_index]

            # 重置状态
            self.current_index = 0
            self.user_answers = {}
            self.answer_results = {}

            # 更新 UI
            self._update_answer_card()

            # 显示当前题目
            self._show_question(0)

            # 保存进度
            self._save_progress()

        except Exception as e:
            print(f"加载下一批题目失败：{e}")
    
    def _prev_question(self):
        """上一题 - 支持加载上一批次"""
        if self.current_index > 0:
            self.current_index -= 1
            self._show_question(self.current_index)
        elif self.practice_mode != 'wrong' and self.current_offset > 0:
            # 在第一题且不是第一批，加载上一批
            prev_offset = max(0, self.current_offset - self.questions_per_session)
            self._load_prev_batch(prev_offset)

    def _load_prev_batch(self, offset: int):
        """加载上一批题目"""
        try:
            self.current_offset = offset
            end_index = offset + self.questions_per_session
            self.questions = self.all_questions[offset:end_index]

            # 重置状态
            self.current_index = len(self.questions) - 1
            self.user_answers = {}
            self.answer_results = {}

            # 更新 UI
            self._update_answer_card()

            # 显示当前题目
            self._show_question(self.current_index)

        except Exception as e:
            print(f"加载上一批题目失败：{e}")
    
    def _jump_to_question(self):
        """跳转到指定题号（全局题号）"""
        try:
            num = int(self.jump_input.text())
            total = len(self.all_questions) if self.practice_mode != 'wrong' else len(self.questions)
            if 1 <= num <= total:
                # 计算目标题号在哪一批次
                batch_index = (num - 1) // self.questions_per_session
                target_offset = batch_index * self.questions_per_session
                target_index = (num - 1) % self.questions_per_session

                # 如果需要加载新的批次
                if target_offset != self.current_offset:
                    self.current_offset = target_offset
                    end_index = min(target_offset + self.questions_per_session, len(self.all_questions))
                    self.questions = self.all_questions[target_offset:end_index]
                    self._update_answer_card()

                self.current_index = target_index
                self._show_question(self.current_index)
                self.jump_input.clear()
            else:
                self.jump_input.clear()
        except ValueError:
            self.jump_input.clear()
    
    def _toggle_mark(self):
        """切换题目标记状态"""
        if self.current_question:
            q_id = self.current_question.id
            if q_id in self.marked_questions:
                # 取消标记
                self.marked_questions.remove(q_id)
                self.mark_btn.setText("📌 标记")
                # 更新数据库
                try:
                    self.practice_service.update_question_mark(q_id, False)
                except Exception as e:
                    print(f"取消标记失败：{e}")
            else:
                # 添加标记
                self.marked_questions.add(q_id)
                self.mark_btn.setText("📌 已标记")
                # 更新数据库
                try:
                    self.practice_service.update_question_mark(q_id, True)
                except Exception as e:
                    print(f"添加标记失败：{e}")

            # 更新答题卡显示
            self._update_answer_card()

    def _show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self, self.settings)
        if dialog.exec():
            new_settings = dialog.get_settings()
            self.settings = new_settings
            self._save_settings(new_settings)
            # 应用设置
            self.auto_next = new_settings.get('auto_next', False)
            self.auto_next_delay = new_settings.get('auto_next_delay', 500)
            self.questions_per_session = new_settings.get('questions_per_session', 50)
            self.continue_last_session = new_settings.get('continue_last_session', False)

    def _toggle_mastered(self):
        """切换题目掌握状态（错题本）"""
        if self.current_question:
            q_id = self.current_question.id
            is_mastered = self._is_question_mastered(q_id)

            if is_mastered:
                # 取消已掌握标记
                self.mastered_btn.setText('✅ 标记')
                self.mastered_btn.setChecked(False)
            else:
                # 标记为已掌握
                self.mastered_btn.setChecked(True)
                self.mastered_btn.setText('✅ 已掌握')

            # 更新数据库
            try:
                self.practice_service.mark_question_as_mastered(q_id)
            except Exception as e:
                print(f'更新掌握状态失败：{e}')

    def _is_question_mastered(self, question_id: int) -> bool:
        """检查题目是否已掌握"""
        try:
            row = self.practice_service.db.fetchone(
                'SELECT mastered FROM wrong_questions WHERE question_id = ?',
                (question_id,)
            )
            return bool(row['mastered']) if row else False
        except Exception as e:
            print(f'检查掌握状态失败：{e}')
            return False

    def _show_confirmation_dialog(self, title: str, message: str) -> bool:
        """显示确认对话框 - 使用 QDialog 代替 QMessageBox 避免 Windows 闪烁"""
        from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
        from PyQt6.QtCore import Qt

        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 消息标签
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("padding: 10px; font-size: 14px; color: #3C4043;")
        layout.addWidget(msg_label)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(100, 36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                color: #5F6368;
                border: 1px solid #DADCE0;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #F1F3F4;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        # 确认按钮
        confirm_btn = QPushButton("确定")
        confirm_btn.setFixedSize(100, 36)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        confirm_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(confirm_btn)

        layout.addLayout(btn_layout)

        return dialog.exec() == QDialog.DialogCode.Accepted

    def _show_current_answer(self):
        """显示当前题目答案 - 使用 QDialog 避免 Windows 弹窗闪烁"""
        if not self.current_question:
            return

        from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
        from PyQt6.QtCore import Qt

        serial = self.current_question.serial_number or (self.current_index + 1)
        answer = self.current_question.answer.upper()
        explanation = self.current_question.explanation or "无解析"

        # 使用 QDialog 代替 QMessageBox 避免闪烁
        dialog = QDialog(self)
        dialog.setWindowTitle(f"第{serial}题 答案")
        dialog.setMinimumSize(400, 200)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 答案标签
        answer_label = QLabel(f"<b style='font-size: 15px; color: #1A73E8;'>正确答案：{answer}</b>")
        answer_label.setStyleSheet("padding: 10px; background-color: #E8F0FE; border-radius: 6px;")
        layout.addWidget(answer_label)

        # 解析标签
        explanation_label = QLabel(f"<b style='font-size: 14px;'>解析：</b><span style='font-size: 13px; color: #5F6368;'>{explanation}</span>")
        explanation_label.setWordWrap(True)
        explanation_label.setStyleSheet("padding: 10px; line-height: 1.6;")
        layout.addWidget(explanation_label)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setFixedSize(100, 36)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A73E8;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1557B0;
            }
        """)
        close_btn.clicked.connect(dialog.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        dialog.exec()

    def _is_question_mastered(self, question_id: int) -> bool:
        """检查题目是否已掌握"""
        try:
            row = self.practice_service.db.fetchone(
                'SELECT mastered FROM wrong_questions WHERE question_id = ?',
                (question_id,)
            )
            return row is not None and bool(row['mastered'])
        except Exception as e:
            print(f'检查掌握状态失败：{e}')
            return False

    def _update_time(self):
        # 用时统计已移除，避免给用户造成压力
        pass

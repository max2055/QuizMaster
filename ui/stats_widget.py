"""
统计组件 - 显示练习统计信息
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QFrame, QScrollArea, QProgressBar, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from services.practice_service import PracticeService


class StatsWidget(QWidget):
    """统计组件"""
    
    def __init__(self, practice_service: PracticeService):
        super().__init__()
        
        self.practice_service = practice_service
        self.stat_cards = {}  # 初始化统计卡片字典
        
        self._init_ui()
        self.load_stats()
    
    def _init_ui(self):
        """初始化界面"""
        # 设置组件背景色为白色
        self.setStyleSheet("background-color: #FFFFFF;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background-color: #FFFFFF; border: none;")

        container = QWidget()
        container.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(container)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title = QLabel("📊 练习统计")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3C4043; padding: 10px 0;")
        layout.addWidget(title)

        # 总体统计卡片
        layout.addWidget(self._create_section_title("📈 总体统计"))

        self.overall_grid = QGridLayout()
        self.overall_grid.setSpacing(20)
        self.overall_grid.setContentsMargins(10, 10, 10, 10)

        # 统计卡片配置 - 使用 Google Material Design 配色
        stats_config = [
            ('total_questions', '📚 总题量', '#1A73E8', '#E8F0FE'),
            ('practiced_questions', '✏️ 已练习', '#1E8E3E', '#E6F4EA'),
            ('accuracy', '🎯 正确率', '#F9AB00', '#FEF7E0'),
            ('wrong_book_count', '📝 错题本', '#D93025', '#FCE8E6'),
        ]
        
        for i, (key, label, color, bg_color) in enumerate(stats_config):
            card = self._create_stat_card(label, "--", color, bg_color)
            self.overall_grid.addWidget(card, i // 2, i % 2)
            self.stat_cards[key] = card.findChild(QLabel, "value")
        
        layout.addLayout(self.overall_grid)
        
        # 详细统计区域
        detail_frame = QFrame()
        detail_frame.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        detail_layout = QVBoxLayout(detail_frame)
        detail_layout.setSpacing(15)
        
        detail_title = QLabel("📋 详细统计")
        detail_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        detail_title.setStyleSheet("color: #3C4043;")
        detail_layout.addWidget(detail_title)
        
        # 正确/错误统计
        self.correct_label = QLabel("✅ 正确：-- | ❌ 错误：--")
        self.correct_label.setFont(QFont("Arial", 13))
        self.correct_label.setStyleSheet("color: #5F6368; padding: 8px 0;")
        detail_layout.addWidget(self.correct_label)
        
        # 练习会话统计
        self.sessions_label = QLabel("💼 完成会话：--")
        self.sessions_label.setFont(QFont("Arial", 13))
        self.sessions_label.setStyleSheet("color: #5F6368; padding: 8px 0;")
        detail_layout.addWidget(self.sessions_label)
        
        layout.addWidget(detail_frame)
        
        # 进度条区域
        progress_frame = QFrame()
        progress_frame.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setSpacing(15)
        
        progress_title = QLabel("📊 练习进度")
        progress_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        progress_title.setStyleSheet("color: #3C4043;")
        progress_layout.addWidget(progress_title)
        
        self.practice_progress_label = QLabel("暂无题目")
        self.practice_progress_label.setFont(QFont("Arial", 12))
        self.practice_progress_label.setStyleSheet("color: #5F6368; padding: 5px 0;")
        progress_layout.addWidget(self.practice_progress_label)
        
        self.practice_progress_bar = QProgressBar()
        self.practice_progress_bar.setRange(0, 100)
        self.practice_progress_bar.setValue(0)
        self.practice_progress_bar.setFormat("%p%")
        self.practice_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #DADCE0;
                border-radius: 10px;
                text-align: center;
                background-color: #FFFFFF;
                height: 24px;
                font-size: 12px;
                color: #5F6368;
            }
            QProgressBar::chunk {
                background-color: #1A73E8;
                border-radius: 8px;
            }
        """)
        progress_layout.addWidget(self.practice_progress_bar)
        
        layout.addWidget(progress_frame)
        
        # 刷新按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.refresh_btn = QPushButton("🔄 刷新统计")
        self.refresh_btn.setFixedHeight(40)
        self.refresh_btn.clicked.connect(self.load_stats)
        btn_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def _create_section_title(self, text: str) -> QLabel:
        """创建章节标题"""
        label = QLabel(text)
        label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        label.setStyleSheet("color: #3C4043; padding: 10px 0; border-bottom: 2px solid #DADCE0;")
        return label
    
    def _create_stat_card(self, title: str, value: str, color: str, bg_color: str) -> QFrame:
        """创建统计卡片"""
        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: {bg_color};
                border: 2px solid {color};
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame#statCard:hover {{
                border-width: 3px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        title_label.setStyleSheet("color: #5F6368;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        return card
    
    def load_stats(self):
        """加载统计数据"""
        stats = self.practice_service.get_practice_stats()
        
        # 更新总体统计
        if self.stat_cards.get('total_questions'):
            self.stat_cards['total_questions'].setText(str(stats.get('total_questions', 0)))
        
        if self.stat_cards.get('practiced_questions'):
            self.stat_cards['practiced_questions'].setText(str(stats.get('practiced_questions', 0)))
        
        if self.stat_cards.get('accuracy'):
            accuracy = stats.get('accuracy', 0)
            self.stat_cards['accuracy'].setText(f"{accuracy:.1f}%")
        
        if self.stat_cards.get('wrong_book_count'):
            self.stat_cards['wrong_book_count'].setText(str(stats.get('wrong_book_count', 0)))
        
        # 更新详细统计
        correct = stats.get('correct_count', 0)
        wrong = stats.get('wrong_count', 0)
        self.correct_label.setText(f"✅ 正确：{correct}  |  ❌ 错误：{wrong}")
        
        sessions = stats.get('total_sessions', 0)
        self.sessions_label.setText(f"💼 完成会话：{sessions}")
        
        # 更新进度条
        total = stats.get('total_questions', 0)
        practiced = stats.get('practiced_questions', 0)
        if total > 0:
            progress = int(practiced / total * 100)
            self.practice_progress_bar.setValue(progress)
            self.practice_progress_label.setText(f"练习进度：{practiced} / {total}")
        else:
            self.practice_progress_bar.setValue(0)
            self.practice_progress_label.setText("暂无题目，请先添加或导入题目")

"""
数据库管理器 - 负责数据库连接和基础操作
"""
import sqlite3
import sys
from pathlib import Path
from contextlib import contextmanager


class DatabaseManager:
    """数据库管理器类"""

    def __init__(self, db_path: str = None):
        """
        初始化数据库管理器

        Args:
            db_path: 数据库文件路径，默认为当前目录下的 quizmaster.db
        """
        if db_path is None:
            # 打包后的环境：使用程序运行目录
            if getattr(sys, 'frozen', False):
                # PyInstaller 打包后的环境
                db_path = Path(sys.executable).parent / "quizmaster.db"
            else:
                # 开发环境：使用项目根目录
                db_path = Path(__file__).parent.parent / "quizmaster.db"
        self.db_path = Path(db_path)
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库连接并创建表"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    @contextmanager
    def get_cursor(self):
        """获取游标的上下文管理器"""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def _create_tables(self):
        """创建所有数据表"""
        with self.get_cursor() as cursor:
            # 题库分类表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    parent_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES categories(id)
                )
            """)
            
            # 题目表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    question_text TEXT NOT NULL,
                    question_type TEXT,
                    options TEXT,
                    answer TEXT NOT NULL,
                    explanation TEXT,
                    difficulty TEXT,
                    tags TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)
            
            # 用户答题记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS practice_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER,
                    user_answer TEXT,
                    is_correct BOOLEAN,
                    time_spent INTEGER,
                    is_marked BOOLEAN,
                    practice_session_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            """)
            
            # 练习会话表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS practice_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mode TEXT,
                    category_id INTEGER,
                    total_questions INTEGER,
                    completed_questions INTEGER DEFAULT 0,
                    correct_count INTEGER DEFAULT 0,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_time DATETIME,
                    status TEXT
                )
            """)
            
            # 错题本表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wrong_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER,
                    wrong_count INTEGER DEFAULT 1,
                    last_wrong_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    mastered BOOLEAN DEFAULT 0,
                    FOREIGN KEY (question_id) REFERENCES questions(id),
                    UNIQUE(question_id)
                )
            """)
    
    def execute(self, query: str, params: tuple = None):
        """执行 SQL 查询"""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    
    def fetchall(self, query: str, params: tuple = None):
        """执行查询并返回所有结果"""
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def fetchone(self, query: str, params: tuple = None):
        """执行查询并返回单条结果"""
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
    
    def backup(self, backup_path: str):
        """备份数据库"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
    
    def get_connection(self):
        """获取数据库连接对象"""
        return self.conn

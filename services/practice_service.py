"""
练习服务 - 负责刷题模式管理
"""
from typing import List, Optional, Tuple
from datetime import datetime
from database.db_manager import DatabaseManager
from database.models import Question, PracticeSession, PracticeRecord, WrongQuestion
import time


class PracticeService:
    """练习服务类"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    # ========== 获取题目 ==========
    
    def get_sequence_questions(self, category_id: Optional[int] = None, limit: int = 50, offset: int = 0) -> List[Question]:
        """按顺序获取题目"""
        query = "SELECT * FROM questions"
        params = []
        
        if category_id:
            query += " WHERE category_id = ?"
            params.append(category_id)
        
        query += " ORDER BY id LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        rows = self.db.fetchall(query, tuple(params))
        return [Question.from_row(row) for row in rows]
    
    def get_random_questions(self, category_id: Optional[int] = None, limit: int = 100) -> List[Question]:
        """随机获取题目"""
        query = "SELECT * FROM questions"
        params = []
        
        if category_id:
            query += " WHERE category_id = ?"
            params.append(category_id)
        
        query += " ORDER BY RANDOM() LIMIT ?"
        params.append(limit)
        
        rows = self.db.fetchall(query, tuple(params))
        return [Question.from_row(row) for row in rows]
    
    def get_wrong_questions(self, limit: int = 50, question_type: str = None) -> List[Question]:
        """获取错题本中的题目

        Args:
            limit: 获取数量限制
            question_type: 题型过滤（单选/多选/判断/填空），None 表示不过滤
        """
        query = """
            SELECT q.*, w.wrong_count, w.last_wrong_at
            FROM questions q
            JOIN wrong_questions w ON q.id = w.question_id
            WHERE w.mastered = 0
        """
        params = [limit]

        if question_type:
            query += " AND q.question_type = ?"
            params.insert(0, question_type)

        query += " ORDER BY q.id LIMIT ?"

        rows = self.db.fetchall(query, tuple(params))
        questions = [Question.from_row(row) for row in rows]

        # 为错题设置 serial_number：按题型分组计算题号
        # 如果指定了题型，只计算该题型内的序号；否则按各自题型分别计算
        if question_type:
            # 按指定题型计算序号
            all_query = "SELECT id FROM questions WHERE question_type = ? ORDER BY id"
            all_rows = self.db.fetchall(all_query, (question_type,))
            id_to_serial = {row['id']: idx + 1 for idx, row in enumerate(all_rows)}
        else:
            # 按题型分组计数
            all_query = "SELECT id, question_type FROM questions ORDER BY id"
            all_rows = self.db.fetchall(all_query)
            type_counters = {}
            id_to_serial = {}
            for row in all_rows:
                qtype = row['question_type'] or 'unknown'
                if qtype not in type_counters:
                    type_counters[qtype] = 0
                type_counters[qtype] += 1
                id_to_serial[row['id']] = type_counters[qtype]

        for q in questions:
            q.serial_number = id_to_serial.get(q.id, q.id)

        return questions
    
    # ========== 练习会话管理 ==========
    
    def create_session(self, mode: str, category_id: Optional[int] = None, total_questions: int = 0) -> int:
        """创建练习会话"""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO practice_sessions (mode, category_id, total_questions, status)
                VALUES (?, ?, ?, 'running')
            """, (mode, category_id, total_questions))
            return cursor.lastrowid
    
    def get_session(self, session_id: int) -> Optional[PracticeSession]:
        """获取练习会话"""
        row = self.db.fetchone(
            "SELECT * FROM practice_sessions WHERE id = ?",
            (session_id,)
        )
        return PracticeSession.from_row(row) if row else None
    
    def update_session_progress(self, session_id: int, completed: int, correct: int):
        """更新会话进度"""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE practice_sessions 
                SET completed_questions = ?, correct_count = ?
                WHERE id = ?
            """, (completed, correct, session_id))
    
    def complete_session(self, session_id: int):
        """完成练习会话"""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE practice_sessions 
                SET status = 'completed', end_time = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (session_id,))
    
    # ========== 答题记录 ==========
    
    def record_answer(self, question_id: int, user_answer: str, is_correct: bool, 
                     time_spent: int, session_id: Optional[int] = None, is_marked: bool = False) -> int:
        """记录答题"""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO practice_records 
                (question_id, user_answer, is_correct, time_spent, practice_session_id, is_marked)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (question_id, user_answer, is_correct, time_spent, session_id, is_marked))
            record_id = cursor.lastrowid
            
            # 如果答错了，加入错题本
            if not is_correct:
                self._add_to_wrong_book(question_id)
            
            return record_id
    
    def _add_to_wrong_book(self, question_id: int):
        """添加到错题本"""
        with self.db.get_cursor() as cursor:
            # 检查是否已存在
            cursor.execute(
                "SELECT * FROM wrong_questions WHERE question_id = ?",
                (question_id,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # 更新错误次数
                cursor.execute("""
                    UPDATE wrong_questions 
                    SET wrong_count = wrong_count + 1, last_wrong_at = CURRENT_TIMESTAMP
                    WHERE question_id = ?
                """, (question_id,))
            else:
                # 新增错题
                cursor.execute("""
                    INSERT INTO wrong_questions (question_id)
                    VALUES (?)
                """, (question_id,))
    
    def mark_question_as_mastered(self, question_id: int):
        """标记题目为已掌握"""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE wrong_questions 
                SET mastered = 1
                WHERE question_id = ?
            """, (question_id,))
    
    def get_question_record(self, question_id: int, session_id: Optional[int] = None) -> Optional[PracticeRecord]:
        """获取某题的答题记录"""
        if session_id:
            row = self.db.fetchone("""
                SELECT * FROM practice_records 
                WHERE question_id = ? AND practice_session_id = ?
                ORDER BY id DESC LIMIT 1
            """, (question_id, session_id))
        else:
            row = self.db.fetchone("""
                SELECT * FROM practice_records 
                WHERE question_id = ?
                ORDER BY id DESC LIMIT 1
            """, (question_id,))
        
        return PracticeRecord.from_row(row) if row else None
    
    # ========== 统计功能 ==========
    
    def get_practice_stats(self) -> dict:
        """获取练习统计"""
        stats = {
            'total_questions': self.db.fetchone("SELECT COUNT(*) FROM questions")[0],
            'practiced_questions': self.db.fetchone("""
                SELECT COUNT(DISTINCT question_id) FROM practice_records
            """)[0],
            'correct_count': self.db.fetchone("""
                SELECT COUNT(*) FROM practice_records WHERE is_correct = 1
            """)[0],
            'wrong_count': self.db.fetchone("""
                SELECT COUNT(*) FROM practice_records WHERE is_correct = 0
            """)[0],
            'wrong_book_count': self.db.fetchone("""
                SELECT COUNT(*) FROM wrong_questions WHERE mastered = 0
            """)[0],
            'total_sessions': self.db.fetchone("""
                SELECT COUNT(*) FROM practice_sessions WHERE status = 'completed'
            """)[0],
        }
        
        total = stats['correct_count'] + stats['wrong_count']
        stats['accuracy'] = (stats['correct_count'] / total * 100) if total > 0 else 0
        
        return stats
    
    def get_session_stats(self, session_id: int) -> dict:
        """获取单次会话统计"""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        return {
            'total': session.total_questions,
            'completed': session.completed_questions,
            'correct': session.correct_count,
            'accuracy': (session.correct_count / session.completed_questions * 100) 
                       if session.completed_questions > 0 else 0
        }
    
    def get_recent_sessions(self, limit: int = 10) -> List[PracticeSession]:
        """获取最近的练习会话"""
        rows = self.db.fetchall("""
            SELECT * FROM practice_sessions
            WHERE status = 'completed'
            ORDER BY end_time DESC
            LIMIT ?
        """, (limit,))
        return [PracticeSession.from_row(row) for row in rows]

    def get_last_practiced_question(self, category_id: Optional[int], question_type: Optional[str]) -> Optional[int]:
        """获取某分类/题型下顺序练习的最后一次题目 ID（用于计算下次起始位置）

        注意：只查询顺序练习模式 (sequence) 的记录，不包括错题练习等其他模式
        """
        query = """
            SELECT pr.question_id
            FROM practice_records pr
            JOIN questions q ON pr.question_id = q.id
            JOIN practice_sessions ps ON pr.practice_session_id = ps.id
            WHERE ps.mode = 'sequence'
        """
        params = []

        if category_id:
            query += " AND q.category_id = ?"
            params.append(category_id)

        if question_type:
            query += " AND q.question_type = ?"
            params.append(question_type)

        query += """
            ORDER BY ps.id DESC, pr.question_id DESC
            LIMIT 1
        """

        row = self.db.fetchone(query, tuple(params))
        return row[0] if row else None

    # ========== 标记功能 ==========

    def get_marked_questions(self) -> set:
        """获取所有已标记的题目 ID 集合"""
        rows = self.db.fetchall("""
            SELECT DISTINCT question_id FROM practice_records
            WHERE is_marked = 1
        """)
        return {row[0] for row in rows}

    def update_question_mark(self, question_id: int, is_marked: bool):
        """更新题目记号"""
        with self.db.get_cursor() as cursor:
            # 查找最近的答题记录
            cursor.execute("""
                SELECT id FROM practice_records
                WHERE question_id = ?
                ORDER BY id DESC LIMIT 1
            """, (question_id,))
            row = cursor.fetchone()

            if row:
                # 更新现有记录
                cursor.execute("""
                    UPDATE practice_records
                    SET is_marked = ?
                    WHERE question_id = ? AND id = ?
                """, (1 if is_marked else 0, question_id, row[0]))
            else:
                # 如果没有答题记录，创建一条标记记录
                cursor.execute("""
                    INSERT INTO practice_records
                    (question_id, is_marked, is_correct, time_spent)
                    VALUES (?, 1, 0, 0)
                """, (question_id,))

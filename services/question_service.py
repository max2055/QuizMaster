"""
题目管理服务 - 负责题目的增删改查
"""
from typing import List, Optional, Dict, Any
from database.db_manager import DatabaseManager
from database.models import Question, Category
import json


class QuestionService:
    """题目管理服务类"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    # ========== 分类管理 ==========
    
    def create_category(self, name: str, parent_id: Optional[int] = None) -> int:
        """创建分类"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO categories (name, parent_id) VALUES (?, ?)",
                (name, parent_id)
            )
            return cursor.lastrowid
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """获取单个分类"""
        row = self.db.fetchone(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,)
        )
        return Category.from_row(row) if row else None
    
    def get_all_categories(self) -> List[Category]:
        """获取所有分类"""
        rows = self.db.fetchall("SELECT * FROM categories ORDER BY id")
        return [Category.from_row(row) for row in rows]
    
    def get_categories_tree(self) -> List[Category]:
        """获取分类树形结构"""
        categories = self.get_all_categories()
        category_map = {cat.id: cat for cat in categories}
        
        # 构建树形结构
        roots = []
        for cat in categories:
            if cat.parent_id is None:
                roots.append(cat)
            else:
                parent = category_map.get(cat.parent_id)
                if parent:
                    parent.children.append(cat)
        
        return roots
    
    def update_category(self, category_id: int, name: str, parent_id: Optional[int] = None) -> bool:
        """更新分类"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "UPDATE categories SET name = ?, parent_id = ? WHERE id = ?",
                (name, parent_id, category_id)
            )
            return cursor.rowcount > 0
    
    def delete_category(self, category_id: int) -> bool:
        """删除分类（同时删除该分类下的题目）"""
        with self.db.get_cursor() as cursor:
            # 先删除该分类下的所有题目
            cursor.execute("DELETE FROM questions WHERE category_id = ?", (category_id,))
            # 再删除分类
            cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            return cursor.rowcount > 0
    
    # ========== 题目管理 ==========
    
    def create_question(self, question: Question) -> int:
        """创建题目"""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO questions 
                (category_id, question_text, question_type, options, answer, explanation, difficulty, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question.category_id,
                question.question_text,
                question.question_type,
                json.dumps(question.options),
                question.answer,
                question.explanation,
                question.difficulty,
                json.dumps(question.tags)
            ))
            return cursor.lastrowid
    
    def get_question(self, question_id: int) -> Optional[Question]:
        """获取单个题目"""
        row = self.db.fetchone(
            "SELECT * FROM questions WHERE id = ?",
            (question_id,)
        )
        return Question.from_row(row) if row else None
    
    def get_questions(self, category_id: Optional[int] = None, limit: int = 50, offset: int = 0) -> List[Question]:
        """获取题目列表"""
        query = "SELECT * FROM questions"
        params = []

        if category_id:
            query += " WHERE category_id = ?"
            params.append(category_id)

        query += " ORDER BY id LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.db.fetchall(query, tuple(params))
        return [Question.from_row(row) for row in rows]

    def get_questions_with_serial(self, category_id: Optional[int] = None,
                                   question_type_filter: Optional[str] = None) -> List[Question]:
        """获取题目列表并附带分组连续编号

        Args:
            category_id: 分类 ID，None 表示全部
            question_type_filter: 题型过滤（单选/多选/判断/填空）

        Returns:
            题目列表，每道题的 serial_number 为分组内连续编号
        """
        query = "SELECT * FROM questions"
        params = []

        # 构建 WHERE 子句
        where_clauses = []
        if category_id:
            where_clauses.append("category_id = ?")
            params.append(category_id)
        if question_type_filter:
            where_clauses.append("question_type = ?")
            params.append(question_type_filter)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        query += " ORDER BY id"

        rows = self.db.fetchall(query, tuple(params))

        # 添加连续编号
        questions = []
        for idx, row in enumerate(rows, start=1):
            q = Question.from_row(row)
            q.serial_number = idx
            questions.append(q)

        return questions

    def get_questions_by_category(self, category_id: int) -> List[Question]:
        """根据分类 ID 获取题目"""
        return self.get_questions(category_id=category_id, limit=10000)

    def get_all_questions(self) -> List[Question]:
        """获取所有题目"""
        return self.get_questions(limit=10000)
    
    def get_question_count(self, category_id: Optional[int] = None) -> int:
        """获取题目总数"""
        if category_id:
            row = self.db.fetchone(
                "SELECT COUNT(*) FROM questions WHERE category_id = ?",
                (category_id,)
            )
        else:
            row = self.db.fetchone("SELECT COUNT(*) FROM questions")
        return row[0] if row else 0
    
    def update_question(self, question: Question) -> bool:
        """更新题目"""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE questions SET
                    category_id = ?,
                    question_text = ?,
                    question_type = ?,
                    options = ?,
                    answer = ?,
                    explanation = ?,
                    difficulty = ?,
                    tags = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                question.category_id,
                question.question_text,
                question.question_type,
                json.dumps(question.options),
                question.answer,
                question.explanation,
                question.difficulty,
                json.dumps(question.tags),
                question.id
            ))
            return cursor.rowcount > 0
    
    def delete_question(self, question_id: int) -> bool:
        """删除题目"""
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
            return cursor.rowcount > 0
    
    def search_questions(self, keyword: str, category_id: Optional[int] = None) -> List[Question]:
        """搜索题目"""
        query = "SELECT * FROM questions WHERE question_text LIKE ?"
        params = [f"%{keyword}%"]
        
        if category_id:
            query += " AND category_id = ?"
            params.append(category_id)
        
        rows = self.db.fetchall(query, tuple(params))
        return [Question.from_row(row) for row in rows]
    
    def batch_import_questions(self, questions: List[Dict[str, Any]]) -> int:
        """批量导入题目"""
        count = 0
        with self.db.get_cursor() as cursor:
            for q_data in questions:
                try:
                    # 获取或创建分类
                    category_name = q_data.get('category', '默认')
                    cursor.execute(
                        "SELECT id FROM categories WHERE name = ?",
                        (category_name,)
                    )
                    cat_row = cursor.fetchone()
                    
                    if cat_row:
                        category_id = cat_row[0]
                    else:
                        cursor.execute(
                            "INSERT INTO categories (name) VALUES (?)",
                            (category_name,)
                        )
                        category_id = cursor.lastrowid
                    
                    # 插入题目
                    cursor.execute("""
                        INSERT INTO questions 
                        (category_id, question_text, question_type, options, answer, explanation, difficulty, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        category_id,
                        q_data['question_text'],
                        q_data.get('question_type', 'single'),
                        q_data.get('options', '{}'),
                        q_data['answer'],
                        q_data.get('explanation', ''),
                        q_data.get('difficulty', 'medium'),
                        q_data.get('tags', '[]')
                    ))
                    count += 1
                except Exception as e:
                    print(f"导入题目失败：{e}")
                    continue
        
        return count
    
    def export_questions(self, category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """导出题目"""
        questions = self.get_questions(category_id, limit=10000)
        result = []
        
        for q in questions:
            result.append({
                'id': q.id,
                'category_id': q.category_id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'options': q.options,
                'answer': q.answer,
                'explanation': q.explanation,
                'difficulty': q.difficulty,
                'tags': q.tags
            })
        
        return result

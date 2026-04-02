"""
数据模型 - 定义数据结构
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


@dataclass
class Category:
    """题库分类模型"""
    id: Optional[int] = None
    name: str = ""
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    children: List['Category'] = field(default_factory=list)
    
    @classmethod
    def from_row(cls, row):
        """从数据库行创建实例"""
        if row is None:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            parent_id=row['parent_id'],
            created_at=row['created_at']
        )


@dataclass
class Question:
    """题目模型"""
    id: Optional[int] = None
    category_id: Optional[int] = None
    question_text: str = ""
    question_type: str = "single"  # single/multi/true_false/fill
    options: Dict[str, str] = field(default_factory=dict)
    answer: str = ""
    explanation: str = ""
    difficulty: str = "medium"  # easy/medium/hard
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    serial_number: Optional[int] = None  # 分组连续编号（动态计算）

    @classmethod
    def from_row(cls, row):
        """从数据库行创建实例"""
        if row is None:
            return None

        # 解析 JSON 字段
        options = {}
        if row['options']:
            try:
                options = json.loads(row['options'])
            except:
                options = {}

        tags = []
        if row['tags']:
            try:
                tags = json.loads(row['tags'])
            except:
                tags = []

        # serial_number 是动态计算字段，可能不存在
        serial_number = None
        try:
            serial_number = row['serial_number'] if 'serial_number' in row.keys() else None
        except:
            serial_number = None

        return cls(
            id=row['id'],
            category_id=row['category_id'],
            question_text=row['question_text'],
            question_type=row['question_type'] or 'single',
            options=options,
            answer=row['answer'],
            explanation=row['explanation'] or '',
            difficulty=row['difficulty'] or 'medium',
            tags=tags,
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            serial_number=serial_number
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'category_id': self.category_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': json.dumps(self.options),
            'answer': self.answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'tags': json.dumps(self.tags),
        }


@dataclass
class PracticeRecord:
    """答题记录模型"""
    id: Optional[int] = None
    question_id: int = 0
    user_answer: str = ""
    is_correct: bool = False
    time_spent: int = 0
    is_marked: bool = False
    practice_session_id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_row(cls, row):
        """从数据库行创建实例"""
        if row is None:
            return None
        return cls(
            id=row['id'],
            question_id=row['question_id'],
            user_answer=row['user_answer'],
            is_correct=bool(row['is_correct']),
            time_spent=row['time_spent'] or 0,
            is_marked=bool(row['is_marked']),
            practice_session_id=row['practice_session_id'],
            created_at=row['created_at']
        )


@dataclass
class PracticeSession:
    """练习会话模型"""
    id: Optional[int] = None
    mode: str = "sequence"  # sequence/random/wrong
    category_id: Optional[int] = None
    total_questions: int = 0
    completed_questions: int = 0
    correct_count: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "pending"  # pending/running/completed
    
    @classmethod
    def from_row(cls, row):
        """从数据库行创建实例"""
        if row is None:
            return None
        return cls(
            id=row['id'],
            mode=row['mode'] or 'sequence',
            category_id=row['category_id'],
            total_questions=row['total_questions'] or 0,
            completed_questions=row['completed_questions'] or 0,
            correct_count=row['correct_count'] or 0,
            start_time=row['start_time'],
            end_time=row['end_time'],
            status=row['status'] or 'pending'
        )


@dataclass
class WrongQuestion:
    """错题模型"""
    id: Optional[int] = None
    question_id: int = 0
    wrong_count: int = 1
    last_wrong_at: Optional[datetime] = None
    mastered: bool = False
    
    @classmethod
    def from_row(cls, row):
        """从数据库行创建实例"""
        if row is None:
            return None
        return cls(
            id=row['id'],
            question_id=row['question_id'],
            wrong_count=row['wrong_count'] or 1,
            last_wrong_at=row['last_wrong_at'],
            mastered=bool(row['mastered'])
        )

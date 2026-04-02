"""
Word 导入工具 - 从 Word 文档导入题目
"""
from typing import List, Dict, Any
import json
import re


class WordImporter:
    """Word 导入器"""
    
    def __init__(self):
        try:
            from docx import Document
            self.Document = Document
        except ImportError:
            raise ImportError("需要安装 python-docx: pip install python-docx")
    
    def import_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        从 Word 文件导入题目
        
        支持两种格式：
        1. 结构化格式：每道题包含题目、选项、答案、解析
        2. 简单格式：按段落分割
        """
        doc = self.Document(file_path)
        questions = []
        
        # 提取所有段落文本
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        # 尝试解析题目
        current_question = None
        current_options = {}
        in_options = False
        
        for para in paragraphs:
            # 检测题目开始（以数字开头或包含"题目"）
            if self._is_question_start(para):
                # 保存之前的题目
                if current_question:
                    current_question['options'] = json.dumps(current_options)
                    questions.append(current_question)
                
                # 开始新题目
                current_question = {
                    'question_text': self._extract_question_text(para),
                    'options': '',
                    'answer': '',
                    'explanation': '',
                    'category': '默认',
                    'difficulty': 'medium',
                    'question_type': 'single',
                    'tags': '[]'
                }
                current_options = {}
                in_options = False
            
            elif current_question:
                # 检测选项
                opt_match = re.match(r'^([A-F])[、.．]\s*(.+)$', para)
                if opt_match:
                    in_options = True
                    opt_letter = opt_match.group(1)
                    opt_text = opt_match.group(2)
                    current_options[opt_letter] = opt_text
                
                # 检测答案
                elif re.match(r'^答案 [：:]', para) or para.startswith('正确答案'):
                    in_options = False
                    answer_text = re.sub(r'^答案 [：:]|^正确答案 [：:]?', '', para).strip()
                    current_question['answer'] = answer_text
                    # 根据答案长度判断题型
                    if len(answer_text) > 1:
                        current_question['question_type'] = 'multi'
                
                # 检测解析
                elif re.match(r'^解析 [：:]', para) or para.startswith('答案解析'):
                    explanation = re.sub(r'^解析 [：:]|^答案解析 [：:]?', '', para).strip()
                    current_question['explanation'] = explanation
                
                # 检测分类
                elif re.match(r'^分类 [：:]', para):
                    category = re.sub(r'^分类 [：:]', '', para).strip()
                    current_question['category'] = category
                
                # 检测难度
                elif re.match(r'^难度 [：:]', para):
                    difficulty = re.sub(r'^难度 [：:]', '', para).strip()
                    current_question['difficulty'] = difficulty
        
        # 保存最后一道题
        if current_question:
            current_question['options'] = json.dumps(current_options)
            questions.append(current_question)
        
        return questions
    
    def _is_question_start(self, text: str) -> bool:
        """判断是否是题目开始"""
        # 匹配 "1." "1、" "第 1 题" 等格式
        if re.match(r'^\d+[、.．]', text):
            return True
        if re.match(r'^第\d+题', text):
            return True
        if text.startswith('题目') and ':' in text:
            return True
        return False
    
    def _extract_question_text(self, text: str) -> str:
        """提取题目文本"""
        # 移除题号前缀
        text = re.sub(r'^\d+[、.．]\s*', '', text)
        text = re.sub(r'^第\d+题\s*', '', text)
        text = re.sub(r'^题目 [：:]\s*', '', text)
        return text.strip()

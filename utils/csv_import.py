"""
CSV 导入工具 - 从 CSV 文件导入题目
"""
from typing import List, Dict, Any
import json
import csv


class CSVImporter:
    """CSV 导入器"""
    
    def import_file(self, file_path: str, encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        """
        从 CSV 文件导入题目
        
        支持的列：
        - 题目 (必需)
        - 选项 A, 选项 B, 选项 C, 选项 D, 选项 E, 选项 F
        - 答案 (必需)
        - 解析
        - 分类
        - 难度
        - 题型
        - 标签
        """
        questions = []
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        question = self._parse_row(row)
                        if question:
                            questions.append(question)
                    except Exception as e:
                        print(f"解析行失败：{e}")
                        continue
        except UnicodeDecodeError:
            # 尝试其他编码
            for enc in ['gbk', 'gb2312', 'latin-1']:
                try:
                    return self.import_file(file_path, encoding=enc)
                except:
                    continue
            raise
        
        return questions
    
    def _parse_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """解析单行数据"""
        # 获取题目内容
        question_text = self._get_value(row, '题目')
        if not question_text:
            return None
        
        # 构建选项
        options = {}
        for opt in ['A', 'B', 'C', 'D', 'E', 'F']:
            opt_key = f'选项{opt}'
            opt_value = self._get_value(row, opt_key)
            if opt_value:
                options[opt] = opt_value
        
        # 获取答案
        answer = self._get_value(row, '答案')
        if not answer:
            return None
        
        # 获取其他字段
        question_type = self._get_value(row, '题型') or self._detect_question_type(options, answer)
        explanation = self._get_value(row, '解析') or ''
        category = self._get_value(row, '分类') or '默认'
        difficulty = self._get_value(row, '难度') or 'medium'
        
        # 处理标签
        tags_str = self._get_value(row, '标签') or ''
        tags = [t.strip() for t in tags_str.split(',') if t.strip()] if tags_str else []
        
        return {
            'question_text': question_text,
            'options': json.dumps(options),
            'answer': answer,
            'explanation': explanation,
            'category': category,
            'difficulty': difficulty,
            'question_type': question_type,
            'tags': json.dumps(tags)
        }
    
    def _get_value(self, row: Dict[str, str], key: str) -> str:
        """安全获取列值"""
        # 尝试多种列名变体
        variations = [key, key.replace(' ', ''), key.replace(' ', '_')]
        for var in variations:
            if var in row:
                val = row[var]
                if val and str(val).strip():
                    return str(val).strip()
        return None
    
    def _detect_question_type(self, options: dict, answer: str) -> str:
        """根据选项和答案推断题型"""
        if len(options) == 2 and any(k in answer for k in ['正确', '错误', '对', '错', 'T', 'F']):
            return 'true_false'
        elif len(answer) > 1:
            return 'multi'  # 多选题
        else:
            return 'single'  # 单选题

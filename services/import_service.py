"""
导入服务 - 负责从不同格式导入题目
"""
from typing import List, Dict, Any
from utils.excel_import import ExcelImporter
from utils.csv_import import CSVImporter
from utils.word_import import WordImporter


class ImportService:
    """导入服务类"""
    
    def __init__(self):
        self.excel_importer = ExcelImporter()
        self.csv_importer = CSVImporter()
        self.word_importer = WordImporter()
    
    def import_from_file(self, file_path: str, file_type: str = None) -> List[Dict[str, Any]]:
        """
        从文件导入题目
        
        Args:
            file_path: 文件路径
            file_type: 文件类型 ('excel', 'csv', 'word'), 为 None 时自动检测
        
        Returns:
            题目数据列表
        """
        if file_type is None:
            file_type = self._detect_file_type(file_path)
        
        if file_type == 'excel':
            return self.excel_importer.import_file(file_path)
        elif file_type == 'csv':
            return self.csv_importer.import_file(file_path)
        elif file_type == 'word':
            return self.word_importer.import_file(file_path)
        else:
            raise ValueError(f"不支持的文件类型：{file_type}")
    
    def _detect_file_type(self, file_path: str) -> str:
        """根据文件扩展名检测文件类型"""
        lower_path = file_path.lower()
        if lower_path.endswith(('.xlsx', '.xls')):
            return 'excel'
        elif lower_path.endswith('.csv'):
            return 'csv'
        elif lower_path.endswith(('.docx', '.doc')):
            return 'word'
        else:
            raise ValueError(f"无法识别的文件类型：{file_path}")
    
    def get_supported_formats(self) -> List[str]:
        """获取支持的文件格式"""
        return ['Excel (.xlsx, .xls)', 'CSV (.csv)', 'Word (.docx, .doc)']

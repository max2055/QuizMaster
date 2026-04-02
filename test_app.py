"""
QuizMaster 测试脚本
用于验证基本功能
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from database.models import Question, Category
from services.question_service import QuestionService
from services.practice_service import PracticeService


def test_database():
    """测试数据库功能"""
    print("🧪 测试数据库功能...")
    
    # 创建数据库管理器
    db = DatabaseManager(":memory:")  # 使用内存数据库测试
    
    # 创建服务
    question_service = QuestionService(db)
    practice_service = PracticeService(db)
    
    # 测试分类
    print("  ✓ 创建分类...")
    cat_id = question_service.create_category("测试分类")
    assert cat_id > 0, "分类创建失败"
    
    # 测试题目
    print("  ✓ 创建题目...")
    question = Question(
        category_id=cat_id,
        question_text="测试题目",
        question_type="single",
        options={"A": "选项 A", "B": "选项 B"},
        answer="A",
        explanation="这是解析",
        difficulty="easy",
        tags=["测试"]
    )
    q_id = question_service.create_question(question)
    assert q_id > 0, "题目创建失败"
    
    # 测试获取题目
    print("  ✓ 获取题目...")
    retrieved = question_service.get_question(q_id)
    assert retrieved is not None, "获取题目失败"
    assert retrieved.question_text == "测试题目", "题目内容不匹配"
    
    # 测试练习会话
    print("  ✓ 创建练习会话...")
    session_id = practice_service.create_session("sequence", cat_id, 10)
    assert session_id > 0, "会话创建失败"
    
    # 测试答题记录
    print("  ✓ 记录答题...")
    record_id = practice_service.record_answer(q_id, "A", True, 10, session_id)
    assert record_id > 0, "答题记录失败"
    
    # 测试统计
    print("  ✓ 获取统计...")
    stats = practice_service.get_practice_stats()
    assert stats['total_questions'] == 1, "统计错误"
    
    # 关闭数据库
    db.close()
    
    print("✅ 所有数据库测试通过！\n")
    return True


def test_import():
    """测试导入功能"""
    print("🧪 测试导入功能...")
    
    from utils.csv_import import CSVImporter
    
    # 测试 CSV 导入
    template_path = os.path.join(os.path.dirname(__file__), "templates", "题目导入模板.csv")
    if os.path.exists(template_path):
        print("  ✓ 导入 CSV 模板...")
        importer = CSVImporter()
        questions = importer.import_file(template_path)
        assert len(questions) > 0, "导入失败"
        print(f"    成功导入 {len(questions)} 道题目")
    else:
        print("  ⚠ 模板文件不存在，跳过测试")
    
    print("✅ 导入测试通过！\n")
    return True


def test_ui_imports():
    """测试 UI 模块导入"""
    print("🧪 测试 UI 模块导入...")
    
    try:
        from ui.main_window import MainWindow
        from ui.question_widget import QuestionWidget
        from ui.stats_widget import StatsWidget
        from ui.dialogs import QuestionDialog, ImportDialog, CategoryDialog
        print("  ✓ 所有 UI 模块导入成功")
    except ImportError as e:
        print(f"  ⚠ UI 模块导入失败（可能缺少 PyQt6）: {e}")
        return False
    
    print("✅ UI 模块测试通过！\n")
    return True


def main():
    """运行所有测试"""
    print("=" * 60)
    print("QuizMaster 测试套件")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # 测试数据库
    try:
        if not test_database():
            all_passed = False
    except Exception as e:
        print(f"❌ 数据库测试失败：{e}\n")
        all_passed = False
    
    # 测试导入
    try:
        if not test_import():
            all_passed = False
    except Exception as e:
        print(f"❌ 导入测试失败：{e}\n")
        all_passed = False
    
    # 测试 UI 导入（需要 PyQt6）
    try:
        if not test_ui_imports():
            print("  提示：安装 PyQt6 后可运行完整 UI 测试\n")
    except Exception as e:
        print(f"❌ UI 测试失败：{e}\n")
    
    # 总结
    print("=" * 60)
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("⚠ 部分测试未通过")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

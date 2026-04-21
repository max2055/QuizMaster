#!/usr/bin/env python3
"""
从 Word 文件导入单选题到数据库 - 保留 E/F 选项
"""
import sys
import json
import re
import sqlite3
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("需要安装 python-docx: pip install python-docx")
    sys.exit(1)


def parse_word_questions(file_path: str):
    """从 Word 文件解析题目"""
    doc = Document(file_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    questions = []
    current_question = None
    current_options = {}

    for para in paragraphs:
        # 检测题目开始（以数字 + 分隔符开头）
        question_start = re.match(r'^(\d+)[、.．．]\s*(.+)$', para)
        if question_start:
            # 保存之前的题目
            if current_question and current_options:
                current_question['options'] = current_options
                questions.append(current_question)

            # 开始新题目
            q_num = int(question_start.group(1))
            q_text = question_start.group(2)
            current_question = {
                'question_text': q_text,
                'answer': '',
                'explanation': '',
                'question_type': '单选'
            }
            current_options = {}

        elif current_question is not None:
            # 检测选项（支持 A-F）
            opt_match = re.match(r'^([A-F])[、.．．]\s*(.+)$', para)
            if opt_match:
                opt_letter = opt_match.group(1)
                opt_text = opt_match.group(2)
                current_options[opt_letter] = opt_text

            # 检测答案
            elif re.match(r'^答案 [：:]', para) or para.startswith('正确答案'):
                answer_text = re.sub(r'^答案 [：:]|^正确答案 [：:]?', '', para).strip()
                current_question['answer'] = answer_text

            # 检测解析
            elif re.match(r'^解析 [：:]', para):
                explanation = re.sub(r'^解析 [：:]', '', para).strip()
                current_question['explanation'] = explanation

    # 保存最后一道题
    if current_question and current_options:
        current_question['options'] = current_options
        questions.append(current_question)

    return questions


def main():
    if len(sys.argv) < 2:
        print("用法：python3 import_single_from_word.py <word 文件路径>")
        sys.exit(1)

    word_file = sys.argv[1]
    db_file = Path(__file__).parent / 'quizmaster.db'

    print(f"正在解析 Word 文件：{word_file}")
    questions = parse_word_questions(word_file)
    print(f"解析到 {len(questions)} 道单选题")

    # 统计有 E/F 选项的题目
    with_ef = sum(1 for q in questions if 'E' in q['options'] or 'F' in q['options'])
    print(f"其中包含 E/F 选项的题目：{with_ef} 道")

    # 显示前 5 道有 E/F 选项的题目
    count = 0
    for q in questions:
        if 'E' in q['options'] or 'F' in q['options']:
            count += 1
            if count <= 5:
                print(f"\n--- 题目 ---")
                print(f"{q['question_text'][:100]}...")
                print(f"选项：{q['options']}")

    # 询问是否继续导入
    print(f"\n是否将这 {len(questions)} 道题目导入数据库？(y/n)")
    response = input().strip().lower()
    if response != 'y':
        print("已取消")
        return

    # 连接到数据库
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 获取现有分类 ID（单选题分类）
    cursor.execute("SELECT id FROM categories WHERE name LIKE '%单选%'")
    row = cursor.fetchone()
    category_id = row[0] if row else None

    if not category_id:
        print("警告：未找到单选题分类，需要先创建分类")
        return

    imported = 0
    for q in questions:
        try:
            # 检查是否已存在相同题目（通过题目文本）
            cursor.execute("SELECT id FROM questions WHERE question_text = ? AND question_type = '单选'",
                          (q['question_text'],))
            if cursor.fetchone():
                print(f"跳过已存在的题目：{q['question_text'][:30]}...")
                continue

            # 插入新题目
            cursor.execute("""
                INSERT INTO questions (category_id, question_text, question_type, options, answer, explanation)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                category_id,
                q['question_text'],
                q['question_type'],
                json.dumps(q['options']),
                q['answer'],
                q['explanation']
            ))
            imported += 1
        except Exception as e:
            print(f"导入失败：{e}")
            continue

    conn.commit()
    conn.close()

    print(f"\n完成！导入了 {imported} 道题目")


if __name__ == '__main__':
    main()

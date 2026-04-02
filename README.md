# QuizMaster - 刷题工具

一款功能明确、高效的题库管理和刷题工具，支持 Windows/macOS/Linux 跨平台运行。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ 功能特性

- 📚 **题库管理** - 支持题目的增删改查、批量导入导出
- 📝 **多种刷题模式** - 顺序刷题、随机刷题、错题模式
- 🌳 **分类管理** - 树形结构，支持多级分类
- 📊 **统计分析** - 实时统计练习进度和正确率
- 📝 **错题本** - 自动记录错题，支持标记掌握
- ⌨️ **键盘快捷键** - 高效操作，提升刷题体验
- 🖥️ **跨平台** - Windows/macOS/Linux 全支持

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

### 打包为可执行文件

**Windows:**
```bash
build.bat
```

**macOS/Linux:**
```bash
chmod +x build.sh
./build.sh
```

---

## 📖 文档

- [用户手册](docs/用户手册.md) - 详细的使用说明
- [导入格式说明](docs/导入格式说明.md) - 题目导入格式规范
- [打包发布指南](docs/打包发布指南.md) - 打包和发布说明

---

## 📷 界面预览

### 主界面
- 左侧：题库分类树
- 右侧：刷题练习/统计分析

### 刷题模式
- 进度条显示
- 题目和选项
- 答案提交和解析
- 键盘快捷键支持

---

## 🗄️ 数据库

使用 SQLite 本地存储，包含以下数据表：

- `categories` - 题库分类
- `questions` - 题目
- `practice_records` - 答题记录
- `practice_sessions` - 练习会话
- `wrong_questions` - 错题本

数据库文件：`quizmaster.db`（运行后自动生成）

---

## 📦 技术栈

- **Python 3.9+** - 开发语言
- **PyQt6** - GUI 框架
- **SQLite** - 数据库
- **pandas** - Excel 数据处理
- **python-docx** - Word 文档处理
- **PyInstaller** - 打包工具

---

## 📁 项目结构

```
QuizMaster/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖包
├── database/               # 数据库模块
├── ui/                     # 界面模块
├── services/               # 服务模块
├── utils/                  # 工具模块
├── resources/              # 资源文件
├── docs/                   # 文档
└── build.*                 # 打包脚本
```

---

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| 1-6 | 选择选项 A-F |
| Enter | 提交答案 |
| → | 下一题 |
| ← | 上一题 |
| Ctrl+N | 添加题目 |
| Ctrl+I | 导入题目 |
| Ctrl+E | 导出题库 |
| Ctrl+Q | 退出程序 |

---

## 📋 导入格式

支持从 Excel、CSV、Word 文件批量导入题目。

### Excel/CSV 格式示例

| 题目 | 选项 A | 选项 B | 选项 C | 选项 D | 答案 | 解析 | 分类 | 难度 |
|------|--------|--------|--------|--------|------|------|------|------|
| 1+1=? | 1 | 2 | 3 | 4 | B | 基础加法 | 数学 | easy |

详见：[导入格式说明](docs/导入格式说明.md)

---

## 🛠️ 开发

### 环境要求

- Python 3.9+
- pip 包管理器

### 开发步骤

```bash
# 克隆项目
git clone <repository-url>
cd QuizMaster

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py

# 运行测试（待添加）
pytest
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 联系方式

如有问题或建议，欢迎反馈。

---

**版本**: 1.0.0  
**更新日期**: 2026-03-26

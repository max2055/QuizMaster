# QuizMaster - 刷题工具

一款功能明确、高效的题库管理和刷题工具，支持 Windows/macOS/Linux 跨平台运行。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ 功能特性

- 📚 **题库管理** - 支持题目的增删改查、批量导入导出
- 📝 **多种题型** - 单选题、多选题、判断题、填空题
- 📝 **多种刷题模式** - 顺序刷题、随机刷题、错题模式
- 🚀 **自动下一题** - 答题后自动跳转，支持延迟设置
- 🎯 **跳转题号** - 支持按题型分别设置起始题号
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
或双击运行 `package_for_windows.bat`

**macOS/Linux:**
```bash
chmod +x build.sh
./build.sh
```

**GitHub Actions 自动构建:**

推送标签后自动构建 Windows 可执行文件：
```bash
git tag v1.5.7
git push origin v1.5.7
```

构建产物在 **Actions** 页面下载：https://github.com/max2055/QuizMaster/actions

打包完成后，可执行文件位于 `dist/` 目录。

---

## 📖 使用说明

### 快速开始

1. 双击运行 QuizMaster.exe（或从源码运行 `python main.py`）
2. 点击左侧分类（如"单选题"）
3. 点击"▶ 开始练习"按钮
4. 答题完成后点击"✓ 提交答案"

### 功能说明

- **题型过滤**：点击"单选题"只练习单选题，点击"多选题"只练习多选题
- **连续编号**：题目按题型从 1 开始连续编号（单选题 1-528，多选题 1-400）
- **标记功能**：按空格键或点击"📌 标记"按钮，标记的题目在答题卡上显示 📌
- **查看答案**：练习过程中可随时点击"查看答案"按钮
- **错题练习**：做错的题目自动收录到错题本

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| 空格键 | 标记/取消标记当前题目 |
| Ctrl+1/2/3/4 | 选择答案 A/B/C/D |
| Enter 键 | 提交当前题目答案 |
| 1-6 | 选择选项 A-F |
| → | 下一题 |
| ← | 上一题 |
| Ctrl+N | 添加题目 |
| Ctrl+I | 导入题目 |
| Ctrl+E | 导出题库 |
| Ctrl+Q | 退出程序 |

### 数据说明

- 所有答题记录保存在 `quizmaster.db` 文件
- 如需备份数据，复制该文件即可
- 如需重置数据，删除该文件后重启程序

### 系统要求

- Windows 10 / 11
- 无需安装 Python 或其他运行环境

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
└── build.*                 # 打包脚本
```

---

## 📋 导入格式

支持从 Excel、CSV、Word 文件批量导入题目。

### Excel/CSV 格式示例

| 题目 | 选项 A | 选项 B | 选项 C | 选项 D | 答案 | 解析 | 分类 | 难度 |
|------|--------|--------|--------|--------|------|------|------|------|
| 1+1=? | 1 | 2 | 3 | 4 | B | 基础加法 | 数学 | easy |

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

**版本**: 1.5.7  
**更新日期**: 2026-04-08

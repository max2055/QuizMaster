# UI 设计规范 - QuizMaster

## 颜色系统

### 主色调
| 用途 | 色值 | 说明 |
|------|------|------|
| 主色 | `#1A73E8` | 按钮、链接、选中状态 |
| 主色悬停 | `#1557B0` | 按钮悬停状态 |
| 主色浅蓝 | `#E8F0FE` | 选中背景 |
| 主色边框 | `#D2E3FC` | 选中边框 |

### 中性色
| 用途 | 色值 |
|------|------|
| 文字主色 | `#3C4043` |
| 文字次要 | `#5F6368` |
| 边框默认 | `#DADCE0` |
| 边框浅色 | `#E8EAED` |
| 背景浅色 | `#F8F9FA` |
| 背景组色 | `#FAFBFC` |

### 语义色
| 用途 | 色值 |
|------|------|
| 成功/正确 | `#1E8E3E` / `#E6F4EA` |
| 错误/危险 | `#D93025` / `#FCE8E6` |
| 警告 | `#F9AB00` |
| 信息 | `#1A73E8` |

## 间距系统

### 边距 (Margins)
- 对话框大边距：`20px`
- 对话框标准边距：`16px`
- 组件内边距：`12px`

### 间距 (Spacing)
- 大组间距：`20px`
- 标准组间距：`16px`
- 组件间距：`12px`
- 紧凑间距：`8px`
- 微间距：`4px`

## 圆角规范

| 组件 | 圆角 |
|------|------|
| 按钮 | `6px` |
| 输入框 | `6px` |
| 卡片 | `8px` |
| 对话框 | `8px` |
| GroupBox | `8px` |

## 字体规范

### 字体家族
| 平台 | 字体 |
|------|------|
| Windows | Microsoft YaHei |
| macOS | PingFang SC |
| Linux | Noto Sans CJK SC |
| 通用 | Arial (备用) |

### 字号
| 用途 | 字号 | 字重 |
|------|------|------|
| 对话框标题 | 16px | Bold |
| 组标题 | 12-13px | Bold |
| 正文 | 12-13px | Normal |
| 按钮 | 13px | Normal/Medium |
| 辅助文字 | 12px | Normal |

## 组件规范

### 按钮
```python
# 主按钮
QPushButton {
    background-color: #1A73E8;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    min-height: 36px;
}

# 次按钮
QPushButton {
    background-color: #FFFFFF;
    color: #5F6368;
    border: 1px solid #DADCE0;
    border-radius: 6px;
    font-size: 13px;
}
```

### 输入框
```python
# 标准输入框
QLineEdit {
    border: 1px solid #DADCE0;
    border-radius: 6px;
    padding: 8px 12px;
    background-color: #FFFFFF;
    font-size: 13px;
    min-height: 36px;
}

QLineEdit:focus {
    border-color: #1A73E8;
}
```

### 复选框
```python
QCheckBox {
    color: #3C4043;
    spacing: 8px;
    padding: 4px 0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 1.5px solid #DADCE0;
}
```

## 布局最佳实践

### 1. 避免固定尺寸
```python
# ❌ 不好的做法
button.setFixedWidth(120)
widget.setFixedHeight(40)

# ✅ 推荐做法
button.setMinimumWidth(120)
button.setMinimumHeight(40)
widget.setMaximumWidth(200)
```

### 2. 使用尺寸策略
```python
from PyQt6.QtWidgets import QSizePolicy

# 弹性布局
widget.setSizePolicy(
    QSizePolicy.Policy.Expanding,  # 水平
    QSizePolicy.Policy.Preferred   # 垂直
)
```

### 3. 对话框最小尺寸
- 设置对话框：`550x480px`
- 分类对话框：`450x280px`
- 题目对话框：`650x550px`
- 导入对话框：`500x350px`

### 4. 响应式侧边栏
```python
# 使用最小/最大宽度代替固定宽度
left_widget.setMinimumWidth(150)
left_widget.setMaximumWidth(200)
```

## 交互规范

### 焦点处理
```python
# 复选框移除焦点，避免整个区域高亮
checkbox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
```

### 悬停效果
```python
# 按钮悬停
QPushButton:hover {
    background-color: #F1F3F4;
    border-color: #1A73E8;
}

# 列表项悬停
QTreeWidget::item:hover {
    background-color: #F8F9FA;
}
```

### 选中状态
```python
# 选中高亮
QTreeWidget::item:selected {
    background-color: #E8F0FE;
    color: #1A73E8;
    font-weight: bold;
}
```

## 无障碍设计

### 对比度要求
- 主要文字对比度至少 4.5:1
- 大文字对比度至少 3:1
- 使用 [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) 验证

### 点击区域
- 按钮最小尺寸：`48x48px` (移动端友好)
- 桌面端最小：`36x36px`
- 复选框指示器：`18x18px`

## 响应式断点

| 窗口宽度 | 布局调整 |
|----------|----------|
| < 600px | 单栏布局，隐藏侧边栏 |
| 600-900px | 侧边栏缩小至 150px |
| > 900px | 标准双栏布局 |

## 常用样式片段

### 卡片样式
```python
card.setStyleSheet("""
    QFrame {
        background-color: #FFFFFF;
        border: 1px solid #E8EAED;
        border-radius: 8px;
        padding: 16px;
    }
    QFrame:hover {
        border-color: #DADCE0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
""")
```

### 分隔线
```python
line = QFrame()
line.setFrameShape(QFrame.Shape.HLine)
line.setStyleSheet("""
    background-color: #E8EAED;
    max-height: 1px;
""")
```

### 滚动条
```python
QScrollBar:vertical {
    background-color: #F1F3F4;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #DADCE0;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #BDC1C6;
}
```

## 检查清单

在提交 UI 改动前，请检查：

- [ ] 所有按钮有最小尺寸（非固定尺寸）
- [ ] 对话框设置了合理的 `minimumSize`
- [ ] 颜色对比度符合无障碍标准
- [ ] 悬停/选中状态有一致的视觉反馈
- [ ] 文字大小在可阅读范围内（12-14px）
- [ ] 间距遵循 4/8/12/16/20 系统
- [ ] 圆角风格一致（6px/8px）
- [ ] 窗口可以正常缩放而不挤压内容

---

**版本**: 1.0.0  
**更新日期**: 2026-03-31

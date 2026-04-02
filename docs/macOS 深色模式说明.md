# macOS 深色模式说明

## 问题描述

在 macOS 系统深色模式下，QuizMaster 的窗口标题栏（包含红黄绿关闭按钮的区域）可能显示为深色，与应用内部的浅色主题不一致。

## 原因

这是 macOS 系统级别的行为：
- 窗口标题栏颜色由系统深色模式设置控制
- Qt 应用无法在运行时单独覆盖窗口标题栏颜色
- 需要应用级别的配置来强制浅色模式

## 解决方案

### 方案 1：打包后自动浅色（推荐）

打包后的应用会自动使用浅色标题栏，因为我们在 `Info.plist` 中设置了：

```xml
<key>NSRequiresAquaSystemAppearance</key>
<true/>
```

**打包步骤**:
```bash
cd QuizMaster
./build.sh
```

打包生成的应用将始终使用浅色模式，不受系统设置影响。

### 方案 2：临时切换系统模式

开发测试时，可以临时切换系统外观：

1. 打开 **系统设置**
2. 选择 **外观**
3. 选择 **浅色**

### 方案 3：仅影响当前应用（开发模式）

在终端运行以下命令后启动应用：

```bash
defaults write com.quizmaster.app NSRequiresAquaSystemAppearance -bool true
python3 main.py
```

## 当前状态

### ✅ 已修复
- 应用内部所有 UI 组件使用浅色主题
- 所有对话框使用浅色背景
- 统计页面使用浅色卡片
- 分类树使用浅色背景

### ⚠️ 限制
- **开发模式运行** (`python3 main.py`): 标题栏颜色跟随系统设置
- **打包后运行** (`QuizMaster.app`): 标题栏强制浅色

## 建议

为了获得一致的用户体验，建议：

1. **开发阶段**: 忽略标题栏颜色差异（正常现象）
2. **发布阶段**: 使用打包后的应用（标题栏强制浅色）
3. **用户分发**: 分发生成的 `.app` 或 `.dmg` 文件

## 技术细节

### Info.plist 配置

```xml
<key>NSRequiresAquaSystemAppearance</key>
<true/>
```

这个键值告诉 macOS 系统，该应用始终使用 Aqua（浅色）外观，即使用户在系统级别选择了深色模式。

### PyInstaller 集成

在 `QuizMaster.spec` 文件中：

```python
if sys.platform == 'darwin':
    info_plist_dict = {
        "NSRequiresAquaSystemAppearance": True,
        # ... 其他配置
    }
```

打包时会自动包含此配置。

## 其他平台

- **Windows**: 不受此问题影响
- **Linux**: 不受此问题影响（取决于桌面环境）

---

**更新日期**: 2026-03-26  
**版本**: 1.0.4

# Claude Skills 使用说明

## 截图中的 Skills 说明

根据你提供的截图，以下是常见的 Claude Skills 及其用途：

### 1. /commit - 代码提交
**用途**: 自动生成 commit message 并提交代码
**用法**:
```bash
/commit -m "修复按钮样式问题"
```
**自动模式**: 直接提交当前暂存区的更改

### 2. /review-pr - PR 审查
**用途**: 自动审查 Pull Request
**用法**:
```bash
/review-pr 123
```
需要提供 PR 编号，会自动获取变更并给出审查意见

### 3. /test - 运行测试
**用途**: 自动运行项目测试
**用法**:
```bash
/test
```
本项目中会运行 `python test_app.py`

### 4. /docs - 生成文档
**用途**: 自动生成代码文档
**用法**:
```bash
/docs ui/dialogs.py
```

### 5. /refactor - 代码重构
**用途**: 安全地重构代码
**用法**:
```bash
/refactor 将函数拆分为更小的单元
```

### 6. /explain - 代码解释
**用途**: 解释复杂代码逻辑
**用法**:
```bash
/explain ui/question_widget.py
```

### 7. /search-code - 代码搜索
**用途**: 在代码库中搜索模式
**用法**:
```bash
/search-code "class.*Dialog"
```

### 8. /git-blame - 代码溯源
**用途**: 查看代码修改历史
**用法**:
```bash
/git-blame ui/main_window.py
```

## 安装 Skills 的步骤

### 方法 1: 使用 Slope AI (推荐)
1. 访问 https://slope.ai/
2. 登录 GitHub 账号 (wu_chenlong@hotmail.com)
3. 浏览 Skills 市场
4. 点击 "Install" 安装需要的 Skills
5. Skills 会自动同步到你的 Claude Code

### 方法 2: 手动配置 MCP
Skills 本质上是 MCP 服务器的封装。对于本项目，已配置以下核心功能：

```json
// .mcp.json 已包含：
- filesystem: 文件操作
- github: GitHub 集成  
- brave-search: 网络搜索
- memory: 长期记忆
```

## 本项目推荐的 Skills 配置

基于 QuizMaster 项目的需求，建议安装以下 Skills：

### PyQt6 开发相关
- `/ui-preview`: 预览 UI 效果
- `/qt-docs`: 查询 PyQt6 文档
- `/style-check`: 检查代码风格

### 项目管理相关
- `/commit`: 提交代码
- `/test`: 运行测试
- `/explain`: 解释代码

## 使用示例

```bash
# 1. 提交代码
/commit -m "优化设置对话框布局"

# 2. 运行测试
/test

# 3. 查询 PyQt6 文档
qt-docs QSizePolicy

# 4. 解释代码
/explain ui/question_widget.py:150-200

# 5. 检查 UI 风格
/style-check ui/settings_dialog.py
```

## 注意事项

1. **GitHub Token**: 部分 Skills 需要 GitHub 认证
   - 访问 https://github.com/settings/tokens
   - 创建 token 并勾选 repo 权限
   - 填入 `.mcp.json` 中的 `GITHUB_TOKEN`

2. **技能冲突**: 如果多个技能功能相似，优先使用项目内置的 MCP

3. **性能**: 首次使用某个技能时会下载依赖，可能需要等待

## 当前项目状态

✅ Node.js v22.22.1 已安装
✅ MCP 配置文件 `.mcp.json` 已创建
✅ 全局 settings.json 已配置使用项目 MCP
✅ UI 设计规范文档已创建 (`docs/UI 设计规范.md`)

## 下一步

1. 如果需要特定技能，请访问 Slope AI 安装
2. 或者告诉我具体需要什么功能，我可以配置对应的 MCP 服务器
3. 当前配置已足够支持日常开发工作

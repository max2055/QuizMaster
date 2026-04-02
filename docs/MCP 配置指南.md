# MCP Skills 配置指南

## 已配置的 MCP Servers

本项目已配置以下 MCP 服务器：

### 1. Filesystem - 文件系统操作
**用途**: 安全地访问项目文件系统
**配置**: 已限定访问本项目目录
**使用方式**: 
- 自动在对话中可用
- 可以读取、搜索、编辑项目文件
- 无需额外配置

### 2. GitHub - GitHub 集成
**用途**: PR 审查、Issue 管理、代码审查
**需要配置**: 
1. 访问 https://github.com/settings/tokens
2. 创建 Personal Access Token (勾选 repo 范围)
3. 将 token 填入 `.mcp.json` 中的 `GITHUB_TOKEN`

**使用方式**:
```
/commit - 提交代码
/review-pr 123 - 审查 PR #123
```

### 3. Brave Search - 网络搜索
**用途**: 获取最新信息、文档查询
**需要配置**:
1. 访问 https://brave.com/search/api/
2. 获取 API Key
3. 填入 `.mcp.json` 中的 `BRAVE_API_KEY`

**使用方式**:
- 自动用于查询最新文档和信息
- 也可通过 `/search` 命令手动触发

### 4. Memory - 长期记忆
**用途**: 跨会话记忆用户偏好和项目信息
**使用方式**:
- 自动保存和读取记忆
- 无需手动操作

## 安装步骤

### 前置要求
1. 确保已安装 Node.js (v18+)
2. 确保已安装 npm

### 快速安装

```bash
# 1. 验证 Node.js 安装
node --version

# 2. 安装 MCP 服务器（自动）
# 首次使用时，Claude Code 会自动通过 npx 安装

# 3. 配置 GitHub Token (可选)
# 编辑 .mcp.json 文件，填入你的 GITHUB_TOKEN
```

### 手动安装 MCP 服务器

```bash
# 全局安装（可选）
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-memory
```

## 常用 Skill 用法示例

### 使用 GitHub Skill
```
用户：审查 PR #42
AI: 使用 MCP GitHub 服务器获取 PR 详情...
```

### 使用 Search Skill
```
用户：查找 PyQt6 最新的文档
AI: 使用 Brave Search 搜索最新文档...
```

### 使用 Filesystem Skill
```
用户：检查项目中的所有 Python 文件
AI: 使用 Filesystem MCP 搜索项目文件...
```

## 故障排查

### 技能未加载
1. 检查 `.mcp.json` 语法是否正确
2. 重启 Claude Code
3. 运行 `claude -mcp list` 查看已加载的服务器

### 认证错误
- GitHub: 检查 token 是否有效
- Brave: 检查 API Key 是否正确

## 其他有用的 MCP 服务器

### Sequential Thinking - 顺序思考
```json
"sequential-thinking": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
}
```

### Git - Git 操作
```json
"git": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-git"]
}
```

### Puppeteer - 浏览器自动化
```json
"puppeteer": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
}
```

---

**注意**: 
- 首次使用某个 MCP 服务器时，npx 会自动下载并安装
- 敏感信息（如 API Keys）应妥善保管
- 可以使用 Claude 的 `/mcp` 命令查看服务器状态

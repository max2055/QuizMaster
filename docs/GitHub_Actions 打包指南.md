# GitHub Actions 打包指南

## 📦 自动打包流程

### 方法一：推送标签触发（推荐）

1. **推送标签到 GitHub**
   ```bash
   git tag v1.5.0
   git push origin v1.5.0
   ```

2. **等待构建完成**
   - 访问 https://github.com/你的用户名/QuizMaster/actions
   - 构建约需 5-10 分钟

3. **下载打包结果**
   - 点击完成的构建任务
   - 在底部"Artifacts"下载 `QuizMaster-Windows.zip`
   - 或创建 Release 后在 Release 页面下载

### 方法二：手动触发

1. 访问 https://github.com/你的用户名/QuizMaster/actions
2. 选择"Build Windows Executable"工作流
3. 点击"Run workflow"
4. 选择分支（通常为 main）
5. 点击"Run workflow"按钮
6. 等待完成后下载

---

## 📥 用户使用方式

### 分发内容

打包后的 `QuizMaster_分发版` 文件夹包含：
```
QuizMaster_分发版/
├── QuizMaster.exe          # 主程序（约 35-50 MB）
├── quizmaster.db           # 数据库（含题库数据）
└── README_用户说明.txt     # 使用说明
```

### 用户使用步骤

1. **解压文件**
   - 用户下载 `QuizMaster.zip`
   - 解压到任意位置（如桌面、D 盘）

2. **双击运行**
   - 双击 `QuizMaster.exe` 即可启动
   - **无需安装** Python 或其他运行环境
   - **无需安装**任何依赖包

3. **数据存储**
   - 所有答题记录保存在 `quizmaster.db` 文件
   - 数据库与程序在同一文件夹
   - 用户可备份该文件保存数据

---

## ⚠️ 重要说明

### 数据库打包

**确认事项**：
- ✅ 数据库文件 `quizmaster.db` 已添加到 `QuizMaster.spec` 的 `datas` 配置
- ✅ GitHub Actions 工作流会复制数据库到分发文件夹
- ✅ 用户下载后数据库与 exe 在同一文件夹

### 数据库位置说明

程序运行时会自动查找同目录下的 `quizmaster.db`：

```python
# 数据库路径会自动设置为程序所在目录
db_path = os.path.join(os.path.dirname(sys.executable), 'quizmaster.db')
```

用户无需担心路径问题，双击即用。

---

## 🔧 常见问题

### Q1: 用户下载后需要安装什么？
**A**: 什么都不需要！双击 `QuizMaster.exe` 直接运行。

### Q2: 杀毒软件报毒怎么办？
**A**: PyInstaller 打包的 exe 可能被误报。
- 告诉用户添加到杀毒软件白名单
- 或在 GitHub Release 中说明这是安全文件

### Q3: 用户如何更新题库？
**A**: 
1. 你在本地更新题库
2. 重新推送标签触发打包
3. 发送新的 `QuizMaster.zip` 给用户
4. 用户替换旧的 `quizmaster.db` 即可

### Q4: 用户的答题记录会丢失吗？
**A**: 
- 答题记录保存在 `quizmaster.db`
- 只要不删除该文件，记录就不会丢失
- 建议用户定期备份该文件

---

## 📊 构建产物说明

### GitHub Actions 生成的文件

| 文件 | 说明 | 获取方式 |
|------|------|----------|
| `QuizMaster-Windows.zip` | 自动打包的压缩包 | Actions Artifacts 或 Release |
| `QuizMaster.exe` | Windows 可执行文件 | 压缩包内 |
| `quizmaster.db` | 题库数据库 | 压缩包内 |

### Artifact 下载期限

- GitHub Actions 的 Artifacts 保留 **90 天**
- 超过期限后自动删除
- 建议及时下载并保存到自己的存储

### 永久分发方式

1. 创建 GitHub Release
2. 将 zip 文件上传到 Release 附件
3. Release 附件永久保存
4. 用户可从 Release 页面下载

---

## 🚀 快速开始

### 你现在可以：

1. **推送到 GitHub**
   ```bash
   git add .
   git commit -m "准备发布 v1.5.0"
   git push origin main
   ```

2. **推送标签触发打包**
   ```bash
   git tag v1.5.0
   git push origin v1.5.0
   ```

3. **访问 Actions 页面查看进度**
   https://github.com/你的用户名/QuizMaster/actions

---

**版本**: v1.5.0  
**最后更新**: 2026-04-02

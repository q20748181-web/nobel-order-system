# GitHub 账号设置和代码推送 - 详细教程

## 🎯 这一步做什么？

把您的本地代码推送到 GitHub，这样才能部署到 Streamlit Cloud。

---

## 📋 前置检查

### 检查1：您有 GitHub 账号吗？

**方法A：检查是否有账号**
1. 访问：https://github.com/login
2. 如果能登录，说明有账号
3. 记住您的用户名（登录后点击头像就能看到）

**方法B：如果没有账号**
1. 访问：https://github.com/signup
2. 按照提示注册（免费）
3. 注册完成后，记住您的用户名

---

## 🚀 完整步骤（图文并茂）

### 第一步：创建 GitHub 仓库

#### 1.1 打开创建页面
在浏览器访问：https://github.com/new

#### 1.2 填写仓库信息

```
┌─────────────────────────────────────────────────┐
│  Create a new repository                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  Repository name *                              │
│  ┌───────────────────────────────────────┐     │
│  │ nobel-order-system                    │     │
│  └───────────────────────────────────────┘     │
│  Great repository names are short and          │
│  memorable.                                   │
│                                                 │
│  Description (optional)                        │
│  ┌───────────────────────────────────────┐     │
│  │ Nobel订单管理系统                     │     │
│  └───────────────────────────────────────┘     │
│                                                 │
│  Public  ○ Private                             │
│                                                 │
│  ❌ Add a README file                          │
│  ❌ Add .gitignore                             │
│  ❌ Choose a license                           │
│                                                 │
│          [ Create repository ]                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

**重要提示**：
- ✅ 仓库名：`nobel-order-system`（或您喜欢的名字）
- ✅ 可见性：选择 **Private**（私有）
- ❌ **不要勾选**任何选项

#### 1.3 点击创建
点击绿色的 "Create repository" 按钮

#### 1.4 创建成功
页面会显示类似这样的内容：

```
Quick setup — if you've done this kind of thing before

HTTPS
https://github.com/你的用户名/nobel-order-system.git

We recommend every repository include a README, LICENSE, and .gitignore.

…or create a new repository on the command line

echo "# nobel-order-system" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/你的用户名/nobel-order-system.git
git push -u origin main

…or push an existing repository from the command line

git remote add origin https://github.com/你的用户名/nobel-order-system.git
git branch -M main
git push -u origin main
```

**复制这个 URL**：
```
https://github.com/你的用户名/nobel-order-system.git
```

---

### 第二步：获取 GitHub Token（用于密码）

#### 2.1 访问 Token 设置页面
登录 GitHub 后，访问：https://github.com/settings/tokens

#### 2.2 生成新 Token
1. 点击 "Generate new token (classic)"
2. 填写信息：
   - Note（备注）：`nobel-order-system`
   - Expiration（过期时间）：选择 `90 days` 或 `No expiration`
   - ✅ 勾选 **repo**（一定要勾选！）
3. 点击页面底部的 "Generate token"

#### 2.3 复制 Token
页面会显示一个很长的字符串，例如：
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ 重要：这个 Token 只显示一次，务必复制并保存！**

---

### 第三步：在终端执行命令

#### 3.1 打开终端
在项目目录打开终端

#### 3.2 执行以下命令

```bash
# 1. 确保在项目目录
cd /workspace/projects

# 2. 添加远程仓库（替换成你的用户名）
git remote add origin https://github.com/你的用户名/nobel-order-system.git

# 3. 查看远程仓库（确认配置正确）
git remote -v

# 4. 推送代码到 GitHub
git push -u origin main
```

#### 3.3 输入用户名和密码

当执行 `git push` 时：

```
Username for 'https://github.com': 【输入您的 GitHub 用户名】
Password for 'https://你的用户名@github.com': 【粘贴您的 Token】
```

**注意**：
- 用户名：输入 GitHub 用户名
- 密码：粘贴刚才生成的 Token（不是登录密码）

#### 3.4 等待推送完成

看到类似以下输出说明成功：
```
Enumerating objects: 150, done.
Counting objects: 100% (150/150), done.
Delta compression using up to 8 threads
Compressing objects: 100% (120/120), done.
Writing objects: 100% (150/150), 50.00 KiB | 2.00 MiB/s, done.
Total 150 (delta 30), reused 0 (delta 0)
To https://github.com/你的用户名/nobel-order-system.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

---

## ✅ 验证是否成功

### 方法1：在 GitHub 网站查看
1. 访问：https://github.com/你的用户名/nobel-order-system
2. 如果能看到代码文件，说明推送成功！

### 方法2：在终端检查
```bash
git status
```
应该显示：
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## ❓ 常见问题

### Q1: 提示 "remote origin already exists"
**A**: 说明已经配置过远程仓库，先删除再添加：
```bash
git remote remove origin
git remote add origin https://github.com/你的用户名/nobel-order-system.git
```

### Q2: 提示 "Authentication failed"
**A**:
1. 确认使用的是 Token，不是密码
2. 确认 Token 有 `repo` 权限
3. 尝试重新生成 Token

### Q3: 提示 "refusing to merge unrelated histories"
**A**: 强制推送（谨慎使用）：
```bash
git push -u origin main --force
```

### Q4: 我看不到仓库名在 URL 中的用户名部分
**A**: 访问您的 GitHub 个人主页，点击头像查看用户名

### Q5: 推送后 GitHub 网站看不到文件
**A**:
1. 刷新浏览器页面
2. 确认推送成功
3. 检查是否推送到正确的分支（main）

---

## 💡 快速参考

### 命令速查

```bash
# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 查看远程仓库
git remote -v

# 删除远程仓库
git remote remove origin

# 推送代码
git push -u origin main

# 强制推送（谨慎使用）
git push -u origin main --force
```

### 重要链接

- 创建仓库：https://github.com/new
- Token 设置：https://github.com/settings/tokens
- 您的仓库：https://github.com/你的用户名/nobel-order-system

---

## 🎯 下一步

推送成功后，就可以在 Streamlit Cloud 部署了！

下一步教程：Streamlit Cloud 部署

---

## 🆘 需要帮助？

如果遇到问题，请提供以下信息：

1. 执行的命令
2. 错误提示信息
3. 您的 GitHub 用户名

我会帮您解决！

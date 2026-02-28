# Nobel订单管理系统 - Streamlit Cloud 完整部署指南

## 🚀 快速部署（5分钟完成）

---

## 📋 前置准备

### 1. 准备 GitHub 账号
- 如果没有，先注册：https://github.com/signup
- 确保账号状态正常

### 2. 准备 Supabase 凭证
从 Supabase 控制台获取：
- Project URL
- anon key
- service_role key

获取步骤：
1. 访问 https://app.supabase.com/
2. 选择你的项目
3. 进入 "Settings" → "API"
4. 复制上述三个值

---

## 🎯 部署步骤（5步完成）

### Step 1: 创建 GitHub 仓库（1分钟）

#### 1.1 访问 GitHub 创建页面
打开浏览器，访问：
```
https://github.com/new
```

#### 1.2 填写仓库信息
- **Repository name**: `nobel-order-system`
- **Description**: Nobel订单管理系统 - 基于Streamlit的橱柜订单管理系统
- **Visibility**: Private（推荐）或 Public
- **其他选项**: 保持默认（不要勾选）

#### 1.3 点击 "Create repository"

**重要**：创建后，复制仓库的URL，类似：
```
https://github.com/你的用户名/nobel-order-system.git
```

---

### Step 2: 配置远程仓库并推送代码（2分钟）

在终端执行以下命令：

```bash
cd /workspace/projects

# 添加远程仓库（替换为你的仓库URL）
git remote add origin https://github.com/你的用户名/nobel-order-system.git

# 推送代码到 GitHub
git push -u origin main
```

**注意**：
- 如果提示输入用户名和密码，请使用 GitHub 的 Personal Access Token（不是登录密码）
- 如何获取 Token：https://github.com/settings/tokens

**获取 Personal Access Token 的步骤**：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 点击 "Generate token"
5. 复制生成的 token（只显示一次）

---

### Step 3: 在 Streamlit Cloud 部署（1分钟）

#### 3.1 访问 Streamlit Cloud
打开浏览器，访问：
```
https://share.streamlit.io/
```

#### 3.2 登录 GitHub
1. 点击 "Sign in with GitHub"
2. 授权 Streamlit 访问你的仓库

#### 3.3 创建新应用
1. 点击右上角的 "New app"
2. 填写配置：
   - **Repository**: 选择 `nobel-order-system`（或你的仓库名）
   - **Branch**: 选择 `main`（或 `master`）
   - **Main file path**: 输入 `src/app_server.py`
3. 点击 "Advanced settings" 展开高级选项
4. 确保 "Python version" 选择 `3.10` 或更高
5. 点击 "Deploy"

---

### Step 4: 配置环境变量（30秒）

部署页面会显示 "Secrets" 部分，点击展开，然后添加以下内容：

```toml
[supabase]
project_url = "你的 Supabase Project URL"
anon_key = "你的 Supabase anon key"
service_role_key = "你的 Supabase service role key"
```

**示例**：
```toml
[supabase]
project_url = "https://abc123.supabase.co"
anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**注意**：
- 引号要保留
- 每个值都要用双引号包裹
- 确保没有多余的空格或换行

添加后，点击 "Save changes"

Streamlit Cloud 会自动检测到配置变更并重新部署。

---

### Step 5: 等待部署完成并访问（1分钟）

#### 5.1 查看部署状态
在部署页面，你会看到：
- Building...（正在构建）
- Deploying...（正在部署）
- Running（运行中）

#### 5.2 访问应用
部署成功后，你会看到绿色的 "Running" 状态，以及一个类似这样的URL：

```
https://nobel-order-system.streamlit.app
```

**点击这个URL，即可访问你的应用！**

---

## ✅ 部署完成！

### 恭喜！🎉

你的 Nobel订单管理系统现在已经部署到 Streamlit Cloud，可以通过以下地址访问：

```
https://nobel-order-system.streamlit.app
```

---

## 🔄 如何更新应用

当你修改代码后，只需：

```bash
cd /workspace/projects
git add .
git commit -m "更新功能"
git push
```

Streamlit Cloud 会自动检测到新的提交并重新部署，通常需要1-3分钟。

---

## 📊 管理应用

### 访问管理面板
访问 https://share.streamlit.io/，登录后可以看到你的所有应用。

### 查看部署日志
在应用页面，点击 "Logs" 可以查看运行日志和错误信息。

### 配置环境变量
在应用页面，点击 "Settings" → "Secrets" 可以修改环境变量。

### 删除应用
在应用页面，点击 "Settings" → "Danger zone" → "Delete app"

---

## ❓ 常见问题

### Q1: 部署失败，提示 "Module not found"
**A**: 检查 `requirements.streamlit.txt` 是否包含所有必要的依赖。

### Q2: 数据库连接失败
**A**:
1. 检查 Supabase 配置是否正确
2. 确认 Project URL、anon key、service_role key 都正确
3. 检查 Supabase 服务是否正常运行

### Q3: 访问应用显示空白
**A**:
1. 查看部署日志是否有错误
2. 检查主文件路径是否正确（`src/app_server.py`）
3. 确认代码语法没有错误

### Q4: 推送代码时提示 "Authentication failed"
**A**:
1. 检查是否使用了正确的 GitHub 用户名和密码（或Token）
2. 确认 Personal Access Token 有 `repo` 权限
3. 尝试重新生成 Token

### Q5: 如何配置自定义域名？
**A**:
1. 在 Streamlit Cloud 控制台
2. 点击 "Settings" → "Custom domains"
3. 添加你的域名
4. 按照提示配置 DNS 记录

### Q6: 如何限制访问权限？
**A**:
Streamlit Cloud 本身不提供密码保护，但可以在代码中添加登录验证。

---

## 📝 代码示例：添加访问密码

如果需要密码保护，可以在 `src/app_server.py` 开头添加：

```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "你的密码":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 清除密码
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.text_input("请输入访问密码", type="password",
                      on_change=password_entered, key="password")
        st.stop()  # 停止执行

check_password()
```

---

## 🎯 最佳实践

### 1. 使用 Git 分支
- 在 `main` 分支发布生产版本
- 在 `dev` 分支开发新功能
- 使用 Pull Request 进行代码审查

### 2. 环境变量管理
- 敏感信息（如API密钥）使用环境变量
- 不要在代码中硬编码密钥

### 3. 日志记录
- 使用 `st.write()` 输出调试信息
- 生产环境可以注释掉或使用日志级别控制

### 4. 性能优化
- 使用 `@st.cache_data` 缓存数据
- 避免频繁的数据库查询
- 使用分页加载数据

---

## 📚 相关文档

- Streamlit Cloud 官方文档：https://docs.streamlit.io/streamlit-cloud
- GitHub 文档：https://docs.github.com/
- Supabase 文档：https://supabase.com/docs

---

## 🎉 总结

**部署到 Streamlit Cloud 的优势**：
- ✅ 完全免费
- ✅ 3分钟部署
- ✅ 固定URL
- ✅ 自动HTTPS
- ✅ 全球CDN
- ✅ 自动更新
- ✅ 零维护

**推荐指数：⭐⭐⭐⭐⭐**

---

**祝您部署顺利！** 🚀

如有任何问题，请查看 Streamlit Cloud 控制台的日志或联系技术支持。

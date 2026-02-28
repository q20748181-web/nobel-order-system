# Streamlit Cloud 部署指南

## 最简单的部署方案 - 免费，3分钟完成

---

## 📋 前置准备

### 1. 准备 GitHub 账号
如果没有，先注册：https://github.com/signup

### 2. 准备 Supabase 凭证
- Project URL
- anon key
- service_role key

从 Supabase 控制台获取：Settings → API

---

## 🚀 部署步骤

### Step 1: 创建 Git 仓库

在项目目录执行：

```bash
cd /workspace/projects
git init
git add .
git commit -m "Initial commit - Nobel订单管理系统"
```

### Step 2: 推送到 GitHub

#### 2.1 在 GitHub 创建新仓库
1. 访问 https://github.com/new
2. 仓库名：`nobel-order-system`
3. 选择 Public 或 Private（推荐 Private）
4. 点击 "Create repository"

#### 2.2 推送代码

复制 GitHub 提供的命令并执行：

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/nobel-order-system.git

# 推送代码
git branch -M main
git push -u origin main
```

### Step 3: 创建 .streamlit 配置文件

```bash
cd /workspace/projects
mkdir -p .streamlit
```

创建 `.streamlit/config.toml`：

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200
```

### Step 4: 创建 secrets.toml（本地配置）

**注意：这个文件不会被提交到 Git**

```bash
cd /workspace/projects
touch .streamlit/secrets.toml
```

编辑内容：

```toml
[supabase]
project_url = "你的 Supabase Project URL"
anon_key = "你的 Supabase anon key"
service_role_key = "你的 Supabase service role key"
```

### Step 5: 添加 requirements.txt

确保项目根目录有 `requirements.txt`：

```txt
streamlit
supabase
pandas
openpyxl
```

### Step 6: 提交并推送

```bash
git add .
git commit -m "Add deployment config"
git push
```

### Step 7: 部署到 Streamlit Cloud

#### 7.1 访问 Streamlit Cloud
https://share.streamlit.io/

#### 7.2 登录并授权
- 使用 GitHub 账号登录
- 授权 Streamlit 访问你的仓库

#### 7.3 创建新应用
1. 点击 "New app"
2. 选择仓库：`nobel-order-system`
3. 选择分支：`main`
4. 主文件路径：`src/app_server.py`
5. 点击 "Deploy"

#### 7.6 配置环境变量（重要！）

在 "Secrets" 部分添加：

```toml
[supabase]
project_url = "你的 Supabase Project URL"
anon_key = "你的 Supabase anon key"
service_role_key = "你的 Supabase service role key"
```

### Step 8: 等待部署

大约需要 1-3 分钟，你会看到：

```
✅ Your app is running!
🌐 URL: https://nobel-order-system.streamlit.app
```

---

## 🎉 完成！

### 你的应用现在可以访问了：

**固定地址**：`https://nobel-order-system.streamlit.app`

**特点**：
- ✅ 免费
- ✅ 固定 URL
- ✅ 自动 HTTPS
- ✅ 全球访问
- ✅ 自动更新（推送代码后）

---

## 🔄 更新应用

修改代码后：

```bash
git add .
git commit -m "Update feature"
git push
```

Streamlit Cloud 会自动检测并重新部署！

---

## 📊 管理应用

访问管理面板：
https://share.streamlit.io/

可以：
- 查看访问日志
- 查看错误信息
- 配置环境变量
- 管理多个应用

---

## ❓ 常见问题

### Q1: 部署失败怎么办？

**A**: 查看部署日志，检查：
- `requirements.txt` 是否正确
- 主文件路径是否正确
- 环境变量是否配置

### Q2: 数据库连接失败？

**A**: 检查 Supabase 配置：
- Project URL 是否正确
- API Key 是否正确
- Supabase 服务是否运行

### Q3: 如何配置自定义域名？

**A**:
1. 在 Streamlit Cloud 管理面板
2. 点击 "Settings" → "Custom domains"
3. 添加你的域名
4. 配置 DNS 记录

### Q4: 如何设置访问密码？

**A**:
Streamlit Cloud 本身不提供密码功能，但可以在应用中添加：

```python
import streamlit as st

# 在 app_server.py 开头添加
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

## 📝 总结

**Streamlit Cloud 是最佳选择**，因为：
- ✅ 完全免费
- ✅ 3分钟部署
- ✅ 固定URL
- ✅ 自动HTTPS
- ✅ 全球CDN加速
- ✅ 无需维护服务器

**推荐指数：⭐⭐⭐⭐⭐**

---

## 🎯 下一步

1. 准备 GitHub 仓库
2. 推送代码
3. 部署到 Streamlit Cloud
4. 分享固定 URL 给同事

**需要我帮你准备部署脚本吗？**

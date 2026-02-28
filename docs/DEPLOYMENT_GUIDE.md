# Nobel订单管理系统 - 部署方案总结

## 🎯 推荐方案对比

| 方案 | 难度 | 费用 | 时间 | 稳定性 | 推荐度 | 适用场景 |
|------|------|------|------|--------|--------|----------|
| **Streamlit Cloud** | ⭐ 免费 | 3分钟 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 快速体验、小团队 |
| **云服务器** | ⭐⭐⭐ 50-100元/月 | 10-30分钟 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 长期使用、需要固定地址 |
| **当前服务器+隧道** | ⭐⭐ 免费 | 5分钟 | ⭐⭐ | ⭐⭐ | 临时测试 |

---

## 🚀 方案1：Streamlit Cloud（强烈推荐）

### 为什么推荐？

✅ **完全免费** - 无需任何费用
✅ **3分钟部署** - 最快部署方式
✅ **固定URL** - 不会变化
✅ **自动HTTPS** - 无需配置
✅ **全球CDN** - 访问速度快
✅ **自动更新** - 推送代码自动部署
✅ **无需维护** - 完全托管

### 部署步骤

1. **准备代码**
   ```bash
   cd /workspace/projects
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **推送到 GitHub**
   - 在 GitHub 创建仓库：`nobel-order-system`
   - 推送代码：
   ```bash
   git remote add origin https://github.com/你的用户名/nobel-order-system.git
   git push -u origin main
   ```

3. **部署到 Streamlit Cloud**
   - 访问：https://share.streamlit.io/
   - 登录 GitHub 账号
   - 点击 "New app"
   - 选择仓库和分支
   - 主文件路径：`src/app_server.py`
   - 点击 "Deploy"

4. **配置环境变量**
   在部署页面添加 Secrets：
   ```toml
   [supabase]
   project_url = "你的 Supabase Project URL"
   anon_key = "你的 Supabase anon key"
   service_role_key = "你的 Supabase service role key"
   ```

5. **等待部署完成**
   - 1-3分钟后，你会看到：
   ```
   ✅ Your app is running!
   🌐 URL: https://nobel-order-system.streamlit.app
   ```

### 优缺点

**优点：**
- ✅ 零成本
- ✅ 零配置
- ✅ 自动 HTTPS
- ✅ 全球访问
- ✅ 自动备份
- ✅ 易于分享

**缺点：**
- ❌ 资源有限（CPU、内存）
- ❌ 不适合大量并发用户
- ❌ 数据库需要外部配置

### 详细文档

📖 完整指南：[docs/DEPLOY_STREAMLIT_CLOUD.md](docs/DEPLOY_STREAMLIT_CLOUD.md)

---

## 🏢 方案2：云服务器部署（长期稳定）

### 为什么选择？

✅ **高性能** - 专属资源，速度快
✅ **固定IP** - 可以配置域名
✅ **完全控制** - 可以安装任何软件
✅ **可扩展** - 随时升级配置
✅ **数据安全** - 自己控制数据
✅ **24/7运行** - 不受限制

### 推荐配置

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| CPU | 2核 | 足够运行 |
| 内存 | 4GB | Python需要较多内存 |
| 带宽 | 5Mbps | 满足小团队 |
| 系统 | Ubuntu 22.04 | 稳定易用 |
| 硬盘 | 40GB SSD | 足够存储 |
| 费用 | 50-100元/月 | 按需选择 |

### 部署步骤

#### 自动化部署（推荐）

1. **购买云服务器**
   - 阿里云：https://www.aliyun.com/product/ecs
   - 腾讯云：https://cloud.tencent.com/product/cvm
   - 华为云：https://www.huaweicloud.com/product/cvm

2. **连接服务器**
   ```bash
   ssh root@你的公网IP
   # 输入密码
   ```

3. **上传部署脚本**
   ```bash
   # 在本地执行
   scp scripts/deploy_to_server.sh root@你的公网IP:/root/
   scp scripts/setup_ssl.sh root@你的公网IP:/root/
   ```

4. **运行部署脚本**
   ```bash
   # 在服务器上执行
   bash /root/deploy_to_server.sh
   ```

5. **上传代码**
   ```bash
   # 方式1：使用 Git
   git clone https://github.com/你的用户名/nobel-order-system.git /opt/nobel-order-system

   # 方式2：手动上传
   scp -r /workspace/projects/* root@你的公网IP:/opt/nobel-order-system/
   ```

6. **重启服务**
   ```bash
   supervisorctl restart nobel-order-system
   ```

7. **（可选）配置 HTTPS**
   ```bash
   bash /root/setup_ssl.sh
   ```

### 手动部署

📖 完整指南：[docs/DEPLOY_CLOUD_SERVER.md](docs/DEPLOY_CLOUD_SERVER.md)

### 优缺点

**优点：**
- ✅ 高性能
- ✅ 完全控制
- ✅ 可扩展
- ✅ 固定IP
- ✅ 可配置域名
- ✅ 数据安全

**缺点：**
- ❌ 需要付费
- ❌ 需要维护
- ❌ 需要技术能力

---

## 🔌 方案3：隧道服务（临时使用）

### 适用场景

✅ 快速测试
✅ 临时分享
✅ 团队内部使用
✅ 无需固定URL

### 推荐方案

#### 1. Serveo（最简单）

```bash
# 在本地电脑执行
ssh -R 80:9.128.127.13:8501 serveo.net
```

等待显示外网地址：`https://abc123.serveo.net`

#### 2. Localtunnel（推荐）

```bash
# 安装
npm install -g localtunnel

# 启动
lt --port 8501 --subdomain nobel-orders
```

#### 3. Cloudflare Tunnel（最稳定）

```bash
# 注册：https://dash.cloudflare.com/sign-up
# 下载 cloudflared
# 运行
cloudflared tunnel --url http://9.128.127.13:8501
```

### 优缺点

**优点：**
- ✅ 免费
- ✅ 无需购买服务器
- ✅ 快速设置

**缺点：**
- ❌ URL不固定
- ❌ 速度较慢
- ❌ 不稳定
- ❌ 不适合长期使用

---

## 💰 成本对比

### 方案1：Streamlit Cloud
- **费用**：0元/月
- **总成本**：0元/年

### 方案2：云服务器
- **服务器**：50-100元/月
- **域名**：50-100元/年
- **总成本**：650-1300元/年

### 方案3：隧道服务
- **费用**：0元/月
- **总成本**：0元/年

---

## 🎯 我的推荐

### 如果你是：
👉 **小团队（<10人）**
- **推荐**：Streamlit Cloud
- **理由**：免费、简单、够用

👉 **中大型团队（>10人）**
- **推荐**：云服务器
- **理由**：性能好、可扩展、专业

👉 **临时测试**
- **推荐**：隧道服务
- **理由**：快速、免费、无需购买

---

## 📋 决策清单

回答以下问题，帮你选择最佳方案：

### 问题1：需要固定URL吗？
- ✅ 是 → 云服务器
- ❌ 否 → Streamlit Cloud 或 隧道

### 问题2：有多少用户？
- <10人 → Streamlit Cloud
- 10-50人 → 云服务器（基础配置）
- >50人 → 云服务器（高配置）

### 问题3：预算是多少？
- 0元 → Streamlit Cloud 或 隧道
- >500元/年 → 云服务器

### 问题4：有技术能力维护服务器吗？
- ✅ 有 → 云服务器
- ❌ 没有 → Streamlit Cloud

### 问题5：需要配置自定义域名吗？
- ✅ 是 → 云服务器
- ❌ 否 → Streamlit Cloud

---

## 🚀 快速决策

| 需求 | 推荐方案 | 立即开始 |
|------|----------|----------|
| 免费、快速 | Streamlit Cloud | [查看教程](docs/DEPLOY_STREAMLIT_CLOUD.md) |
| 固定地址、长期使用 | 云服务器 | [查看教程](docs/DEPLOY_CLOUD_SERVER.md) |
| 临时测试 | 隧道服务 | 运行 `python scripts/show_tunnel_solutions.py` |

---

## 📞 需要帮助？

### Streamlit Cloud 部署
- 📖 完整教程：[docs/DEPLOY_STREAMLIT_CLOUD.md](docs/DEPLOY_STREAMLIT_CLOUD.md)
- 🛠️ 官方文档：https://docs.streamlit.io/streamlit-cloud/get-started

### 云服务器部署
- 📖 完整教程：[docs/DEPLOY_CLOUD_SERVER.md](docs/DEPLOY_CLOUD_SERVER.md)
- 🛠️ 部署脚本：`scripts/deploy_to_server.sh`
- 🔐 HTTPS配置：`scripts/setup_ssl.sh`

### 隧道服务
- 📖 查看方案：`python scripts/show_tunnel_solutions.py`

---

## ✨ 总结

**最推荐：Streamlit Cloud**

理由：
- ✅ 完全免费
- ✅ 3分钟部署
- ✅ 固定URL
- ✅ 自动HTTPS
- ✅ 全球访问
- ✅ 零维护

**适合90%的使用场景！**

---

## 🎉 立即开始

### 选择 Streamlit Cloud（推荐）

1. 准备 GitHub 仓库
2. 推送代码
3. 访问 https://share.streamlit.io/
4. 点击 "Deploy"

**3分钟后，你的应用就可以访问了！**

### 选择云服务器

1. 购买云服务器（50-100元/月）
2. 连接服务器
3. 运行部署脚本：`bash scripts/deploy_to_server.sh`
4. 上传代码
5. 完成！

**10-30分钟后，你就有自己的固定地址了！**

---

**祝您部署顺利！🚀**

如有任何问题，请查看相应文档或联系技术支持。

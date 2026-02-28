# Nobel订单管理系统 - 快速使用教程

## 📋 目录
1. [服务状态](#服务状态)
2. [如何访问](#如何访问)
3. [外网访问方案](#外网访问方案)
4. [常见问题](#常见问题)

---

## 🔴 服务状态

### ✅ 当前运行状态
- **Streamlit服务**: 运行中
- **服务地址**: 
  - 内网访问: `http://9.128.127.13:8501`
  - 本地访问: `http://localhost:8501`
- **数据库**: Supabase 云端数据库
- **数据同步**: 实时同步（多用户可同时访问）

---

## 🌐 如何访问

### 方法1：内网访问（推荐）
如果您的电脑在同一个网络环境中，可以直接访问：

```
http://9.128.127.13:8501
```

### 方法2：本地测试
在服务器本机访问：

```
http://localhost:8501
```

---

## 🌍 外网访问方案

### ⚡ 方案A：使用 Serveo 隧道（最简单，无需下载）

**适用场景**: 临时需要外网访问，快速分享给同事

**步骤**：

1. **在您的本地电脑**（不是服务器上）打开终端或命令提示符

2. **输入以下命令**：
   ```bash
   ssh -R 80:9.128.127.13:8501 serveo.net
   ```

3. **等待连接建立**，会显示类似以下内容：
   ```
   Forwarding HTTP traffic from https://abc123.serveo.net
   Press Ctrl+C to stop
   ```

4. **复制显示的URL**（如 `https://abc123.serveo.net`）分享给您的同事

**注意**：
- 第一次使用需要接受SSH密钥（输入 `yes`）
- URL是临时的，关闭终端后会失效
- 如果显示连接失败，可能是SSH端口被防火墙阻挡

---

### 🚀 方案B：使用 Localtunnel（简单，需安装Node.js）

**适用场景**: 希望有更稳定的临时URL

**步骤**：

1. **安装 Node.js**（如果已安装可跳过）
   - 访问 https://nodejs.org/ 下载安装

2. **安装 localtunnel**：
   ```bash
   npm install -g localtunnel
   ```

3. **启动隧道**：
   ```bash
   lt --port 8501 --subdomain nobel-orders
   ```

4. **复制显示的URL**分享给同事

**优点**：
- 可以指定子域名（更专业）
- 支持HTTPS
- 免费使用

---

### ☁️ 方案C：部署到云服务器（长期稳定，推荐）

**适用场景**: 需要长期使用，希望有固定的访问地址

**推荐云服务商**：
- 阿里云（https://www.aliyun.com）
- 腾讯云（https://cloud.tencent.com）
- 华为云（https://www.huaweicloud.com）

**基本配置建议**：
- CPU: 2核
- 内存: 4GB
- 带宽: 5Mbps
- 系统: Ubuntu 20.04 或 22.04
- 费用: 约 50-100元/月

**部署步骤**：

1. **购买云服务器**并获取登录信息

2. **连接到服务器**：
   ```bash
   ssh root@your_server_ip
   ```

3. **安装 Python 环境**：
   ```bash
   apt update
   apt install -y python3 python3-pip
   ```

4. **安装依赖**：
   ```bash
   pip3 install streamlit supabase pandas
   ```

5. **上传项目文件**：
   ```bash
   scp -r /workspace/projects root@your_server_ip:/root/
   ```

6. **启动服务**：
   ```bash
   cd /root/projects
   nohup streamlit run src/app_server.py --server.port 8501 --server.address 0.0.0.0 &
   ```

7. **访问您的服务**：
   ```
   http://your_server_ip:8501
   ```

**可选：配置域名和HTTPS**
- 购买域名（阿里云、腾讯云等）
- 使用 Nginx 配置反向代理
- 使用 Let's Encrypt 配置免费SSL证书

---

### 🔐 方案D：使用 Cloudflare Tunnel（稳定，免费）

**适用场景**: 需要稳定的免费隧道服务

**步骤**：

1. **注册 Cloudflare 账号**（免费）
   - 访问 https://dash.cloudflare.com/sign-up

2. **下载 cloudflared**：
   - 访问 https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
   - 根据您的操作系统下载对应版本

3. **安装 cloudflared**

4. **启动隧道**：
   ```bash
   cloudflared tunnel --url http://localhost:8501
   ```

5. **复制显示的URL**分享给同事

**优点**：
- 完全免费
- 速度快，稳定性好
- 可以使用自己的域名
- 自动HTTPS

---

## 📖 使用指南

### 登录系统
1. 访问系统地址
2. 输入您的用户名和密码
3. 点击"登录"

### 基本操作
- **客户管理**: 添加、编辑、查看客户信息
- **订单管理**: 创建订单、添加打样、生成报价
- **数据同步**: 所有操作实时保存到云端数据库
- **数据导出**: 导出订单数据为Excel或CSV

### 多用户协作
- 不同用户可以同时登录
- 实时看到其他用户的操作
- 数据自动同步，无需刷新页面

---

## ❓ 常见问题

### Q1: 服务无法访问怎么办？
**A**: 
1. 检查服务是否运行：
   ```bash
   ps aux | grep streamlit
   ```
2. 如果未运行，启动服务：
   ```bash
   cd /workspace/projects
   bash scripts/start_server.sh
   ```
3. 检查防火墙是否开放8501端口

### Q2: 数据不同步怎么办？
**A**:
1. 检查 Supabase 数据库连接是否正常
2. 检查浏览器控制台是否有错误信息
3. 刷新页面重新加载

### Q3: 外网访问速度慢怎么办？
**A**:
1. 尝试使用其他隧道服务（如 Cloudflare Tunnel）
2. 考虑部署到云服务器以获得更好的性能
3. 检查网络连接是否稳定

### Q4: 如何备份数据？
**A**:
- 所有数据已保存在 Supabase 云端数据库
- 可通过 Supabase 控制台导出数据
- 建议定期导出重要数据到本地

### Q5: 如何重置密码？
**A**:
- 联系系统管理员
- 或修改 `src/app_server.py` 中的用户信息

### Q6: 服务崩溃了怎么办？
**A**:
1. 重启服务：
   ```bash
   cd /workspace/projects
   bash scripts/start_server.sh
   ```
2. 查看日志：
   ```bash
   tail -f /tmp/streamlit.log
   ```
3. 如果问题持续，联系技术支持

---

## 📞 技术支持

如果遇到问题，可以：
1. 查看日志文件：`/tmp/streamlit.log`
2. 检查服务状态：`python scripts/show_tunnel_solutions.py`
3. 联系系统管理员

---

## 🔄 服务管理

### 启动服务
```bash
cd /workspace/projects
bash scripts/start_server.sh
```

### 停止服务
```bash
pkill -f "streamlit run src/app_server.py"
```

### 重启服务
```bash
pkill -f "streamlit run src/app_server.py"
cd /workspace/projects
bash scripts/start_server.sh
```

### 查看日志
```bash
tail -f /tmp/streamlit.log
```

---

## 📝 更新日志

### 2024-01-XX
- ✅ 完成 Streamlit 后端服务
- ✅ 集成 Supabase 云端数据库
- ✅ 实现多用户数据同步
- ✅ 添加外网访问方案文档

---

**祝您使用愉快！** 🎉

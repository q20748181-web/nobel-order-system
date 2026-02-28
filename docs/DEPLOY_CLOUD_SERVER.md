# 云服务器部署指南（阿里云/腾讯云）

## 最稳定的部署方案 - 50-100元/月

---

## 📋 前置准备

### 1. 购买云服务器

#### 推荐配置

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| CPU | 2核 | 足够运行Streamlit |
| 内存 | 4GB | Python需要较多内存 |
| 带宽 | 5Mbps | 满足小团队访问 |
| 系统 | Ubuntu 22.04 LTS | 稳定且易用 |
| 硬盘 | 40GB SSD | 足够存储数据 |
| 费用 | 约 50-100元/月 | 按需选择 |

#### 推荐服务商

1. **阿里云**：https://www.aliyun.com/product/ecs
2. **腾讯云**：https://cloud.tencent.com/product/cvm
3. **华为云**：https://www.huaweicloud.com/product/cvm

### 2. 准备域名（可选）

- 阿里云域名：https://wanwang.aliyun.com/
- 腾讯云域名：https://dnspod.cloud.tencent.com/

---

## 🚀 部署步骤

### Step 1: 连接服务器

购买后，你会收到：
- 公网IP地址（如：123.45.67.89）
- 用户名（通常是 root）
- 密码或SSH密钥

连接方式：

#### 方式A：使用密码连接
```bash
ssh root@你的公网IP
# 输入密码
```

#### 方式B：使用SSH密钥连接
```bash
ssh -i 你的密钥.pem root@你的公网IP
```

### Step 2: 更新系统

```bash
# 更新软件包列表
apt update

# 升级系统
apt upgrade -y
```

### Step 3: 安装必要软件

```bash
# 安装 Python 3 和 pip
apt install -y python3 python3-pip python3-venv

# 安装 Git
apt install -y git

# 安装 Nginx（用于反向代理）
apt install -y nginx

# 安装 Supervisor（进程管理）
apt install -y supervisor
```

### Step 4: 创建项目目录

```bash
# 创建项目目录
mkdir -p /opt/nobel-order-system

# 进入目录
cd /opt/nobel-order-system
```

### Step 5: 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### Step 6: 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install streamlit supabase pandas openpyxl
```

### Step 7: 上传代码

#### 方式A：使用 Git（推荐）
```bash
# 如果代码在 GitHub
git clone https://github.com/你的用户名/nobel-order-system.git .
```

#### 方式B：手动上传
```bash
# 在本地电脑打包代码
cd /workspace/projects
tar -czf nobel-order-system.tar.gz \
    src/ \
    config/ \
    requirements.txt \
    scripts/

# 使用 scp 上传
scp nobel-order-system.tar.gz root@你的公网IP:/opt/

# 在服务器上解压
cd /opt
tar -xzf nobel-order-system.tar.gz -C /opt/nobel-order-system/
```

### Step 8: 配置 Streamlit

```bash
# 创建配置目录
mkdir -p /opt/nobel-order-system/.streamlit
```

创建配置文件 `/opt/nobel-order-system/.streamlit/config.toml`：

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

### Step 9: 配置环境变量

```bash
# 创建环境变量文件
cat > /opt/nobel-order-system/.streamlit/secrets.toml << EOF
[supabase]
project_url = "你的 Supabase Project URL"
anon_key = "你的 Supabase anon key"
service_role_key = "你的 Supabase service role key"
EOF
```

### Step 10: 配置 Supervisor（确保服务持续运行）

创建配置文件 `/etc/supervisor/conf.d/nobel-order-system.conf`：

```ini
[program:nobel-order-system]
command=/opt/nobel-order-system/venv/bin/streamlit run src/app_server.py --server.port=8501 --server.address=127.0.0.1
directory=/opt/nobel-order-system
user=root
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/nobel-order-system.err.log
stdout_logfile=/var/log/nobel-order-system.out.log
environment=HOME="/root",USER="root"
```

### Step 11: 启动服务

```bash
# 重新加载 Supervisor 配置
supervisorctl reread

# 更新 Supervisor 配置
supervisorctl update

# 启动服务
supervisorctl start nobel-order-system

# 查看状态
supervisorctl status
```

### Step 12: 配置 Nginx 反向代理

创建 Nginx 配置文件 `/etc/nginx/sites-available/nobel-order-system`：

```nginx
server {
    listen 80;
    server_name 你的域名或IP;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
# 启用站点
ln -s /etc/nginx/sites-available/nobel-order-system /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

### Step 13: 开放防火墙端口

```bash
# 如果使用 UFW
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 如果使用 iptables
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
service iptables save
```

### Step 14: 配置云服务器安全组

**重要！** 必须在云服务商控制台配置安全组规则：

- 开放端口：80（HTTP）
- 开放端口：443（HTTPS）
- 可选：开放端口：8501（直接访问，不推荐）

---

## 🔐 Step 15: 配置 HTTPS（可选，推荐）

### 使用 Let's Encrypt 免费证书

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 获取证书（自动配置 Nginx）
certbot --nginx -d 你的域名

# 按提示操作
```

配置文件会自动更新为：

```nginx
server {
    listen 443 ssl;
    server_name 你的域名;

    ssl_certificate /etc/letsencrypt/live/你的域名/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/你的域名/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name 你的域名;
    return 301 https://$server_name$request_uri;
}
```

---

## 🎉 完成！

### 访问地址

- HTTP: `http://你的公网IP` 或 `http://你的域名`
- HTTPS: `https://你的域名`（如果配置了）

### 管理服务

```bash
# 查看服务状态
supervisorctl status nobel-order-system

# 重启服务
supervisorctl restart nobel-order-system

# 停止服务
supervisorctl stop nobel-order-system

# 查看日志
tail -f /var/log/nobel-order-system.out.log
```

---

## 🔄 更新应用

```bash
# 拉取最新代码
cd /opt/nobel-order-system
git pull

# 重启服务
supervisorctl restart nobel-order-system
```

---

## 📊 监控与维护

### 查看系统资源

```bash
# CPU和内存
htop

# 磁盘使用
df -h

# 网络连接
netstat -tlnp
```

### 日志管理

```bash
# Streamlit 日志
tail -f /var/log/nobel-order-system.out.log

# Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Supervisor 日志
tail -f /var/log/supervisor/supervisord.log
```

---

## 📝 备份策略

### 备份数据库

```bash
# 创建备份脚本
cat > /opt/backup-supabase.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/supabase"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份 Supabase 数据（如果可访问）
pg_dump -h 你的 Supabase 主机 -U postgres -d 你的数据库名 > $BACKUP_DIR/backup_$DATE.sql

# 保留最近7天的备份
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
EOF

chmod +x /opt/backup-supabase.sh

# 添加到 crontab（每天凌晨2点备份）
crontab -e
# 添加：0 2 * * * /opt/backup-supabase.sh
```

### 备份代码

```bash
# 创建备份脚本
cat > /opt/backup-code.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/code"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

tar -czf $BACKUP_DIR/code_backup_$DATE.tar.gz /opt/nobel-order-system

# 保留最近7天的备份
find $BACKUP_DIR -name "code_backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x /opt/backup-code.sh

# 添加到 crontab（每周日凌晨3点备份）
crontab -e
# 添加：0 3 * * 0 /opt/backup-code.sh
```

---

## 🚨 故障排查

### 问题1: 服务无法启动

```bash
# 查看日志
tail -f /var/log/nobel-order-system.out.log

# 检查端口占用
netstat -tlnp | grep 8501

# 手动启动测试
cd /opt/nobel-order-system
source venv/bin/activate
streamlit run src/app_server.py --server.port=8501
```

### 问题2: 无法访问网站

```bash
# 检查 Nginx 状态
systemctl status nginx

# 检查 Nginx 配置
nginx -t

# 检查防火墙
ufw status
iptables -L
```

### 问题3: 数据库连接失败

```bash
# 测试网络连接
ping 你的 Supabase 主机

# 测试端口
telnet 你的 Supabase 主机 5432

# 检查配置
cat /opt/nobel-order-system/.streamlit/secrets.toml
```

---

## 💰 成本估算

| 项目 | 费用 | 说明 |
|------|------|------|
| 云服务器 | 50-100元/月 | 2核4G配置 |
| 域名 | 50-100元/年 | .com或.cn |
| HTTPS证书 | 免费 | Let's Encrypt |
| **总计** | **约650-1300元/年** | - |

---

## 🎯 总结

### 优势
- ✅ 固定公网IP
- ✅ 高性能
- ✅ 完全控制
- ✅ 可扩展性强
- ✅ 数据安全

### 缺点
- ❌ 需要维护
- ❌ 需要付费
- ❌ 需要技术能力

### 适用场景
- 长期使用
- 需要高性能
- 需要更多控制权

**推荐指数：⭐⭐⭐⭐**

---

## 📞 获取帮助

如有问题，可以：
1. 查看日志文件
2. 检查服务状态
3. 参考云服务商文档
4. 联系技术支持

---

**需要自动化部署脚本吗？** 我可以为您创建一键部署脚本！

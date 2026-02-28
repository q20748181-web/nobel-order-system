#!/bin/bash
# -*- coding: utf-8 -*-
# Nobel订单管理系统 - 一键部署到云服务器

set -e  # 遇到错误立即退出

echo "=========================================="
echo "🚀 Nobel订单管理系统 - 云服务器一键部署"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否以root运行
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用 root 权限运行此脚本${NC}"
    echo "命令: sudo bash deploy.sh"
    exit 1
fi

# 显示欢迎信息
echo -e "${GREEN}欢迎使用 Nobel订单管理系统一键部署脚本${NC}"
echo ""
echo "本脚本将自动完成以下操作："
echo "  1. 更新系统"
echo "  2. 安装必要软件（Python, Nginx, Supervisor）"
echo "  3. 创建虚拟环境并安装依赖"
echo "  4. 配置 Streamlit 服务"
echo "  5. 配置 Nginx 反向代理"
echo "  6. 配置 Supervisor 进程管理"
echo "  7. 启动服务"
echo ""
echo -e "${YELLOW}预计耗时：5-10 分钟${NC}"
echo ""
read -p "是否继续？(y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "部署已取消"
    exit 0
fi

echo ""
echo "=========================================="
echo "📦 步骤 1/7: 更新系统"
echo "=========================================="
echo ""

apt update
apt upgrade -y

echo -e "${GREEN}✓ 系统更新完成${NC}"
echo ""

echo "=========================================="
echo "📦 步骤 2/7: 安装必要软件"
echo "=========================================="
echo ""

echo "安装 Python 3 和 pip..."
apt install -y python3 python3-pip python3-venv

echo "安装 Git..."
apt install -y git

echo "安装 Nginx..."
apt install -y nginx

echo "安装 Supervisor..."
apt install -y supervisor

echo -e "${GREEN}✓ 软件安装完成${NC}"
echo ""

echo "=========================================="
echo "📦 步骤 3/7: 创建项目目录"
echo "=========================================="
echo ""

PROJECT_DIR="/opt/nobel-order-system"

if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}项目目录已存在，是否删除重新创建？${NC}"
    read -p "(y/n): " recreate
    if [ "$recreate" = "y" ] || [ "$recreate" = "Y" ]; then
        rm -rf "$PROJECT_DIR"
        echo "已删除旧目录"
    else
        echo "保留现有目录"
    fi
fi

mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/.streamlit"

echo -e "${GREEN}✓ 项目目录创建完成${NC}"
echo ""

echo "=========================================="
echo "📦 步骤 4/7: 创建虚拟环境并安装依赖"
echo "=========================================="
echo ""

cd "$PROJECT_DIR"

echo "创建虚拟环境..."
python3 -m venv venv

echo "激活虚拟环境..."
source venv/bin/activate

echo "升级 pip..."
pip install --upgrade pip

echo "安装 Python 依赖..."
pip install streamlit supabase pandas openpyxl

echo -e "${GREEN}✓ 虚拟环境和依赖安装完成${NC}"
echo ""

echo "=========================================="
echo "📦 步骤 5/7: 配置 Streamlit"
echo "=========================================="
echo ""

# 创建 Streamlit 配置文件
cat > "$PROJECT_DIR/.streamlit/config.toml" << 'EOF'
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
EOF

echo "Streamlit 配置文件已创建"
echo ""

echo "=========================================="
echo "📦 步骤 6/7: 配置 Supabase"
echo "=========================================="
echo ""

echo "请输入您的 Supabase 配置信息："
echo ""

read -p "Supabase Project URL: " SUPABASE_URL
read -p "Supabase anon key: " SUPABASE_ANON_KEY
read -p "Supabase service_role key: " SUPABASE_SERVICE_ROLE_KEY

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ] || [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    echo -e "${RED}错误：所有配置项都不能为空${NC}"
    exit 1
fi

# 创建 secrets.toml 文件
cat > "$PROJECT_DIR/.streamlit/secrets.toml" << EOF
[supabase]
project_url = "$SUPABASE_URL"
anon_key = "$SUPABASE_ANON_KEY"
service_role_key = "$SUPABASE_SERVICE_ROLE_KEY"
EOF

echo -e "${GREEN}✓ Supabase 配置完成${NC}"
echo ""

echo "=========================================="
echo "📦 步骤 7/7: 配置服务"
echo "=========================================="
echo ""

echo "配置 Supervisor..."
cat > /etc/supervisor/conf.d/nobel-order-system.conf << EOF
[program:nobel-order-system]
command=$PROJECT_DIR/venv/bin/streamlit run src/app_server.py --server.port=8501 --server.address=127.0.0.1
directory=$PROJECT_DIR
user=root
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/nobel-order-system.err.log
stdout_logfile=/var/log/nobel-order-system.out.log
environment=HOME="/root",USER="root"
EOF

echo "配置 Nginx..."
SERVER_IP=$(hostname -I | awk '{print $1}')
cat > /etc/nginx/sites-available/nobel-order-system << EOF
server {
    listen 80;
    server_name $SERVER_IP;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# 启用站点
ln -sf /etc/nginx/sites-available/nobel-order-system /etc/nginx/sites-enabled/

# 测试 Nginx 配置
nginx -t

echo -e "${GREEN}✓ 服务配置完成${NC}"
echo ""

echo "=========================================="
echo "🚀 启动服务"
echo "=========================================="
echo ""

echo "重新加载 Supervisor 配置..."
supervisorctl reread
supervisorctl update

echo "启动 Nobel订单管理系统服务..."
supervisorctl start nobel-order-system

echo "重启 Nginx..."
systemctl restart nginx

echo ""
echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo ""

echo -e "${GREEN}🎉 恭喜！Nobel订单管理系统已成功部署！${NC}"
echo ""
echo "📍 访问地址："
echo "   http://$SERVER_IP"
echo ""
echo "🔧 管理命令："
echo "   查看服务状态: supervisorctl status nobel-order-system"
echo "   重启服务: supervisorctl restart nobel-order-system"
echo "   查看日志: tail -f /var/log/nobel-order-system.out.log"
echo ""
echo "📝 下一步："
echo "   1. 上传代码到 $PROJECT_DIR"
echo "   2. 确保代码目录结构为："
echo "      $PROJECT_DIR/"
echo "      ├── src/"
echo "      │   └── app_server.py"
echo "      ├── config/"
echo "      ├── .streamlit/"
echo "      │   ├── config.toml"
echo "      │   └── secrets.toml"
echo "      └── venv/"
echo ""
echo "   3. 上传代码后，重启服务："
echo "      supervisorctl restart nobel-order-system"
echo ""
echo "🔐 配置 HTTPS（可选）："
echo "   运行: bash scripts/setup_ssl.sh"
echo ""
echo "=========================================="
echo ""

# 等待服务启动
sleep 3

# 检查服务状态
if supervisorctl status nobel-order-system | grep -q "RUNNING"; then
    echo -e "${GREEN}✓ 服务运行正常${NC}"
else
    echo -e "${YELLOW}⚠ 服务状态异常，请查看日志${NC}"
    echo "命令: tail -f /var/log/nobel-order-system.out.log"
fi

echo ""
echo "部署脚本执行完毕！"

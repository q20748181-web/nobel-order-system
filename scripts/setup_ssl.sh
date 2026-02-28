#!/bin/bash
# -*- coding: utf-8 -*-
# 配置 HTTPS 证书（Let's Encrypt）

set -e

echo "=========================================="
echo "🔐 Nobel订单管理系统 - HTTPS 配置"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查是否以root运行
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用 root 权限运行此脚本${NC}"
    echo "命令: sudo bash setup_ssl.sh"
    exit 1
fi

echo -e "${YELLOW}本脚本将为您的 Nobel订单管理系统配置 HTTPS 证书${NC}"
echo ""
echo "前置条件："
echo "  1. 已有域名（如：example.com）"
echo "  2. 域名已解析到服务器IP"
echo "  3. 服务器防火墙已开放 80 和 443 端口"
echo ""
read -p "是否继续？(y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "配置已取消"
    exit 0
fi

# 输入域名
echo ""
read -p "请输入您的域名（如：example.com）: " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo -e "${RED}错误：域名不能为空${NC}"
    exit 1
fi

# 检查域名是否已解析
echo ""
echo "检查域名解析..."
SERVER_IP=$(hostname -I | awk '{print $1}')
DOMAIN_IP=$(dig +short $DOMAIN)

if [ "$DOMAIN_IP" != "$SERVER_IP" ]; then
    echo -e "${RED}错误：域名未正确解析到服务器IP${NC}"
    echo "服务器IP: $SERVER_IP"
    echo "域名解析: $DOMAIN_IP"
    echo ""
    echo "请先在域名服务商处配置DNS解析："
    echo "  A 记录 -> $DOMAIN -> $SERVER_IP"
    exit 1
fi

echo -e "${GREEN}✓ 域名解析正确${NC}"
echo ""

# 安装 Certbot
echo "=========================================="
echo "📦 安装 Certbot"
echo "=========================================="
echo ""

apt update
apt install -y certbot python3-certbot-nginx

echo -e "${GREEN}✓ Certbot 安装完成${NC}"
echo ""

# 获取证书
echo "=========================================="
echo "🔐 获取 SSL 证书"
echo "=========================================="
echo ""

echo "正在为域名 $DOMAIN 获取证书..."
echo ""

certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSL 证书获取成功${NC}"
else
    echo -e "${RED}证书获取失败${NC}"
    echo "请检查："
    echo "  1. 域名解析是否正确"
    echo "  2. 防火墙是否开放 80 端口"
    echo "  3. Nginx 是否正在运行"
    exit 1
fi

# 更新 Nginx 配置
echo ""
echo "=========================================="
echo "🔧 更新 Nginx 配置"
echo "=========================================="
echo ""

cat > /etc/nginx/sites-available/nobel-order-system << EOF
server {
    listen 443 ssl;
    server_name $DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

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

server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$server_name\$request_uri;
}
EOF

# 测试 Nginx 配置
nginx -t

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Nginx 配置测试通过${NC}"
else
    echo -e "${RED}Nginx 配置测试失败${NC}"
    exit 1
fi

# 重启 Nginx
systemctl restart nginx

echo -e "${GREEN}✓ Nginx 重启成功${NC}"
echo ""

# 设置自动续期
echo "=========================================="
echo "🔄 设置证书自动续期"
echo "=========================================="
echo ""

(crontab -l 2>/dev/null; echo "0 0,12 * * * certbot renew --quiet && systemctl reload nginx") | crontab -

echo -e "${GREEN}✓ 证书自动续期已设置${NC}"
echo ""

echo "=========================================="
echo "✅ HTTPS 配置完成！"
echo "=========================================="
echo ""

echo -e "${GREEN}🎉 恭喜！HTTPS 配置成功！${NC}"
echo ""
echo "📍 访问地址："
echo "   http://$DOMAIN  (自动跳转到 HTTPS)"
echo "   https://$DOMAIN"
echo ""
echo "🔐 证书信息："
echo "   证书路径: /etc/letsencrypt/live/$DOMAIN/"
echo "   有效期: 90 天"
echo "   自动续期: 已启用（每天检查）"
echo ""
echo "🔧 管理命令："
echo "   手动续期: certbot renew"
echo "   查看证书: certbot certificates"
echo "   撤销证书: certbot revoke --cert-path /etc/letsencrypt/live/$DOMAIN/cert.pem"
echo ""
echo "=========================================="
echo ""
echo "配置脚本执行完毕！"

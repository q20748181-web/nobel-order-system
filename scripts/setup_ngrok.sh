#!/bin/bash
# 下载并配置ngrok

echo "🌐 正在下载ngrok..."

# 下载ngrok
wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -O /tmp/ngrok.zip

# 解压
unzip -q /tmp/ngrok.zip -d /tmp

# 赋予执行权限
chmod +x /tmp/ngrok

echo "✅ ngrok下载完成"
echo ""
echo "🚀 正在启动ngrok隧道..."

# 启动ngrok
/tmp/ngrok http 8501

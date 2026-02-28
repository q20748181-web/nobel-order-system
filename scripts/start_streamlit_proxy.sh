#!/bin/bash
# Streamlit 反向代理脚本 - 通过 Coze 域名提供外网访问

echo "🚀 启动 Streamlit 反向代理..."

# 确保 Streamlit 在 8501 端口运行
streamlit run src/app_server.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false

echo "✅ Streamlit 已在端口 8501 启动"

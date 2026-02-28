#!/bin/bash
# 快速启动 Streamlit 应用

echo "🚀 正在启动 Nobel订单管理系统..."

cd /workspace/projects

# 检查依赖
echo "📦 检查依赖..."
pip install -q streamlit pandas

# 启动应用
echo "✅ 启动服务中..."
streamlit run src/app_server.py --server.port=8501 --server.address=0.0.0.0

echo "✅ 服务已启动！"

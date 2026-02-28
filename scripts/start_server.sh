#!/bin/bash
# 启动Streamlit后端服务

echo "🚀 正在启动 Nobel 订单管理系统（网络同步版）..."
echo "📊 数据库连接：Supabase"
echo "🌐 数据将实时同步到云端"
echo ""

cd /workspace/projects

streamlit run src/app_server.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false

#!/bin/bash
# -*- coding: utf-8 -*-
# Nobel订单管理系统 - 快速启动脚本

echo "=========================================="
echo "🚀 Nobel订单管理系统 - 快速启动"
echo "=========================================="
echo ""

# 检查服务是否在运行
if pgrep -f "streamlit run src/app_server.py" > /dev/null; then
    echo "✅ Streamlit服务已在运行"
    echo ""
    echo "📍 访问地址："
    echo "   - 内网: http://9.128.127.13:8501"
    echo "   - 本地: http://localhost:8501"
    echo ""
else
    echo "⚠️  Streamlit服务未运行"
    echo ""
    echo "正在启动服务..."
    nohup streamlit run src/app_server.py \
        --server.port=8501 \
        --server.address=0.0.0.0 \
        --server.headless=true \
        --browser.gatherUsageStats=false \
        > /tmp/streamlit.log 2>&1 &
    
    sleep 3
    
    if pgrep -f "streamlit run src/app_server.py" > /dev/null; then
        echo "✅ Streamlit服务启动成功"
        echo ""
        echo "📍 访问地址："
        echo "   - 内网: http://9.128.127.13:8501"
        echo "   - 本地: http://localhost:8501"
        echo ""
    else
        echo "❌ Streamlit服务启动失败"
        echo ""
        echo "查看日志："
        echo "   tail -f /tmp/streamlit.log"
        echo ""
        exit 1
    fi
fi

echo "=========================================="
echo "📌 快速链接"
echo "=========================================="
echo ""
echo "1️⃣  访问系统: http://9.128.127.13:8501"
echo ""
echo "2️⃣  查看外网访问方案: python scripts/show_tunnel_solutions.py"
echo ""
echo "3️⃣  查看完整教程: cat docs/QUICK_START_TUTORIAL.md"
echo ""
echo "4️⃣  查看服务日志: tail -f /tmp/streamlit.log"
echo ""
echo "=========================================="
echo ""
echo "💡 需要外网访问吗？运行以下命令查看解决方案："
echo "   python scripts/show_tunnel_solutions.py"
echo ""
echo "=========================================="

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - 外网访问解决方案
使用在线隧道服务快速获取外网地址
"""

import os
import sys

def show_solutions():
    """显示外网访问解决方案"""

    print("=" * 70)
    print("🌐 Nobel订单管理系统 - 外网访问解决方案")
    print("=" * 70)
    print()
    print("您的Streamlit服务已经在运行：")
    print("   📍 内网地址: http://9.128.127.13:8501")
    print("   📍 本地地址: http://localhost:8501")
    print()
    print("=" * 70)
    print()

    print("💡 推荐方案：使用在线隧道服务（无需下载，立即使用）")
    print()
    print("方案1：使用 Serveo 隧道（推荐，免费，无需注册）")
    print("-" * 70)
    print("步骤：")
    print("  1. 在您的本地电脑上打开终端")
    print("  2. 输入以下命令：")
    print("     ssh -R 80:localhost:8501 serveo.net")
    print("  3. 等待连接建立，会显示一个外网地址")
    print("  4. 将这个地址分享给您的同事")
    print()
    print("示例输出：")
    print("  Forwarding HTTP traffic from https://abc123.serveo.net")
    print("  Press Ctrl+C to stop")
    print()
    print("注意：")
    print("  - 需要您的本地电脑能够访问这个服务器")
    print("  - 第一次使用需要接受SSH密钥")
    print("  - 地址可能会变化，建议每次分享前重新获取")
    print()
    print("-" * 70)
    print()

    print("方案2：使用 localtunnel（推荐，免费，简单）")
    print("-" * 70)
    print("步骤：")
    print("  1. 确保您的电脑已安装 Node.js")
    print("  2. 在您的本地电脑上打开终端")
    print("  3. 安装 localtunnel：")
    print("     npm install -g localtunnel")
    print("  4. 启动隧道：")
    print("     lt --port 8501")
    print("  5. 复制显示的URL分享给您的同事")
    print()
    print("示例输出：")
    print("  your url is: https://random-name.loca.lt")
    print()
    print("注意：")
    print("  - 需要在您的本地电脑上运行，不是在这台服务器上")
    print("  - URL是临时的，关闭终端后失效")
    print()
    print("-" * 70)
    print()

    print("方案3：使用 Cloudflare Tunnel（推荐，稳定，免费）")
    print("-" * 70)
    print("步骤：")
    print("  1. 注册 Cloudflare 账号（免费）")
    print("  2. 下载 cloudflared：")
    print("     https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/")
    print("  3. 安装并运行：")
    print("     cloudflared tunnel --url http://localhost:8501")
    print("  4. 复制显示的URL分享给您的同事")
    print()
    print("优点：")
    print("  - 可以使用自己的域名")
    print("  - 更稳定，速度更快")
    print("  - 免费额度充足")
    print()
    print("-" * 70)
    print()

    print("方案4：部署到云服务器（最稳定，长期使用）")
    print("-" * 70)
    print("步骤：")
    print("  1. 购买云服务器（阿里云、腾讯云、华为云等）")
    print("  2. 配置服务器：")
    print("     - 安装 Python 3")
    print("     - 安装依赖：pip install streamlit supabase pandas")
    print("  3. 上传代码文件")
    print("  4. 启动服务：")
    print("     streamlit run app_server.py --server.port 8501")
    print("  5. 配置域名和HTTPS（可选）")
    print()
    print("优点：")
    print("  - URL固定，随时可访问")
    print("  - 性能稳定")
    print("  - 可以24小时运行")
    print()
    print("-" * 70)
    print()

    print("⚡ 快速开始（最简单方案）")
    print("=" * 70)
    print()
    print("如果您只是临时需要外网访问，推荐使用 serveo.net：")
    print()
    print("1️⃣ 在您的本地电脑打开终端")
    print("2️⃣ 输入命令：")
    print()
    print("   ssh -R 80:localhost:9.128.127.13:8501 serveo.net")
    print()
    print("3️⃣ 等待显示外网地址")
    print("4️⃣ 分享这个地址给您的同事")
    print()
    print("=" * 70)
    print()
    print("💡 如果您需要长期稳定的外网访问，建议：")
    print()
    print("1. 购买云服务器（约50-100元/月）")
    print("2. 部署Streamlit服务")
    print("3. 配置域名")
    print()
    print("💬 需要帮助配置云服务器吗？")
    print("   我可以为您提供详细的部署步骤！")
    print()
    print("=" * 70)

def check_service():
    """检查Streamlit服务状态"""
    import subprocess
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'streamlit' in line and 'app_server.py' in line and 'grep' not in line:
                parts = line.split()
                print(f"✅ Streamlit服务正在运行")
                print(f"   进程ID: {parts[1]}")
                print(f"   端口: 8501")
                print()
                return True
    except:
        pass

    print("⚠️  Streamlit服务未运行")
    print()
    print("启动命令：")
    print("   cd /workspace/projects")
    print("   bash scripts/start_server.sh")
    print()
    return False

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')

    print()
    print("🔍 检查服务状态...")
    print()
    check_service()

    show_solutions()

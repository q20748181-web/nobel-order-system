#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用本地隧道服务获取外网地址
"""

import subprocess
import time
import requests
import sys

def use_localtunnel(port=8501):
    """使用localtunnel获取外网地址"""
    print("🌐 正在启动本地隧道...")

    try:
        # 安装localtunnel
        print("📦 正在安装localtunnel...")
        subprocess.run([sys.executable, "-m", "pip", "install", "localtunnel"], check=True)

        # 启动localtunnel
        print(f"🚀 正在启动隧道服务，端口 {port}...")
        lt_process = subprocess.Popen(
            ["lt", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 等待服务启动
        time.sleep(3)

        # 读取输出，获取URL
        try:
            # 设置超时读取
            import select
            if select.select([lt_process.stdout], [], [], 5)[0]:
                output = lt_process.stdout.readline()
                print(f"✅ 隧道启动成功！")
                print(f"📍 外网地址: {output.strip()}")

                # 持续运行
                print("\n⏰ 服务正在运行中，按 Ctrl+C 停止")
                print("🔗 分享上面的地址给您的同事即可访问\n")

                # 保持运行
                lt_process.wait()
            else:
                print("⚠️  无法获取外网地址")
                lt_process.terminate()

        except KeyboardInterrupt:
            print("\n\n⏹️  正在停止隧道服务...")
            lt_process.terminate()
            lt_process.wait()
            print("✅ 服务已停止")

    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        print("\n💡 请手动安装:")
        print("   npm install -g localtunnel")
        print("   lt --port 8501")
    except Exception as e:
        print(f"❌ 错误: {e}")
        if 'lt_process' in locals():
            lt_process.terminate()

if __name__ == "__main__":
    port = 8501
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print("🌐 Nobel订单管理系统 - 外网访问工具")
    print("=" * 50)
    use_localtunnel(port)

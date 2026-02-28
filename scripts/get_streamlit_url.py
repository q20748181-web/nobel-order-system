#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - HTML代理页面
通过 HTML 页面代理 Streamlit 应用
"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

# HTML 内容 - 将通过 iframe 加载本地 Streamlit 服务
HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nobel订单管理系统 - 外网访问</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }
        .loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            font-family: Arial, sans-serif;
            color: #333;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p>正在加载 Nobel订单管理系统...</p>
        <p style="font-size: 12px; color: #666; margin-top: 10px;">首次加载可能需要几秒钟</p>
    </div>
    <iframe id="streamlit-frame" src="" onload="document.getElementById('loading').style.display='none'"></iframe>

    <script>
        // 获取 Streamlit 服务的内网地址
        const streamlitHost = 'http://localhost:8501';

        // 尝试通过 Coze 代理访问
        // 注意：这种方式需要在同一个网络环境或配置了端口转发
        document.getElementById('streamlit-frame').src = streamlitHost;

        // 如果加载失败，显示提示
        setTimeout(function() {
            const loading = document.getElementById('loading');
            if (loading.style.display !== 'none') {
                loading.innerHTML = `
                    <div style="color: #e74c3c;">
                        <p>⚠️ 无法连接到 Streamlit 服务</p>
                        <p style="font-size: 12px; color: #666; margin-top: 10px;">
                            请确保服务已启动并配置了外网访问
                        </p>
                    </div>
                `;
            }
        }, 10000);
    </script>
</body>
</html>"""

def upload_proxy_page():
    """上传代理页面到 Coze 存储"""

    print("🚀 正在上传代理页面...")

    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    # 上传 HTML 文件
    file_key = "nobel_streamlit_proxy.html"

    # 写入临时文件
    temp_path = f"/tmp/{file_key}"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    # 上传到存储
    storage.upload_file(
        file_path=temp_path,
        key=file_key,
    )

    # 生成访问URL（有效期30天）
    access_url = storage.generate_presigned_url(
        key=file_key,
        expire_time=2592000,  # 30天
    )

    print("=" * 70)
    print("🌐 Nobel订单管理系统 - 外网访问地址")
    print("=" * 70)
    print(f"\n{access_url}")
    print("\n" + "=" * 70)
    print("⚠️ 注意：")
    print("  • 此链接需要与 Streamlit 服务在同一网络环境")
    print("  • 如需跨网访问，请配置端口转发或 VPN")
    print("  • 更好的方案：使用 Streamlit Cloud 部署")
    print("=" * 70)

    # 清理临时文件
    os.remove(temp_path)

    return access_url

if __name__ == "__main__":
    upload_proxy_page()

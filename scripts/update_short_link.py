#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新短链接，指向新版本的HTML
"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

# 初始化存储客户端
storage = S3SyncStorage(
    endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
    access_key="",
    secret_key="",
    bucket_name=os.getenv("COZE_BUCKET_NAME"),
    region="cn-beijing",
)

# 新版本的URL
new_url = "https://coze-coding-project.tos.coze.site/coze_storage_7611717619640762422/c_d5000a39.html"

# 创建HTML重定向页面
redirect_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url={new_url}">
    <title>正在跳转...</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
        p {{ font-size: 18px; color: #666; }}
        a {{ color: #667eea; text-decoration: none; }}
    </style>
</head>
<body>
    <p>正在跳转到橱柜订单管理系统...</p>
    <p><a href="{new_url}">如果没有自动跳转，请点击这里</a></p>
</body>
</html>
"""

print("正在更新短链接...")

try:
    # 上传重定向页面（使用短文件名 c.html）
    file_key = storage.upload_file(
        file_content=redirect_html.encode('utf-8'),
        file_name="c.html",
        content_type="text/html; charset=utf-8",
    )
    
    print(f"✅ 短链接更新成功！")
    print(f"   文件Key: {file_key}")
    
    # 生成预签名 URL（有效期1年）
    url = storage.generate_presigned_url(
        key=file_key,
        expire_time=31536000  # 1年
    )
    
    print(f"\n🔗 短链接 (有效期1年):")
    print(f"{url}")
    print(f"\n✅ 用户访问短链接后会自动跳转到新版本！")
    
except Exception as e:
    print(f"❌ 更新失败: {e}")

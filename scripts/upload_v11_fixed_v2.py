#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传修复版HTML到对象存储（使用SDK）
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

# 读取HTML文件
local_file = "assets/cabinet_system_v11_fixed.html"
file_name = "c.html"

print(f"正在上传 {local_file}...")

try:
    # 读取文件内容
    with open(local_file, 'rb') as f:
        file_content = f.read()
    
    # 上传文件
    file_key = storage.upload_file(
        file_content=file_content,
        file_name=file_name,
        content_type="text/html; charset=utf-8",
    )
    
    print(f"✅ 上传成功！")
    print(f"   文件Key: {file_key}")
    
    # 生成预签名 URL（有效期1年）
    url = storage.generate_presigned_url(
        key=file_key,
        expire_time=31536000  # 1年
    )
    
    print(f"\n🌐 访问链接 (有效期1年):")
    print(f"{url}")
    
except Exception as e:
    print(f"❌ 上传失败: {e}")

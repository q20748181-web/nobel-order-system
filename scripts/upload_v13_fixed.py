#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传V13修复版（修复状态、文件显示和下载按钮）到对象存储
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

print("正在上传V13修复版（修复状态、文件显示和下载按钮）...")

try:
    # 读取HTML文件
    with open('assets/cabinet_system_v13_fixed.html', 'rb') as f:
        file_content = f.read()
    
    # 上传文件
    file_key = storage.upload_file(
        file_content=file_content,
        file_name="cabinet_system_v13_fixed.html",
        content_type="text/html; charset=utf-8",
    )
    
    print(f"✅ 上传成功！")
    print(f"   文件Key: {file_key}")
    
    # 生成预签名 URL（有效期10年）
    url = storage.generate_presigned_url(
        key=file_key,
        expire_time=315360000  # 10年
    )
    
    print(f"\n🔗 访问链接 (有效期10年):")
    print(f"\n{url}")
    print(f"\n📋 默认登录账号:")
    print(f"   用户名: admin")
    print(f"   密码: admin")
    print(f"\n🔧 本次修复:")
    print(f"   ✅ 订单编辑状态选择框可见")
    print(f"   ✅ 文件上传预览显示")
    print(f"   ✅ 文件下载链接可见")
    print(f"   ✅ 改进样式和用户体验")
    
except Exception as e:
    print(f"❌ 上传失败: {e}")
    import traceback
    traceback.print_exc()

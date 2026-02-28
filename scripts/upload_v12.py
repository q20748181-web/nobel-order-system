#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传V12版本到对象存储
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

print("正在上传V12版本...")

try:
    # 读取HTML文件
    with open('assets/cabinet_system_v12_with_auth.html', 'rb') as f:
        file_content = f.read()
    
    # 上传文件
    file_key = storage.upload_file(
        file_content=file_content,
        file_name="cabinet_system_v12_with_auth.html",
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
    print(f"\n💡 新功能:")
    print(f"   ✅ 用户登录系统")
    print(f"   ✅ 角色权限管理")
    print(f"   ✅ 订单状态细化")
    print(f"   ✅ 完整时间追踪")
    print(f"   ✅ 文件上传下载")
    print(f"   ✅ 去掉顶部多余文字")
    
except Exception as e:
    print(f"❌ 上传失败: {e}")
    import traceback
    traceback.print_exc()

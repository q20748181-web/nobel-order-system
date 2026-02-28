#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接生成并上传最终的访问链接
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

print("正在生成访问链接...")

try:
    # 直接生成已上传文件的预签名 URL
    file_key = "c_d5000a39.html"
    
    # 生成长期有效的预签名 URL（10年）
    url = storage.generate_presigned_url(
        key=file_key,
        expire_time=315360000  # 10年
    )
    
    print(f"✅ 链接生成成功！")
    print(f"   文件Key: {file_key}")
    print(f"\n🔗 最终访问链接 (有效期10年):")
    print(f"\n{url}")
    print(f"\n💡 请复制上面的完整链接，在浏览器中打开即可使用！")
    
except Exception as e:
    print(f"❌ 生成失败: {e}")
    import traceback
    traceback.print_exc()

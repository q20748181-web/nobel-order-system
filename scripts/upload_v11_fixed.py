#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传修复版HTML到对象存储
"""

import boto3
from botocore.client import Config

# S3 兼容对象存储配置
S3_ENDPOINT = "https://s3.coze-coding.dev"
S3_BUCKET = "coze-coding-dev"
S3_ACCESS_KEY = "Y3Z6dGJqcG9rZWh4ZGVycW54em5k"
S3_SECRET_KEY = "NzR4bDRjaWh2aGpxbWlrcG9zZHh5a3h4a2V5aGx6ZmVqb3RueWNmbQ=="

# 创建 S3 客户端
s3 = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# 上传文件
local_file = "assets/cabinet_system_v11_fixed.html"
s3_key = "c.html"

print(f"正在上传 {local_file} 到 {S3_BUCKET}/{s3_key}...")

try:
    s3.upload_file(
        local_file,
        S3_BUCKET,
        s3_key,
        ExtraArgs={'ContentType': 'text/html; charset=utf-8'}
    )
    print("✅ 上传成功！")
    
    # 生成预签名 URL
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': s3_key},
        ExpiresIn=31536000  # 1年有效期
    )
    
    print(f"\n🌐 访问链接 (有效期1年):")
    print(f"{url}")
    
except Exception as e:
    print(f"❌ 上传失败: {e}")

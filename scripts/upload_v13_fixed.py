#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""将修复后的HTML文件上传到对象存储"""

import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
OBJECT_STORAGE_ENDPOINT = os.getenv("OBJECT_STORAGE_ENDPOINT", "")
OBJECT_STORAGE_ACCESS_KEY = os.getenv("OBJECT_STORAGE_ACCESS_KEY", "")
OBJECT_STORAGE_SECRET_KEY = os.getenv("OBJECT_STORAGE_SECRET_KEY", "")
OBJECT_STORAGE_BUCKET = os.getenv("OBJECT_STORAGE_BUCKET", "")

def upload_to_object_storage(file_path, object_name):
    """上传文件到对象存储"""
    if not all([OBJECT_STORAGE_ENDPOINT, OBJECT_STORAGE_ACCESS_KEY, OBJECT_STORAGE_SECRET_KEY]):
        print("❌ 对象存储配置不完整，跳过上传")
        return None

    try:
        # 构造预签名URL（使用PutObject方法）
        # 注意：这里使用PUT方法上传，需要将文件内容放在body中
        with open(file_path, 'rb') as f:
            response = requests.put(
                f"{OBJECT_STORAGE_ENDPOINT}/{OBJECT_STORAGE_BUCKET}/{object_name}",
                headers={
                    "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
                    "X-Amz-Credential": f"{OBJECT_STORAGE_ACCESS_KEY}/us-east-1/s3/aws4_request",
                    "X-Amz-Date": "20250101T000000Z",
                    "X-Amz-SignedHeaders": "host",
                    "X-Amz-Signature": "dummy"  # 简化处理，实际需要生成签名
                },
                data=f.read()
            )

        if response.status_code in [200, 201]:
            print(f"✅ 文件上传成功: {object_name}")
            # 返回访问URL（需要生成预签名URL）
            return f"{OBJECT_STORAGE_ENDPOINT}/{OBJECT_STORAGE_BUCKET}/{object_name}"
        else:
            print(f"❌ 上传失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 上传出错: {str(e)}")
        return None

if __name__ == "__main__":
    html_file = "assets/cabinet_system_v13_fixed.html"
    if os.path.exists(html_file):
        # 使用极简文件名以缩短URL
        print("📤 正在上传到对象存储...")
        result = upload_to_object_storage(html_file, "c.html")
        if result:
            print(f"✅ 上传成功！")
            print(f"🔗 访问链接: {result}")
            print(f"\n💡 提示：如果需要预签名URL，请联系管理员生成永久访问链接")
        else:
            print("⚠️  上传失败，请手动上传文件到对象存储")
    else:
        print(f"❌ 文件不存在: {html_file}")

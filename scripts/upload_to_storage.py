#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传HTML文件到对象存储并生成访问链接"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_html():
    """上传HTML文件并生成访问链接"""

    # 初始化对象存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    # HTML文件路径
    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v14.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        # 使用流式上传
        print("📤 正在上传文件到对象存储...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v14.html",
                content_type="text/html",
            )

        print(f"✅ 上传成功！")
        print(f"📂 对象键: {key}")

        # 生成预签名URL（有效期7天 = 604800秒）
        url = storage.generate_presigned_url(
            key=key,
            expire_time=604800  # 7天
        )

        print(f"\n🔗 访问链接:")
        print(f"{url}")
        print(f"\n⏰ 链接有效期: 7天")
        print(f"\n💡 提示:")
        print(f"  - 链接有效期7天，过期后需要重新生成")
        print(f"  - 可以直接在浏览器中打开此链接访问系统")
        print(f"  - 建议收藏此链接方便后续访问")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_html()

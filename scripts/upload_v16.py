#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传v16修复版本HTML文件到对象存储"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_v16():
    """上传v16修复版本HTML文件并生成访问链接"""

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v16.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        print("📤 正在上传 v16 修复版本...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v16.html",
                content_type="text/html",
            )

        print(f"✅ 上传成功！")
        print(f"📂 对象键: {key}")

        url = storage.generate_presigned_url(
            key=key,
            expire_time=604800  # 7天
        )

        print(f"\n🔗 访问链接:")
        print(f"{url}")
        print(f"\n⏰ 链接有效期: 7天")
        print(f"\n🔧 v16 版本修复内容:")
        print(f"  - ✅ 修复了登录按钮无法点击的问题")
        print(f"  - ✅ 修复了JavaScript执行顺序问题")
        print(f"  - ✅ 添加了初始化事件监听")
        print(f"  - ✅ 优化了登录验证逻辑")
        print(f"  - ✅ 添加了详细的调试日志")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_v16()

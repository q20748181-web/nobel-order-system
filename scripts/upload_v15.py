#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传v15版本HTML文件到对象存储"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_v15():
    """上传v15版本HTML文件并生成访问链接"""

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v15.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        print("📤 正在上传 v15 版本...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v15.html",
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
        print(f"\n✨ v15 版本更新内容:")
        print(f"  - ✅ 修复了客户选择显示 undefined 的问题")
        print(f"  - ✅ 优化了UI设计，更现代化")
        print(f"  - ✅ 修复了所有按钮点击问题")
        print(f"  - ✅ 改进了表单标题和提示文字")
        print(f"  - ✅ 优化了文件上传和下载功能")
        print(f"  - ✅ 添加了更好的视觉反馈")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_v15()

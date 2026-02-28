#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传v17版本HTML文件到对象存储"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_v17():
    """上传v17版本HTML文件并生成访问链接"""

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v17.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        print("📤 正在上传 v17 版本...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v17.html",
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
        print(f"\n🔧 v17 版本更新内容:")
        print(f"  - ✅ 修改执行人标签：打样→执行人，设计报价→执行人")
        print(f"  - ✅ 修改执行人标签：正式订单→拆单技术员，售后服务→拆单技术员")
        print(f"  - ✅ 添加客户编号点击功能，显示该客户的所有订单")
        print(f"  - ✅ 优化客户订单视图，支持按订单类型分组展示")
        print(f"  - ✅ 改进用户体验，订单详情一目了然")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_v17()

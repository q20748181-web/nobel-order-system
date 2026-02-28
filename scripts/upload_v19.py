#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传v19版本HTML文件到对象存储"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_v19():
    """上传v19版本HTML文件并生成访问链接"""

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v19.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        print("📤 正在上传 v19 版本...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v19.html",
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
        print(f"\n🔧 v19 版本更新内容:")
        print(f"  - ✅ 添加'清除所有数据'功能")
        print(f"  - ✅ 添加'重置为演示数据'功能")
        print(f"  - ✅ 解决订单数量显示不准确的问题")
        print(f"  - ✅ 添加警告提示，防止误操作")
        print(f"  - ✅ 保持v18版本的所有功能不变")

        print(f"\n💡 使用说明:")
        print(f"  - 如果订单数量显示不准确，请使用'清除所有数据'或'重置为演示数据'")
        print(f"  - 演示数据包含：3个客户、1个打样订单、1个管理员账号")
        print(f"  - '重置为演示数据'会清空当前所有数据并加载预设数据")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_v19()

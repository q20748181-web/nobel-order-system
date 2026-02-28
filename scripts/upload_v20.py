#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传v20版本HTML文件到对象存储"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_v20():
    """上传v20版本HTML文件并生成访问链接"""

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v20.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        print("📤 正在上传 v20 版本...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v20.html",
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
        print(f"\n🔧 v20 版本更新内容:")
        print(f"  - ✅ 危险操作（清除/重置数据）仅admin可见")
        print(f"  - ✅ 非admin用户无法看到危险操作区域")
        print(f"  - ✅ 增强系统安全性，防止误操作")
        print(f"  - ✅ 保持v19版本的所有功能不变")

        print(f"\n💡 权限说明:")
        print(f"  - 只有admin用户可以看到'危险操作'卡片")
        print(f"  - 其他用户只能看到'数据导出'和'数据导入'功能")
        print(f"  - 建议创建不同角色的用户账号进行测试")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_v20()

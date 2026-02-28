#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传v22版本HTML文件到对象存储"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_v22():
    """上传v22版本HTML文件并生成访问链接"""

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v22.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        print("📤 正在上传 v22 版本...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v22.html",
                content_type="text/html",
            )

        print(f"✅ 上传成功！")
        print(f"📂 对象键: {key}")

        # 10年有效期
        url = storage.generate_presigned_url(
            key=key,
            expire_time=315360000
        )

        print(f"\n🔗 访问链接:")
        print(f"{url}")
        print(f"\n⏰ 链接有效期: 10年")

        print(f"\n🔧 v22 版本更新内容:")
        print(f"  - ✅ 添加Supabase JavaScript SDK")
        print(f"  - ✅ 创建数据库表结构（customers、orders、users、order_files）")
        print(f"  - ✅ 配置RLS安全策略")
        print(f"  - ✅ 插入初始演示数据")
        print(f"  - ⚠️  注意：当前版本仍使用localStorage存储")

        print(f"\n⚠️  重要说明:")
        print(f"  - 数据库表已创建完成，可以存储数据")
        print(f"  - HTML文件已添加Supabase SDK")
        print(f"  - 由于代码复杂性，完整数据库集成需要开发后端API")
        print(f"  - 建议参考 docs/DATABASE_INTEGRATION.md 了解详细说明")

        print(f"\n💡 后续步骤:")
        print(f"  1. 开发后端API服务（Python + FastAPI）")
        print(f"  2. 在后端集成Supabase数据库")
        print(f"  3. 修改前端通过API访问数据")
        print(f"  4. 实现多用户数据共享")

        print(f"\n📚 详细文档:")
        print(f"  - 查看 docs/DATABASE_INTEGRATION.md 了解数据库集成方案")
        print(f"  - 数据库已配置完成，可以开始开发后端服务")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_v22()

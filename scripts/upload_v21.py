#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""上传v21版本HTML文件到对象存储"""

import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_v21():
    """上传v21版本HTML文件并生成访问链接"""

    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )

    html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets", "cabinet_system_v21.html")

    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        return None

    try:
        print("📤 正在上传 v21 版本...")
        with open(html_path, "rb") as f:
            key = storage.stream_upload_file(
                fileobj=f,
                file_name="cabinet_system_v21.html",
                content_type="text/html",
            )

        print(f"✅ 上传成功！")
        print(f"📂 对象键: {key}")

        # 10年有效期：10 * 365 * 24 * 60 * 60 = 315360000秒
        url = storage.generate_presigned_url(
            key=key,
            expire_time=315360000
        )

        print(f"\n🔗 访问链接:")
        print(f"{url}")
        print(f"\n⏰ 链接有效期: 10年")
        print(f"\n🔧 v21 版本更新内容:")
        print(f"  - ✅ 仪表板卡片可点击跳转到对应页面")
        print(f"  - ✅ 客户总数 → 客户管理页面")
        print(f"  - ✅ 打样订单 → 打样订单页面")
        print(f"  - ✅ 设计报价 → 设计报价页面")
        print(f"  - ✅ 正式订单 → 正式订单页面")
        print(f"  - ✅ 售后服务 → 售后服务页面")
        print(f"  - ✅ 链接有效期延长至10年")
        print(f"  - ✅ 优化卡片交互效果（点击反馈）")

        print(f"\n💡 使用说明:")
        print(f"  - 点击仪表板任意统计卡片即可跳转到对应页面")
        print(f"  - 卡片支持鼠标悬停和点击动画效果")
        print(f"  - 系统链接有效期10年，无需频繁更新")

        return url

    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return None

if __name__ == "__main__":
    upload_v21()

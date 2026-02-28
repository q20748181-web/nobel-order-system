"""
生成橱柜订单管理系统的短链接访问地址
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def generate_short_url():
    """生成短链接访问地址"""
    
    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 生成访问URL（有效期30天）
    access_url = storage.generate_presigned_url(
        key="c_6876f231.html",
        expire_time=2592000,  # 30天
    )
    
    print("=" * 70)
    print("🏠 橱柜订单管理系统 - 优化后的访问地址")
    print("=" * 70)
    print(f"\n{access_url}")
    print("\n" + "=" * 70)
    print("✨ 特点：")
    print("  • 已预载示例数据（3个客户、6个产品、3个订单）")
    print("  • 完全在线使用，无需下载")
    print("  • 数据保存在浏览器本地")
    print("  • 链接有效期：30天")
    print("=" * 70)
    
    return access_url

if __name__ == "__main__":
    generate_short_url()

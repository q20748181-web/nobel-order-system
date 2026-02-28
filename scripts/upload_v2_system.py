"""
上传新版本系统到对象存储并生成访问链接
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_system_to_storage():
    """上传HTML文件到对象存储并返回访问URL"""
    
    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 读取HTML文件
    html_file_path = "/workspace/projects/assets/cabinet_system_v2.html"
    
    print("📖 正在读取HTML文件...")
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 上传到对象存储（使用简短文件名c2.html以缩短URL）
    print("⬆️  正在上传到对象存储...")
    file_key = storage.upload_file(
        file_content=html_content.encode('utf-8'),
        file_name="c2.html",
        content_type="text/html",
    )
    
    print(f"✅ 上传成功！文件Key: {file_key}")
    
    # 生成预签名URL（30天有效期）
    print("🔗 正在生成访问链接...")
    access_url = storage.generate_presigned_url(
        key=file_key,
        expire_time=30 * 24 * 60 * 60,  # 30天
    )
    
    print("\n" + "="*60)
    print("🎉 系统上传成功！")
    print("="*60)
    print(f"\n访问链接（30天有效）：\n{access_url}")
    print("\n" + "="*60)
    print("\n📋 系统功能说明：")
    print("1. 📊 仪表盘 - 概览所有数据统计")
    print("2. 👥 客户管理 - 客户代码、地区、Logo上传")
    print("3. 🎨 订单打样 - 打样订单管理")
    print("4. 💰 设计报价 - 设计报价订单")
    print("5. 📝 下单管理 - 正式下单管理")
    print("6. 🔧 售后管理 - 售后服务订单")
    print("\n✨ 特色功能：")
    print("- 支持客户Logo上传（图片预览）")
    print("- 数据本地存储，刷新不丢失")
    print("- 已预载示例数据，直接可用")
    print("="*60)
    
    return access_url

if __name__ == "__main__":
    url = upload_system_to_storage()

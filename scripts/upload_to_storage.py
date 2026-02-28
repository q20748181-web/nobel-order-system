"""
将橱柜订单管理系统上传到对象存储，生成永久可访问的URL
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_system_to_storage():
    """上传系统到对象存储"""
    
    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 读取HTML文件
    html_file_path = "/workspace/projects/assets/cabinet_order_system_with_demo.html"
    
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read().encode('utf-8')
    
    # 上传文件
    print("正在上传系统到对象存储...")
    key = storage.upload_file(
        file_content=html_content,
        file_name="cabinet_order_system/index.html",
        content_type="text/html",
    )
    
    print(f"✅ 上传成功！")
    print(f"文件 key: {key}")
    
    # 生成永久访问URL（有效期30天）
    access_url = storage.generate_presigned_url(
        key=key,
        expire_time=2592000,  # 30天
    )
    
    print(f"\n🌐 访问地址：")
    print(f"{access_url}")
    print(f"\n⚠️ 注意：此链接有效期30天，如需长期使用请重新生成")
    
    return access_url

if __name__ == "__main__":
    url = upload_system_to_storage()

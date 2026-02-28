"""
上传增强版订单系统HTML到对象存储（使用coze-coding-dev-sdk）
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_to_object_storage():
    """上传文件到对象存储"""
    
    # 文件路径
    local_file = "/workspace/projects/assets/cabinet_system_v7_enhanced.html"
    
    # 读取文件内容
    with open(local_file, 'rb') as f:
        file_content = f.read()
    
    try:
        # 初始化S3SyncStorage
        storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
        
        # 上传文件（使用极简文件名）
        print("正在上传文件到对象存储...")
        key = storage.upload_file(
            file_content=file_content,
            file_name="cabinet_enhanced_final.html",
            content_type="text/html; charset=utf-8",
        )
        
        print(f"✅ 文件已上传，对象Key: {key}")
        
        # 生成预签名URL（30天有效）
        url = storage.generate_presigned_url(
            key=key,
            expire_time=30 * 24 * 60 * 60  # 30天
        )
        
        print(f"🔗 预签名URL（30天有效）:")
        print(url)
        return url
            
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    url = upload_to_object_storage()
    if url:
        print("\n🎉 增强版系统部署成功！")
    else:
        print("\n❌ 部署失败")

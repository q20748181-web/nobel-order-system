"""
上传增强版系统到对象存储
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_enhanced_system():
    """上传增强版HTML文件到对象存储"""
    
    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 读取HTML文件
    html_file_path = "/workspace/projects/assets/cabinet_system_v4_enhanced.html"
    
    print("📖 正在读取增强版HTML文件...")
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✅ 文件读取成功，大小：{len(html_content)} 字符")
    
    # 上传到对象存储
    print("⬆️  正在上传到对象存储...")
    file_key = storage.upload_file(
        file_content=html_content.encode('utf-8'),
        file_name="cabinet_enhanced.html",
        content_type="text/html",
    )
    
    print(f"✅ 上传成功！文件Key: {file_key}")
    
    # 生成预签名URL（30天有效期）
    print("🔗 正在生成访问链接...")
    access_url = storage.generate_presigned_url(
        key=file_key,
        expire_time=30 * 24 * 60 * 60,  # 30天
    )
    
    print("\n" + "="*70)
    print("🎉 增强版系统上传成功！")
    print("="*70)
    print(f"\n🚀 增强版访问链接（30天有效）：\n{access_url}")
    print("\n" + "="*70)
    print("\n✨ 新增功能：")
    print("\n📊 仪表盘增强：")
    print("  ✓ 统计卡片可点击")
    print("  ✓ 点击客户总数 → 跳转到客户管理")
    print("  ✓ 点击打样订单 → 跳转到订单打样")
    print("  ✓ 点击设计报价 → 跳转到设计报价")
    print("  ✓ 点击正式订单 → 跳转到下单管理")
    print("  ✓ 点击售后订单 → 跳转到售后管理")
    
    print("\n📋 订单状态归类：")
    print("  ✓ 按状态分组显示（待处理、处理中、已完成、已取消）")
    print("  ✓ 每个状态显示订单数量")
    print("  ✓ 搜索时也保持状态归类")
    
    print("\n" + "="*70)
    
    return access_url

if __name__ == "__main__":
    url = upload_enhanced_system()

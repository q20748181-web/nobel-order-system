"""
上传完整版系统到对象存储
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_complete_system():
    """上传完整版HTML文件到对象存储"""
    
    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 读取HTML文件
    html_file_path = "/workspace/projects/assets/cabinet_system_v2_complete.html"
    
    print("📖 正在读取完整版HTML文件...")
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✅ 文件读取成功，大小：{len(html_content)} 字符")
    
    # 上传到对象存储（使用新文件名）
    print("⬆️  正在上传到对象存储...")
    file_key = storage.upload_file(
        file_content=html_content.encode('utf-8'),
        file_name="cabinet_v3.html",
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
    print("🎉 完整版系统上传成功！")
    print("="*70)
    print(f"\n🚀 永久访问链接（30天有效）：\n{access_url}")
    print("\n" + "="*70)
    print("\n✨ 系统功能完整清单：")
    print("\n👥 客户管理：")
    print("  ✓ 添加客户（客户代码、地区、Logo上传）")
    print("  ✓ 编辑客户信息")
    print("  ✓ 删除客户")
    print("  ✓ Logo图片预览")
    print("  ✓ 搜索客户")
    
    print("\n🎨 订单打样管理：")
    print("  ✓ 创建打样订单")
    print("  ✓ 更新订单状态")
    print("  ✓ 删除订单")
    print("  ✓ 搜索订单")
    
    print("\n💰 订单设计报价：")
    print("  ✓ 创建设计报价订单")
    print("  ✓ 更新订单状态")
    print("  ✓ 删除订单")
    print("  ✓ 搜索订单")
    
    print("\n📝 下单管理：")
    print("  ✓ 创建正式订单")
    print("  ✓ 更新订单状态")
    print("  ✓ 删除订单")
    print("  ✓ 搜索订单")
    
    print("\n🔧 订单售后管理：")
    print("  ✓ 创建售后订单")
    print("  ✓ 更新订单状态")
    print("  ✓ 删除订单")
    print("  ✓ 搜索订单")
    
    print("\n📊 仪表盘：")
    print("  ✓ 实时统计各类订单数量")
    print("  ✓ 显示最近订单")
    
    print("\n💾 数据功能：")
    print("  ✓ 本地数据持久化")
    print("  ✓ 刷新页面不丢失")
    print("  ✓ 预载示例数据")
    
    print("\n" + "="*70)
    
    return access_url

if __name__ == "__main__":
    url = upload_complete_system()

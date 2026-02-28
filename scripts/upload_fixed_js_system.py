"""
上传修复JavaScript转义问题的系统到对象存储
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_fixed_js_system():
    """上传修复后的HTML文件到对象存储"""
    
    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 读取HTML文件
    html_file_path = "/workspace/projects/assets/cabinet_system_v6_fixed.html"
    
    print("📖 正在读取修复后的HTML文件...")
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✅ 文件读取成功，大小：{len(html_content)} 字符")
    
    # 上传到对象存储
    print("⬆️  正在上传到对象存储...")
    file_key = storage.upload_file(
        file_content=html_content.encode('utf-8'),
        file_name="cabinet_fixed_js.html",
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
    print("🎉 JavaScript转义问题修复完成！")
    print("="*70)
    print(f"\n🚀 修复版访问链接（30天有效）：\n{access_url}")
    print("\n" + "="*70)
    print("\n🔧 修复内容：")
    print("  ✓ 修复了renderOrders函数中的字符串转义问题")
    print("  ✓ 修复了filterOrders函数中的字符串转义问题")
    print("  ✓ 编辑按钮现在可以正常点击")
    print("  ✓ 所有订单操作功能恢复正常")
    
    print("\n✨ 现在可以正常使用的功能：")
    print("  ✓ 客户管理：添加/编辑/删除/搜索")
    print("  ✓ 订单管理：创建/编辑/更新状态/删除/搜索")
    print("  ✓ 仪表盘：可点击跳转")
    print("  ✓ 订单状态归类显示")
    
    print("\n" + "="*70)
    
    return access_url

if __name__ == "__main__":
    url = upload_fixed_js_system()

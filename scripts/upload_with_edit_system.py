"""
上传带编辑功能的系统到对象存储
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_with_edit_system():
    """上传带编辑功能的HTML文件到对象存储"""
    
    # 初始化存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 读取HTML文件
    html_file_path = "/workspace/projects/assets/cabinet_system_v5_with_edit.html"
    
    print("📖 正在读取带编辑功能的HTML文件...")
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✅ 文件读取成功，大小：{len(html_content)} 字符")
    
    # 上传到对象存储
    print("⬆️  正在上传到对象存储...")
    file_key = storage.upload_file(
        file_content=html_content.encode('utf-8'),
        file_name="cabinet_with_edit.html",
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
    print("🎉 带编辑功能的系统上传成功！")
    print("="*70)
    print(f"\n🚀 访问链接（30天有效）：\n{access_url}")
    print("\n" + "="*70)
    print("\n✨ 新增功能：")
    print("\n📝 订单编辑功能：")
    print("  ✓ 每个订单卡片新增「编辑」按钮（橙色）")
    print("  ✓ 点击编辑后显示订单详情表单")
    print("  ✓ 可修改：客户、订单内容、金额、状态、备注")
    print("  ✓ 订单号不可修改（保持唯一性）")
    print("  ✓ 点击「更新订单」保存修改")
    
    print("\n📊 现有功能：")
    print("  ✓ 仪表盘卡片可点击，快速跳转")
    print("  ✓ 订单按状态归类显示")
    print("  ✓ 客户Logo上传")
    print("  ✓ 数据本地持久化")
    
    print("\n" + "="*70)
    print("\n🔧 按钮说明：")
    print("  🟨 编辑 - 修改订单详细信息")
    print("  📊 更新状态 - 快速更改订单状态")
    print("  🔴 删除 - 删除订单")
    
    print("\n" + "="*70)
    
    return access_url

if __name__ == "__main__":
    url = upload_with_edit_system()

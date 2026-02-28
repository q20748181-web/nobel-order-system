"""
上传修复版系统并更新短链接
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_and_update():
    """上传文件并更新重定向"""
    
    # 文件路径
    local_file = "/workspace/projects/assets/cabinet_system_v9_final.html"
    
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
        
        print("步骤1: 上传修复版系统...")
        key = storage.upload_file(
            file_content=file_content,
            file_name="cabinet_final_stable.html",  # 使用稳定文件名
            content_type="text/html; charset=utf-8",
        )
        
        print(f"✅ 系统文件已上传，对象Key: {key}")
        
        # 生成系统访问URL
        system_url = storage.generate_presigned_url(
            key=key,
            expire_time=365 * 24 * 60 * 60  # 1年
        )
        
        print(f"\n🔗 系统访问URL（1年有效）:")
        print(system_url)
        
        # 创建重定向HTML
        print("\n步骤2: 创建重定向HTML...")
        redirect_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={system_url}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>正在跳转...</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: white;
        }}
        .container {{ text-align: center; padding: 40px; }}
        .loader {{
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
        h1 {{ font-size: 24px; margin-bottom: 10px; }}
        p {{ opacity: 0.9; font-size: 16px; margin-bottom: 20px; }}
        .manual-link {{
            display: inline-block;
            padding: 15px 25px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-size: 14px;
            margin-top: 20px;
            transition: all 0.3s;
        }}
        .manual-link:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }}
        .auto-redirect {{ font-size: 14px; opacity: 0.8; margin-top: 10px; }}
    </style>
    <script>
        window.location.href = "{system_url}";
        setTimeout(function() {{ window.location.href = "{system_url}"; }}, 100);
    </script>
</head>
<body>
    <div class="container">
        <div class="loader"></div>
        <h1>正在跳转到橱柜订单管理系统...</h1>
        <p>如果页面没有自动跳转，请点击下方链接</p>
        <a href="{system_url}" class="manual-link">手动点击跳转 →</a>
        <p class="auto-redirect">将在 3 秒内自动跳转...</p>
    </div>
</body>
</html>'''
        
        print("步骤3: 上传重定向文件...")
        redirect_key = storage.upload_file(
            file_content=redirect_html.encode('utf-8'),
            file_name="cabinet.html",  # 固定的短链接文件名
            content_type="text/html; charset=utf-8",
        )
        
        print(f"✅ 重定向文件已上传，对象Key: {redirect_key}")
        
        # 生成短链接URL
        short_url = storage.generate_presigned_url(
            key=redirect_key,
            expire_time=365 * 24 * 60 * 60  # 1年
        )
        
        return short_url, system_url
            
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    print("=" * 80)
    print("上传修复版系统并更新短链接")
    print("=" * 80)
    
    short_url, system_url = upload_and_update()
    
    if short_url and system_url:
        print("\n" + "=" * 80)
        print("🎉 系统修复完成！")
        print("=" * 80)
        print(f"\n🔗 短链接（固定，1年有效）：")
        print(short_url)
        print(f"\n📝 系统URL（直接访问）：")
        print(system_url)
        print(f"\n✨ 修复内容：")
        print("- 数据迁移：自动从v3迁移到v4，保留原有数据")
        print("- 短链接固定：以后只更新重定向HTML，链接不变")
        print("- 执行人员功能：所有订单类型都已添加执行人员字段")
        print("\n💡 使用建议：")
        print("- 保存短链接，以后更新系统时链接不变")
        print("- 系统会自动迁移旧数据")
        print("- 点击短链接访问最新版本系统")
        print("\n" + "=" * 80)
    else:
        print("\n❌ 处理失败")

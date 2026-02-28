"""
更新短链接重定向文件，指向新的系统链接
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def create_redirect_html():
    """创建重定向HTML"""
    
    # 新的系统链接
    long_url = "https://coze-coding-project.tos.coze.site/coze_storage_7611717619640762422/cabinet_enhanced_final_84f4a5ee.html?sign=1774845465-cc950ad077-0-c1e75c0ec2c5f761c2b987c302c303295ea94c900adee810caf727153cfffae7"
    
    redirect_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={long_url}">
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
        window.location.href = "{long_url}";
        setTimeout(function() {{ window.location.href = "{long_url}"; }}, 100);
    </script>
</head>
<body>
    <div class="container">
        <div class="loader"></div>
        <h1>正在跳转到橱柜订单管理系统...</h1>
        <p>如果页面没有自动跳转，请点击下方链接</p>
        <a href="{long_url}" class="manual-link">手动点击跳转 →</a>
        <p class="auto-redirect">将在 3 秒内自动跳转...</p>
    </div>
</body>
</html>'''
    
    return redirect_html

def upload_redirect_file():
    """上传重定向文件"""
    
    redirect_html = create_redirect_html()
    
    try:
        storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
        
        print("正在更新短链接重定向文件...")
        key = storage.upload_file(
            file_content=redirect_html.encode('utf-8'),
            file_name="c.html",  # 使用相同的文件名
            content_type="text/html; charset=utf-8",
        )
        
        print(f"✅ 重定向文件已更新，对象Key: {key}")
        
        # 生成预签名URL（1年有效）
        url = storage.generate_presigned_url(
            key=key,
            expire_time=365 * 24 * 60 * 60
        )
        
        return url
            
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=" * 80)
    print("更新短链接指向新版本系统")
    print("=" * 80)
    
    url = upload_redirect_file()
    
    if url:
        print("\n" + "=" * 80)
        print("🎉 短链接已更新！")
        print("=" * 80)
        print(f"\n🔗 短链接（1年有效）：")
        print(url)
        print(f"\n📝 说明：")
        print("- 短链接已更新指向新版本（包含执行人员功能）")
        print("- 此链接会自动跳转到橱柜订单管理系统")
        print("- 新增执行人员管理功能")
        print("\n" + "=" * 80)
    else:
        print("\n❌ 更新失败")

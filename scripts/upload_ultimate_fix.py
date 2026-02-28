"""
上传终极修复版系统
"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

def upload_ultimate_fix():
    """上传终极修复版"""
    
    local_file = "/workspace/projects/assets/cabinet_system_v10_ultimate.html"
    
    with open(local_file, 'rb') as f:
        file_content = f.read()
    
    try:
        storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
        
        print("正在上传终极修复版系统...")
        key = storage.upload_file(
            file_content=file_content,
            file_name="cabinet_final_stable.html",  # 覆盖之前的文件
            content_type="text/html; charset=utf-8",
        )
        
        print(f"✅ 系统文件已上传，对象Key: {key}")
        
        system_url = storage.generate_presigned_url(
            key=key,
            expire_time=365 * 24 * 60 * 60  # 1年
        )
        
        print(f"\n🔗 系统访问URL:")
        print(system_url)
        
        # 更新短链接重定向
        print("\n正在更新短链接重定向...")
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
        
        redirect_key = storage.upload_file(
            file_content=redirect_html.encode('utf-8'),
            file_name="cabinet.html",  # 固定短链接
            content_type="text/html; charset=utf-8",
        )
        
        print(f"✅ 短链接已更新，对象Key: {redirect_key}")
        
        short_url = storage.generate_presigned_url(
            key=redirect_key,
            expire_time=365 * 24 * 60 * 60
        )
        
        return short_url, system_url
            
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    print("=" * 80)
    print("上传终极修复版系统")
    print("=" * 80)
    
    short_url, system_url = upload_ultimate_fix()
    
    if short_url and system_url:
        print("\n" + "=" * 80)
        print("🎉 终极修复完成！")
        print("=" * 80)
        print(f"\n🔗 短链接（固定）：")
        print(short_url)
        print(f"\n✨ 核心修复：")
        print("- 使用addEventListener绑定事件")
        print("- 彻底解决onclick转义问题")
        print("- 所有按钮功能应该正常工作")
        print("\n🧪 测试建议：")
        print("1. 点击导航栏切换页面")
        print("2. 点击'添加客户'按钮")
        print("3. 点击订单的'编辑'按钮")
        print("4. 测试搜索功能")
        print("\n" + "=" * 80)
    else:
        print("\n❌ 上传失败")

"""
使用 is.gd 服务生成短链接
"""
import requests

def generate_short_link(long_url):
    """使用 is.gd 生成短链接"""
    
    api_url = "https://is.gd/create.php"
    params = {
        'format': 'simple',
        'url': long_url
    }
    
    try:
        print("正在生成短链接...")
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            short_url = response.text.strip()
            if short_url.startswith("http"):
                print(f"✅ 短链接生成成功！")
                print(f"\n原始链接:")
                print(long_url)
                print(f"\n短链接:")
                print(short_url)
                return short_url
            else:
                print(f"❌ 生成失败: {response.text}")
                return None
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 生成短链接失败: {e}")
        return None

if __name__ == "__main__":
    long_url = "https://coze-coding-project.tos.coze.site/coze_storage_7611717619640762422/cabinet_enhanced_final_de484c72.html?sign=1774844498-1cf0449c68-0-566bc097e3a6d1fc93bcca4e364ba6c753f65bdf40dbe6683f0d87570f234b26"
    
    short_url = generate_short_link(long_url)
    
    if short_url:
        print("\n" + "=" * 80)
        print("🎉 完成！")
        print("=" * 80)

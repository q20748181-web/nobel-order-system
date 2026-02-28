"""
尝试使用国内短链接服务
"""
import requests

def try_suo_run(long_url):
    """尝试使用 suo.run 生成短链接"""
    
    api_url = "http://suo.run/api.php"
    params = {
        'url': long_url
    }
    
    try:
        print("尝试使用 suo.run 服务...")
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            short_url = response.text.strip()
            print(f"返回结果: {short_url}")
            if short_url.startswith("http"):
                print(f"✅ 短链接生成成功！")
                print(f"\n原始链接:")
                print(long_url)
                print(f"\n短链接:")
                print(short_url)
                return short_url
            else:
                print(f"返回的不是有效链接: {short_url}")
                return None
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ suo.run 失败: {e}")
        return None

def try_sina_lt(long_url):
    """尝试使用 sina.lt 生成短链接"""
    
    api_url = "https://sina.lt/api.php"
    params = {
        'url': long_url
    }
    
    try:
        print("\n尝试使用 sina.lt 服务...")
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            short_url = response.text.strip()
            print(f"返回结果: {short_url}")
            if short_url.startswith("http"):
                print(f"✅ 短链接生成成功！")
                print(f"\n原始链接:")
                print(long_url)
                print(f"\n短链接:")
                print(short_url)
                return short_url
            else:
                print(f"返回的不是有效链接: {short_url}")
                return None
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ sina.lt 失败: {e}")
        return None

def try_c1n(long_url):
    """尝试使用 c1n.cn 生成短链接"""
    
    # c1n.cn 可能需要 POST 请求
    api_url = "https://c1n.cn/api"
    
    try:
        print("\n尝试使用 c1n.cn 服务...")
        response = requests.post(api_url, json={'url': long_url}, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"返回结果: {result}")
            if 'short_url' in result or 'data' in result:
                short_url = result.get('short_url') or result.get('data')
                print(f"✅ 短链接生成成功！")
                print(f"\n原始链接:")
                print(long_url)
                print(f"\n短链接:")
                print(short_url)
                return short_url
            else:
                print(f"返回结果中没有短链接: {result}")
                return None
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ c1n.cn 失败: {e}")
        return None

if __name__ == "__main__":
    long_url = "https://coze-coding-project.tos.coze.site/coze_storage_7611717619640762422/cabinet_enhanced_final_de484c72.html?sign=1774844498-1cf0449c68-0-566bc097e3a6d1fc93bcca4e364ba6c753f65bdf40dbe6683f0d87570f234b26"
    
    # 尝试多个服务
    services = [try_suo_run, try_sina_lt, try_c1n]
    
    for service in services:
        short_url = service(long_url)
        if short_url:
            print("\n" + "=" * 80)
            print("🎉 完成！")
            print("=" * 80)
            break
    else:
        print("\n❌ 所有服务都失败了")
        print(f"\n原始链接仍然可用:")
        print(long_url)

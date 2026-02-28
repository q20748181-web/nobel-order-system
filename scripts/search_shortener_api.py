"""
搜索可用的短链接服务API
"""
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

ctx = new_context(method="search.web")

client = SearchClient(ctx=ctx)

response = client.web_search(
    query="免费短链接API服务 缩短网址API",
    count=10
)

if response.web_items:
    print("=" * 80)
    print("搜索到的短链接服务：")
    print("=" * 80)
    for i, item in enumerate(response.web_items, 1):
        print(f"\n{i}. {item.title}")
        print(f"   来源: {item.site_name}")
        print(f"   URL: {item.url}")
        if item.snippet:
            print(f"   简介: {item.snippet[:200]}...")
    print("\n" + "=" * 80)
else:
    print("未找到相关结果")

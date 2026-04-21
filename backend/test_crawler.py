import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from app.crawlers.simple_crawler import WeiboCrawler, DouyinCrawler, XiaohongshuCrawler

async def test_crawler():
    print("测试爬虫...")
    
    weibo = WeiboCrawler()
    douyin = DouyinCrawler()
    xiaohongshu = XiaohongshuCrawler()
    
    print("\n1. 测试微博爬虫 - 搜索: 肖战")
    try:
        weibo_results = await weibo.search_user("肖战")
        print(f"   结果数量: {len(weibo_results)}")
        if weibo_results:
            for r in weibo_results[:3]:
                print(f"   - {r.get('weibo_name')}: {r.get('fans_count')} 粉丝")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n2. 测试抖音爬虫 - 搜索: 肖战")
    try:
        douyin_results = await douyin.search_user("肖战")
        print(f"   结果数量: {len(douyin_results)}")
        if douyin_results:
            for r in douyin_results[:3]:
                print(f"   - {r.get('douyin_name')}: {r.get('fans_count')} 粉丝")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n3. 测试小红书爬虫 - 搜索: 肖战")
    try:
        xhs_results = await xiaohongshu.search_user("肖战")
        print(f"   结果数量: {len(xhs_results)}")
        if xhs_results:
            for r in xhs_results[:3]:
                print(f"   - {r.get('xhs_name')}: {r.get('fans_count')} 粉丝")
    except Exception as e:
        print(f"   错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_crawler())

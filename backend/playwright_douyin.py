import asyncio
from playwright.async_api import async_playwright
from datetime import date
from typing import List, Dict, Optional
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'


class PlaywrightDouyinCrawler:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    async def init(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await self.context.new_page()
        print("Playwright 浏览器已启动")
    
    async def search_user(self, keyword: str, max_results: int = 10) -> List[Dict]:
        if not self.page:
            await self.init()
        
        results = []
        
        try:
            search_url = f"https://www.douyin.com/search/{keyword}?type=user"
            print(f"正在访问: {search_url}")
            
            await self.page.goto(search_url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(3)
            
            await self.page.screenshot(path="screenshot_douyin_search.png")
            print("已保存截图: screenshot_douyin_search.png")
            
            content = await self.page.content()
            with open("page_content_douyin.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("已保存页面内容: page_content_douyin.html")
            
            user_cards = await self.page.query_selector_all('[class*="user"]')
            print(f"找到 {len(user_cards)} 个用户元素")
            
            for i, card in enumerate(user_cards[:max_results]):
                try:
                    name_elem = await card.query_selector('[class*="name"], [class*="title"]')
                    fans_elem = await card.query_selector('[class*="fans"], [class*="count"]')
                    
                    if name_elem:
                        name = await name_elem.inner_text()
                        fans_text = "0"
                        if fans_elem:
                            fans_text = await fans_elem.inner_text()
                        
                        fans_count = self.parse_fans(fans_text)
                        
                        results.append({
                            "douyin_name": name.strip(),
                            "fans_count": fans_count,
                            "collect_date": str(date.today())
                        })
                        print(f"  [{i+1}] {name.strip()}: {fans_text} ({fans_count})")
                    
                except Exception as e:
                    print(f"  解析用户卡片错误: {e}")
            
        except Exception as e:
            print(f"搜索错误: {e}")
            await self.page.screenshot(path="screenshot_douyin_error.png")
        
        return results
    
    def parse_fans(self, text: str) -> int:
        text = text.strip().replace(',', '')
        if '万' in text:
            num = float(text.replace('万', '').strip())
            return int(num * 10000)
        elif '亿' in text:
            num = float(text.replace('亿', '').strip())
            return int(num * 100000000)
        else:
            try:
                return int(text.replace(',', '').strip())
            except:
                return 0
    
    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


async def test_douyin_crawler():
    crawler = PlaywrightDouyinCrawler(headless=False)
    
    try:
        results = await crawler.search_user("肖战")
        print(f"\n搜索结果: {len(results)} 个")
        for r in results:
            print(f"  - {r['douyin_name']}: {r['fans_count']} 粉丝")
    finally:
        await crawler.close()


if __name__ == "__main__":
    asyncio.run(test_douyin_crawler())

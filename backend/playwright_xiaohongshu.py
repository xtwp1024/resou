import asyncio
from playwright.async_api import async_playwright
from datetime import date
from typing import List, Dict, Optional
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'


class PlaywrightXiaohongshuCrawler:
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
    
    async def close_cookie_banner(self):
        try:
            close_btn = await self.page.query_selector('[class*="close"], [aria-label*="关闭"], button:has-text("关闭")')
            if close_btn:
                await close_btn.click()
                await asyncio.sleep(1)
                print("已关闭 Cookie 弹窗")
        except:
            pass
    
    async def search_user(self, keyword: str, max_results: int = 10) -> List[Dict]:
        if not self.page:
            await self.init()
        
        results = []
        
        try:
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=user"
            print(f"正在访问: {search_url}")
            
            await self.page.goto(search_url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(3)
            
            await self.close_cookie_banner()
            
            await self.page.screenshot(path="screenshot_xiaohongshu_search.png")
            print("已保存截图: screenshot_xiaohongshu_search.png")
            
            content = await self.page.content()
            with open("page_content_xiaohongshu.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("已保存页面内容: page_content_xiaohongshu.html")
            
            selectors = [
                '.user-item',
                '.userItem',
                '[class*="search-user"]',
                '[class*="UserItem"]',
                '[class*="user-card"]',
                'a[href*="/user/profile/"]',
            ]
            
            user_cards = []
            for selector in selectors:
                cards = await self.page.query_selector_all(selector)
                if cards:
                    user_cards = cards
                    print(f"找到 {len(cards)} 个元素: {selector}")
                    break
            
            if not user_cards:
                all_links = await self.page.query_selector_all('a[href*="/user/profile/"]')
                print(f"找到 {len(all_links)} 个用户链接")
                
                for link in all_links[:max_results]:
                    try:
                        href = await link.get_attribute('href')
                        text = await link.inner_text()
                        if text.strip():
                            results.append({
                                "xhs_name": text.strip(),
                                "xhs_id": href.split('/')[-1] if href else None,
                                "fans_count": 0,
                                "collect_date": str(date.today())
                            })
                            print(f"  找到: {text.strip()}")
                    except:
                        pass
            
            for i, card in enumerate(user_cards[:max_results]):
                try:
                    name_elem = await card.query_selector('[class*="name"], [class*="title"], [class*="nickname"], a')
                    fans_elem = await card.query_selector('[class*="fans"], [class*="count"], [class*="follower"]')
                    
                    if name_elem:
                        name = await name_elem.inner_text()
                        fans_text = "0"
                        if fans_elem:
                            fans_text = await fans_elem.inner_text()
                        
                        fans_count = self.parse_fans(fans_text)
                        
                        results.append({
                            "xhs_name": name.strip(),
                            "fans_count": fans_count,
                            "collect_date": str(date.today())
                        })
                        print(f"  [{i+1}] {name.strip()}: {fans_text} ({fans_count})")
                    
                except Exception as e:
                    print(f"  解析用户卡片错误: {e}")
            
        except Exception as e:
            print(f"搜索错误: {e}")
            await self.page.screenshot(path="screenshot_xiaohongshu_error.png")
        
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


async def test_xiaohongshu_crawler():
    crawler = PlaywrightXiaohongshuCrawler(headless=False)
    
    try:
        results = await crawler.search_user("肖战")
        print(f"\n搜索结果: {len(results)} 个")
        for r in results:
            print(f"  - {r['xhs_name']}: {r['fans_count']} 粉丝")
    finally:
        await crawler.close()


if __name__ == "__main__":
    asyncio.run(test_xiaohongshu_crawler())

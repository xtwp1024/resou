import asyncio
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from app.database import SessionLocal
from app.models.models import Star, XiaohongshuData
from playwright.async_api import async_playwright
import json
import re


class XiaohongshuCrawler:
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
        print("浏览器已启动，请在浏览器中手动登录小红书...")
        print("登录完成后，按回车继续...")
        input()
    
    async def search_user(self, keyword: str, max_results: int = 5) -> list:
        results = []
        
        try:
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=user"
            print(f"正在搜索: {keyword}")
            
            await self.page.goto(search_url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            await self.page.screenshot(path=f"screenshot_xhs_{keyword}.png")
            
            user_links = await self.page.query_selector_all('a[href*="/user/profile/"]')
            print(f"找到 {len(user_links)} 个用户链接")
            
            for link in user_links[:max_results]:
                try:
                    href = await link.get_attribute('href')
                    parent = await link.evaluate_handle('el => el.closest("[class*=\'user\'], [class*=\'User\'], div")')
                    
                    text = await link.inner_text()
                    if text.strip() and href:
                        xhs_id = href.split('/user/profile/')[-1].split('?')[0]
                        
                        results.append({
                            "xhs_name": text.strip(),
                            "xhs_id": xhs_id,
                            "fans_count": 0,
                            "collect_date": str(date.today())
                        })
                        print(f"  - {text.strip()}")
                except Exception as e:
                    pass
            
        except Exception as e:
            print(f"搜索错误: {e}")
        
        return results
    
    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


async def main():
    db = SessionLocal()
    crawler = XiaohongshuCrawler(headless=False)
    
    try:
        await crawler.init()
        
        stars = db.query(Star).filter(~Star.xiaohongshu_data.any()).limit(50).all()
        print(f"\n需要采集小红书数据的明星: {len(stars)} 个")
        
        added = 0
        for i, star in enumerate(stars):
            print(f"\n[{i+1}/{len(stars)}] {star.name}")
            
            results = await crawler.search_user(star.name, max_results=3)
            
            if results:
                best = results[0]
                xhs_data = XiaohongshuData(
                    star_id=star.id,
                    xhs_name=best.get('xhs_name'),
                    xhs_id=best.get('xhs_id'),
                    fans_count=best.get('fans_count', 0),
                    has_official_account=True,
                    collect_date=date.today()
                )
                db.add(xhs_data)
                db.commit()
                added += 1
                print(f"  已添加: {best.get('xhs_name')}")
            else:
                print(f"  未找到")
            
            await asyncio.sleep(2)
        
        print(f"\n完成！共添加 {added} 条小红书数据")
        
    finally:
        await crawler.close()
        db.close()


if __name__ == "__main__":
    asyncio.run(main())

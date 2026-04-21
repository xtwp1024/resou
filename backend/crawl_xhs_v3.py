import asyncio
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from app.database import SessionLocal
from app.models.models import Star, XiaohongshuData


async def main():
    from playwright.async_api import async_playwright
    
    print("正在启动浏览器...")
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,
        args=['--start-maximized', '--disable-blink-features=AutomationControlled']
    )
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = await context.new_page()
    
    print("正在打开小红书...")
    await page.goto("https://www.xiaohongshu.com", timeout=60000)
    await asyncio.sleep(5)
    
    print("等待登录... (30秒)")
    await asyncio.sleep(30)
    
    db = SessionLocal()
    
    stars = db.query(Star).filter(~Star.xiaohongshu_data.any()).limit(30).all()
    print(f"\n开始采集: {len(stars)} 个明星")
    
    added = 0
    for i, star in enumerate(stars):
        print(f"\n[{i+1}/{len(stars)}] {star.name}")
        
        try:
            await page.goto("https://www.xiaohongshu.com", timeout=30000)
            await asyncio.sleep(2)
            
            search_input = await page.query_selector('input[placeholder*="搜索"], input[type="text"]')
            if search_input:
                await search_input.click()
                await search_input.fill(star.name)
                await page.keyboard.press('Enter')
                await asyncio.sleep(3)
                
                user_tab = await page.query_selector('text=用户')
                if user_tab:
                    await user_tab.click()
                    await asyncio.sleep(2)
            
            links = await page.query_selector_all('a[href*="/user/profile/"]')
            print(f"  找到 {len(links)} 个用户链接")
            
            if links:
                best_match = None
                for link in links:
                    text = await link.inner_text()
                    if star.name in text:
                        best_match = link
                        break
                
                if not best_match:
                    best_match = links[0]
                
                href = await best_match.get_attribute('href')
                text = await best_match.inner_text()
                
                if text.strip() and href:
                    xhs_id = href.split('/user/profile/')[-1].split('?')[0]
                    
                    data = XiaohongshuData(
                        star_id=star.id,
                        xhs_name=text.strip(),
                        xhs_id=xhs_id,
                        fans_count=0,
                        has_official_account=True,
                        collect_date=date.today()
                    )
                    db.add(data)
                    db.commit()
                    added += 1
                    print(f"  已添加: {text.strip()}")
        except Exception as e:
            print(f"  错误: {e}")
        
        await asyncio.sleep(3)
    
    await browser.close()
    db.close()
    print(f"\n完成! 共添加 {added} 条小红书数据")


if __name__ == "__main__":
    asyncio.run(main())

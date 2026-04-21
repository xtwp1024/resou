import asyncio
import sys
import os
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from app.database import SessionLocal
from app.models.models import Star, XiaohongshuData

USER_DATA_DIR = Path(__file__).parent / "browser_data_xiaohongshu"


async def main():
    from playwright.async_api import async_playwright
    
    print("后台自动采集小红书数据...")
    print(f"浏览器数据目录: {USER_DATA_DIR}")
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=True,
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            args=['--disable-blink-features=AutomationControlled', '--disable-gpu']
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("正在打开小红书...")
        await page.goto("https://www.xiaohongshu.com", timeout=60000)
        await asyncio.sleep(5)
        
        logged_in = await page.query_selector('a[href*="/user/profile/"], [class*="UserNickName"], [class*="nickname"]')
        
        if not logged_in:
            print("\n未检测到登录状态，请先运行 crawl_xhs_v4.py 登录")
            await context.close()
            return
        
        print("已检测到登录状态\n")
        
        db = SessionLocal()
        
        stars = db.query(Star).filter(~Star.xiaohongshu_data.any()).limit(100).all()
        print(f"开始采集: {len(stars)} 个明星\n")
        
        added = 0
        for i, star in enumerate(stars):
            print(f"[{i+1}/{len(stars)}] {star.name}", end=" ")
            
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
                        print(f"-> 已添加: {text.strip()[:30]}")
                    else:
                        print("-> 跳过")
                else:
                    print("-> 未找到")
            except Exception as e:
                print(f"-> 错误: {str(e)[:30]}")
            
            await asyncio.sleep(3)
        
        await context.close()
        db.close()
        print(f"\n完成! 共添加 {added} 条小红书数据")


if __name__ == "__main__":
    asyncio.run(main())
